"""
Main Agent orchestration for SMS chatbot.
Routes each incoming user message to the appropriate sub-agent using rule-based detection:
1. Direct exit commands
2. Scheduling flow (interactive)
3. InfoAdvisor query
4. ExitAdvisor ML-based conversation end
5. Greeting detection for friendly responses
6. Chat fallback (general conversation)
"""
import os
import warnings
import contextlib
import io
import openai
import re
from dotenv import load_dotenv

# Suppress pandas and deprecation warnings
warnings.filterwarnings("ignore")

# Load environment and OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Suppress prints during import of sub-agents
_silent_buf = io.StringIO()
with contextlib.redirect_stdout(_silent_buf):
    from exit_advisor import ExitAdvisor
    from info_advisor import InfoAdvisor
from scheduling_advisor import SchedulingAdvisor, df as schedule_df

# Keywords for routing
EXIT_KEYWORDS = {"exit", "quit", "bye"}
SCHED_KEYWORDS = {"schedule", "appointment", "interview", "meeting", "book", "booking", "set a meeting"}
INFO_KEYWORDS = {
    "who", "what", "how", "when", "where", "why", "which",
    "explain", "detail", "clarify", "clarification",
    "responsibility", "responsibilities"
}
GREETINGS = {"hi", "hello", "hey", "shalom", "שלום"}


def chat_fallback(user_input: str) -> str:
    """
    Fallback to OpenAI chat model for open conversation.
    Uses new openai.chat.completions API (v1.0.0+).
    """
    for model_name in ["gpt-4o", "gpt-3.5-turbo"]:
        try:
            resp = openai.chat.completions.create(
                model=model_name,
                messages=[{"role": "system", "content": "You are an AI recruitment assistant: you find candidates, provide information on open roles, and schedule interviews for qualified applicants."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=150
            )
            return resp.choices[0].message.content.strip()
        except Exception:
            continue
    return "I’m sorry, I’m having trouble responding right now."


def schedule_flow(initial_query: str) -> None:
    """
    Interactive scheduling flow: prompts for role/month if needed, shows slots, lets user choose.
    """
    prof_month = initial_query.strip()
    if not re.search(r"\b(month|january|february|march|april|may|june|july|august|september|october|november|december)\b", prof_month, re.IGNORECASE) \
       or not re.search(r"\b(role|profession|position|appointment)\b", prof_month, re.IGNORECASE):
        print("Assistant: Sure — what role (e.g. Python Developer) and month (e.g. March) would you like to schedule for? Or type 'exit' to cancel.")
        prof_month = input("User: ").strip()
        if prof_month.lower() in EXIT_KEYWORDS:
            print("Assistant: Scheduling canceled.")
            return

    pool = SchedulingAdvisor.get_schedule_options(prof_month, schedule_df)
    if not pool:
        print("Assistant: I’m sorry, no available slots match your criteria.")
        return

    page = 0
    while True:
        options_text = SchedulingAdvisor.show_options_page(pool, start=page)
        print(f"Assistant: {options_text}")
        choice = input("User: ").strip()
        if choice.lower() in EXIT_KEYWORDS:
            print("Assistant: Scheduling canceled.")
            return
        if re.fullmatch(r"[1-4]", choice):
            idx = int(choice)
            if 1 <= idx <= 3 and page + idx - 1 < len(pool):
                slot = pool[page + idx - 1]
                SchedulingAdvisor.confirm_choice(slot, schedule_df)
                print(f"Assistant: Your {slot['position']} appointment is confirmed for {slot['date']} at {slot['time']}.")
                return
            if idx == 4:
                page += 3
                if page >= len(pool):
                    print("Assistant: No more slots available.")
                    return
                continue
        print("Assistant: Invalid choice. Please enter 1-4 or 'exit'.")


def main():
    # Initialize sub-agents
    exit_adv = ExitAdvisor()
    info_adv = InfoAdvisor()

    print("Assistant: Hello! I’m an AI recruitment assistant. I help you find and schedule interviews, and provide information about positions. How can I assist you today? (type 'exit' to quit)")


    while True:
        user_input = input("User: ").strip()
        low = user_input.lower()

        # 1. Direct exit
        if low in EXIT_KEYWORDS:
            print("Assistant: Goodbye! Have a great day.")
            break

        # 1a. Greeting detection
        if low in GREETINGS:
            print(f"Assistant: {user_input.capitalize()}! How can I assist you today?")
            continue

        # 2. Scheduling flow
        if any(kw in low for kw in SCHED_KEYWORDS):
            schedule_flow(user_input)
            continue

        # 3. InfoAdvisor query
        if any(kw in low for kw in INFO_KEYWORDS):
            try:
                info_ans = info_adv.get_info_answer(user_input)
            except Exception:
                print("Assistant: I’m sorry, I’m having trouble retrieving information right now.")
                continue
            if info_ans and info_ans.strip():
                print(f"Assistant: {info_ans}")
            else:
                print("Assistant: I’m sorry, I don’t have that information right now.")
            continue

        # 4. ExitAdvisor ML-based check
        exit_adv.chat_history.append(user_input)
        exit_adv.receive_output(user_input)
        if exit_adv.decide_option() == "End Conversation":
            print("Assistant: It was nice talking with you. Goodbye!")
            break

        # 5. Chat fallback
        reply = chat_fallback(user_input)
        print(f"Assistant: {reply}")


if __name__ == "__main__":
    main()
