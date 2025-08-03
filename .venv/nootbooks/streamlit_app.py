__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import pysqlite3
import sqlite3
import streamlit as st
import os
from PIL import Image
from dotenv import load_dotenv
import openai

from exit_advisor import ExitAdvisor
from info_advisor import InfoAdvisor
from scheduling_advisor import SchedulingAdvisor, df as schedule_df

# Constants
EXIT_KEYWORDS = {"exit", "quit", "bye"}
SCHED_KEYWORDS = {"schedule", "appointment", "interview", "meeting", "book", "booking", "set a meeting"}
INFO_KEYWORDS = {
    "who", "what", "how", "when", "where", "why", "which",
    "explain", "detail", "clarify", "clarification",
    "responsibility", "responsibilities"
}
GREETINGS = {"hi", "hello", "hey", "shalom", "שלום"}

# --- Setup and Assets ---
def setup_api():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

# Load agent context from Main_5.py
try:
    with open("Main_5.py", "r", encoding="utf-8") as f:
        AGENT_CONTEXT = f.read()
except FileNotFoundError:
    AGENT_CONTEXT = ""

@st.cache_resource
def load_assets():
    assets = {}
    base = "assets"
    assets['logo'] = Image.open(os.path.join(base, "logo.png")) if os.path.exists(os.path.join(base, "logo.png")) else None
    assets['banner'] = Image.open(os.path.join(base, "banner.png")) if os.path.exists(os.path.join(base, "banner.png")) else None
    assets['background'] = os.path.join(base, "background.jpg") if os.path.exists(os.path.join(base, "background.jpg")) else None
    return assets

# Apply custom CSS
def apply_custom_styles(background_path=None):
    css = ""
    if background_path:
        css += f".stApp {{ background-image: url('{background_path}'); background-size: cover; }}"
    css += """
    .user-bubble {
        background-color: #daf1ff;
        padding: 8px;
        border-radius: 8px;
        margin: 4px 0;
    }
    .assistant-bubble {
        background-color: #f0f0f0;
        padding: 8px;
        border-radius: 8px;
        margin: 4px 0;
    }
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Initialize session state
def init_state():
    if 'initialized' not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.exit_adv = ExitAdvisor()
        st.session_state.info_adv = InfoAdvisor()
        st.session_state.stage = 'normal'
        st.session_state.last_prof = None
        st.session_state.sched_pool = []
        st.session_state.sched_page = 0
        st.session_state.initialized = True

# Confirm slot choice
def confirm_slot(slot):
    SchedulingAdvisor.confirm_choice(slot, schedule_df)
    message = f"Your {slot['position']} appointment is confirmed for {slot['date']} at {slot['time']}."
    st.session_state.chat_history.append({'role': 'assistant', 'message': message})
    st.session_state.stage = 'normal'

# Next page of slots
def next_page():
    st.session_state.sched_page += 3
    if st.session_state.sched_page >= len(st.session_state.sched_pool):
        st.session_state.chat_history.append({'role': 'assistant', 'message': 'No more slots available.'})
        st.session_state.stage = 'normal'

# Chat fallback including context
def chat_fallback(user_input: str) -> str:
    for model in ["gpt-4o", "gpt-3.5-turbo"]:
        try:
            messages = []
            if AGENT_CONTEXT:
                messages.append({'role': 'system', 'content': AGENT_CONTEXT})
            messages.append({'role': 'system', 'content': (
                "You are an AI assistant: you find information and schedule appointments."
            )})
            messages.append({'role': 'user', 'content': user_input})
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception:
            continue
    return "I’m sorry, I’m having trouble responding right now."

# Main application
def main():
    setup_api()
    init_state()
    assets = load_assets()
    apply_custom_styles(assets.get('background'))

    # Sidebar menu
    if assets.get('logo'):
        st.sidebar.image(assets['logo'], use_column_width=True)
    st.sidebar.title('🗂️ Menu')
    st.sidebar.write('Use the menu for navigation.')

    # Header/banner
    if assets.get('banner'):
        st.image(assets['banner'], use_column_width=True)
    else:
        st.markdown('# ✨ AI Assistant')

    # Display chat history
    for entry in st.session_state.chat_history:
        bubble = 'user-bubble' if entry['role'] == 'user' else 'assistant-bubble'
        icon = '🗣️' if entry['role'] == 'user' else '🤖️'
        st.markdown(f"<div class='{bubble}'>{icon} {entry['message']}</div>", unsafe_allow_html=True)

    # Chat input form
    if st.session_state.stage == 'normal':
        with st.form('chat_form', clear_on_submit=True):
            inp = st.text_input('📝 Your message', key='input_text')
            submitted = st.form_submit_button('Send ✉️')
            if submitted and inp:
                text = inp.strip()
                st.session_state.chat_history.append({'role': 'user', 'message': text})
                low = text.lower()
                # Exit
                if low in EXIT_KEYWORDS:
                    st.session_state.chat_history.append({'role': 'assistant', 'message': 'Goodbye!'})
                # Greeting
                elif low in GREETINGS:
                    st.session_state.chat_history.append({'role': 'assistant', 'message': 'Hello! How can I help?'})
                # Next step -> schedule interview
                elif 'next step' in low:
                    role = st.session_state.last_prof or text
                    st.session_state.last_prof = role
                    st.session_state.stage = 'sched_role_month'
                    st.session_state.chat_history.append({'role': 'assistant', 'message': f"Sure—let's schedule an interview for the {role}. What month works for you?"})
                # Scheduling intent
                elif any(kw in low for kw in SCHED_KEYWORDS):
                    st.session_state.stage = 'sched_role_month'
                    st.session_state.chat_history.append({'role': 'assistant', 'message': 'Sure — what role and month would you like?'})
                # Info intent
                elif any(kw in low for kw in INFO_KEYWORDS):
                    st.session_state.last_prof = text
                    try:
                        resp = st.session_state.info_adv.get_info_answer(text)
                    except:
                        resp = 'Sorry, I cannot retrieve that information.'
                    st.session_state.chat_history.append({'role': 'assistant', 'message': resp})
                # Fallback
                else:
                    st.session_state.exit_adv.chat_history.append(text)
                    st.session_state.exit_adv.receive_output(text)
                    if st.session_state.exit_adv.decide_option() == 'End Conversation':
                        st.session_state.chat_history.append({'role': 'assistant', 'message': 'Goodbye!'})
                    else:
                        reply = chat_fallback(text)
                        st.session_state.chat_history.append({'role': 'assistant', 'message': reply})
                st.rerun()

    # Scheduling form
    elif st.session_state.stage == 'sched_role_month':
        with st.form('sched_form'):
            role = st.text_input('🎯 Role (e.g. Python Developer)', key='role_in')
            month = st.selectbox('🗓️ Month', [
                'January','February','March','April','May','June',
                'July','August','September','October','November','December'
            ], key='month_in')
            sched_sub = st.form_submit_button('Get available slots 🗓️')
            if sched_sub and role and month:
                prof = f"{role} {month}".strip()
                st.session_state.last_prof = prof
                pool = SchedulingAdvisor.get_schedule_options(prof, schedule_df)
                st.session_state.sched_pool = pool or []
                st.session_state.sched_page = 0
                if not pool:
                    st.session_state.chat_history.append({'role': 'assistant', 'message': 'No available slots.'})
                    st.session_state.stage = 'normal'
                else:
                    st.session_state.stage = 'sched_select'
                st.rerun()

    # Scheduling selection
    elif st.session_state.stage == 'sched_select':
        st.markdown('### 🗓️ Please select a slot:')
        cols = st.columns(4)
        pool = st.session_state.sched_pool
        page = st.session_state.sched_page
        for i, slot in enumerate(pool[page:page+3]):
            with cols[i]:
                label = f"{slot['date']} at {slot['time']}"
                st.button(f"➤ {label}", key=f"slot_{page+i}", on_click=confirm_slot, args=(slot,))
        with cols[3]:
            st.button('⏭️ None of these dates', key=f'none_{page}', on_click=next_page)

if __name__ == '__main__':
    main()
