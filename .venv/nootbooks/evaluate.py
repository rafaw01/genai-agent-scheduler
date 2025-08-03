"""
Evaluation script for Main Agent conversation routing.

Loads a labeled CSV of conversation turns and compares the system's predicted action
against the true labels. Actions:
  - End the conversation
  - Schedule an interview
  - Continue the conversation

Usage:
  python evaluate_agent.py --data labeled_conversations.csv
"""
import argparse
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import contextlib
import io

# Suppress prints during import of sub-agents
_silent_buf = io.StringIO()
with contextlib.redirect_stdout(_silent_buf):
    from exit_advisor import ExitAdvisor
    from scheduling_advisor import SchedulingAdvisor
    from info_advisor import InfoAdvisor

# Keywords for routing (should match main_agent.py)
EXIT_KEYWORDS = {"exit", "quit", "bye"}
SCHED_KEYWORDS = {"schedule", "appointment", "interview", "meeting", "book", "booking", "set a meeting"}
INFO_KEYWORDS = {
    "who", "what", "how", "when", "where", "why", "which",
    "explain", "detail", "clarify", "clarification",
    "responsibility", "responsibilities"
}

ACTION_END = "End the conversation"
ACTION_SCHEDULE = "Schedule an interview"
ACTION_CONTINUE = "Continue the conversation"


def predict_action(user_input: str, exit_adv: ExitAdvisor) -> str:
    low = user_input.lower()
    # 1. Direct exit
    if low in EXIT_KEYWORDS:
        return ACTION_END
    # 2. Scheduling
    if any(kw in low for kw in SCHED_KEYWORDS):
        return ACTION_SCHEDULE
    # 3. Info query
    if any(kw in low for kw in INFO_KEYWORDS):
        return ACTION_CONTINUE
    # 4. ExitAdvisor ML decision
    exit_adv.chat_history.append(user_input)
    exit_adv.receive_output(user_input)
    if exit_adv.decide_option() == "End Conversation":
        return ACTION_END
    # 5. Default to continue
    return ACTION_CONTINUE


def evaluate(data_path: str):
    # Load labeled data
    df = pd.read_csv(data_path)
    # Expect columns: conversation_id, turn_index, user_input, true_action
    y_true = []
    y_pred = []

    # Evaluate per conversation
    for conv_id, group in df.groupby("conversation_id"):
        exit_adv = ExitAdvisor()
        for _, row in group.sort_values("turn_index").iterrows():
            user_input = row["user_input"]
            true = row["true_action"]
            pred = predict_action(user_input, exit_adv)
            y_true.append(true)
            y_pred.append(pred)

    # Classification report
    print("Classification Report:")
    print(classification_report(y_true, y_pred,
                                labels=[ACTION_END, ACTION_SCHEDULE, ACTION_CONTINUE]))
    # Confusion matrix
    print("Confusion Matrix:")
    cm = confusion_matrix(y_true, y_pred, labels=[ACTION_END, ACTION_SCHEDULE, ACTION_CONTINUE])
    cm_df = pd.DataFrame(cm,
                         index=[ACTION_END, ACTION_SCHEDULE, ACTION_CONTINUE],
                         columns=[ACTION_END, ACTION_SCHEDULE, ACTION_CONTINUE])
    print(cm_df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Main Agent routing accuracy.")
    parser.add_argument(
        "--data",
        default="Sample_Labeled_Conversations.csv",
        help="Sample_Labeled_Conversations.csv"
    )
    args = parser.parse_args()
    evaluate(args.data)
