# %%
import openai
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

openai.api_key = 'OPENAI_API_KEY'

def call_exit_advisor(chat_history: str, model: str = "ada:ft-your-org:exit-advisor-2025-07-XX") -> str:
    """
    מקבל את כל היסטוריית השיחה כטקסט,
    קורא למודל המותאם ומחזיר את הלייבל.
    """
    resp = openai.Completion.create(
        model=model,
        prompt=chat_history + "\n\n###\nLabel:",
        max_tokens=1,
        temperature=0
    )
    return resp.choices[0].text.strip()



# 1. טוענים את ה־JSON מקובץ
with open("sms_conversations.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. "מיישרים" (normalize) את הרשימה של ה-turns, ושומרים כעמודות את המטא
df = pd.json_normalize(
    data,
    record_path=['turns'],
    meta=['conversation_id', 'candidate_phone', 'recruiter_phone', 'start_time_utc']
)


# 3. המרת תאריכים ל־datetime
df['timestamp_utc']   = pd.to_datetime(df['timestamp_utc'])
df['start_time_utc']  = pd.to_datetime(df['start_time_utc'])

# 4. מיון לפי שיחה וזמן
df = df.sort_values(['conversation_id', 'timestamp_utc']).reset_index(drop=True)

# 5. יצירת תווית בינארית: האם זה turn עם label="end"?
df['y_end'] = (df['label'] == 'end').astype(int)

# 6. חישוב זמן תגובה בין תורות recruiter (אופציונלי)
#    – יוצרים רק תורות recruiter
df_rec = df[df['speaker'] == 'recruiter'].copy()
df_rec['prev_ts'] = df_rec.groupby('conversation_id')['timestamp_utc'].shift(1)
df_rec['response_secs'] = (
    df_rec['timestamp_utc'] - df_rec['prev_ts']
).dt.total_seconds()

# 7. בניית “היסטוריית שיחה” של N תורות אחרונים
def rolling_history(group, n=3):
    texts = group['text'].tolist()
    hist = []
    for i in range(len(texts)):
        start = max(0, i - n)
        hist.append(" ".join(texts[start:i]))
    return pd.Series(hist, index=group.index)

df_rec['history_last3'] = (
    df_rec.groupby('conversation_id')
          .apply(lambda g: rolling_history(g, n=3))
          .reset_index(level=0, drop=True)
)

# 8. בחירת העמודות הסופיות
prep_df = df_rec[[
    'conversation_id',
    'turn_id',
    'history_last3',  # input X: היסטוריה
    'text',           # input X: turn הנוכחי
    'y_end',          # target y
    'response_secs'   # אופציונלי: feature נוספת
]]


prep_df['response_secs'] = prep_df['response_secs'].fillna(0)





train, test = train_test_split(prep_df, test_size=20, random_state=0, shuffle=True)

label = 'y_end'

psn_train = train.index
psn_test = test.index

x_train = train.drop(columns=[label])
y_train = train[label]

x_test = test.drop(columns=[label])
y_test = test[label]




# 1. מגדירים את העיבוד המוקדם
preprocessor = ColumnTransformer([
    # TF‑IDF על העמודה 'text'
    ("tfidf_text",    TfidfVectorizer(max_features=2000, ngram_range=(1,2)), "text"),
    # TF‑IDF על ההיסטוריה
    ("tfidf_hist",    TfidfVectorizer(max_features=1000, ngram_range=(1,2)), "history_last3"),
    # שאר העמודות (מספריות) במצב passthrough
    ("num",           "passthrough", ["conversation_id", "turn_id", "response_secs"]),
])

# 2. בונים Pipeline עם scaler (ל‑RF לא חובה, אבל יכול לעזור) ו־RF
pipeline_rf = Pipeline([
    ("preproc", preprocessor),
    ("scale",   StandardScaler(with_mean=False)),
    ("rf",      RandomForestClassifier(n_estimators=100, max_depth=4, random_state=1))
])

# 3. אימון
pipeline_rf.fit(x_train, y_train)

# 4. חיזוי והערכת ביצועים
y_pred = pipeline_rf.predict(x_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, digits=4))

# 5. Confusion matrix visualization
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(4,3))
sns.heatmap(cm, annot=True, fmt="d", cbar=False)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.show()


class ExitAdvisor:
    def __init__(self,
                 json_path: str = "sms_conversations.json",
                 history_size: int = 3,
                 test_size: float = 0.2,
                 random_state: int = 42):
        self.history_size = history_size
        self.chat_history: List[str] = []

        # --- Load & preprocess dataset ---
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.json_normalize(
            data,
            record_path=['turns'],
            meta=['conversation_id','candidate_phone','recruiter_phone','start_time_utc']
        )
        df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'])
        df = df.sort_values(['conversation_id','timestamp_utc'])
        df['y_end'] = (df['label'] == 'end').astype(int)

        df_rec = df[df['speaker']=='recruiter'].copy()
        df_rec['prev_ts'] = df_rec.groupby('conversation_id')['timestamp_utc'].shift(1)
        df_rec['response_secs'] = (
            df_rec['timestamp_utc'] - df_rec['prev_ts']
        ).dt.total_seconds().fillna(0)

        def rolling_history(g, n=self.history_size):
            texts = g['text'].tolist()
            h = []
            for i in range(len(texts)):
                start = max(0, i - n)
                h.append(" ".join(texts[start:i]))
            return pd.Series(h, index=g.index)

        df_rec['history_last3'] = (
            df_rec.groupby('conversation_id')
                  .apply(rolling_history)
                  .reset_index(level=0, drop=True)
        )

        prep = df_rec[['history_last3','text','y_end','response_secs']]

        # --- Train/test split & pipeline training ---
        train, _ = train_test_split(
            prep,
            test_size=test_size,
            random_state=random_state,
            stratify=prep['y_end']
        )
        X_train = train.drop(columns=['y_end'])
        y_train = train['y_end']

        # רק TF‑IDF על הטקסט; נשליך שאר התכונות
        preprocessor = ColumnTransformer([
            ("tfidf_text", TfidfVectorizer(max_features=2000, ngram_range=(1,2)), "text"),
            ("tfidf_hist", TfidfVectorizer(max_features=1000, ngram_range=(1,2)), "history_last3")
        ], remainder='drop')

        self.pipeline = Pipeline([
            ("preproc", preprocessor),
            ("scale",   StandardScaler(with_mean=False)),
            ("rf",      RandomForestClassifier(
                             n_estimators=100,
                             max_depth=4,
                             random_state=1,
                             class_weight='balanced'
                       ))
        ])
        self.pipeline.fit(X_train, y_train)
        print("✅ Model trained on", len(X_train), "samples")

    def receive_output(self, output: str):
        self.main_output = output

    def decide_option(self) -> str:
        # 1) בדיקת מילים קבועות בעברית
        raw = " ".join(self.chat_history + [self.main_output]).lower()
        hebrew_goodbyes = ["bye","please stop texting me", "leave me alone", "Please remove me from your list. Thanks.","thanks for now", "I am not interested","Maybe I'm not the ideal candidate","Let's finish our conversation","Thanks for calling; I’ll be in touch.,That covers everything on the agenda. Thank you, everyone","I look forward to our next meeting","Talk to you later","Have a great day!"]
        if any(kw in raw for kw in hebrew_goodbyes):
            decision = "End Conversation"
            print(f"[ExitAdvisor]  keyword → {decision}")
            return decision


        hist = self.chat_history[-self.history_size:]
        hist_text = " ".join(hist)
        X = pd.DataFrame([{
            "history_last3": hist_text,
            "text":          self.main_output
        }])
        proba = self.pipeline.predict_proba(X)[0,1]
        threshold = 0.2
        decision = "End Conversation" if proba >= threshold else "Don't End Conv"
        print(f"[ExitAdvisor] ML prob(end)={proba:.3f} (thr={threshold}) → {decision}")
        return decision


class MainAgent:
    def __init__(self, advisor: ExitAdvisor):
        self.advisor = advisor

    def run_step(self, msg: str):
        self.advisor.chat_history.append(msg)
        output = f"{msg}"
        print(f"[MainAgent] Generated output: {output!r}")
        self.advisor.receive_output(output)
        dec = self.advisor.decide_option()
        print(f"[MainAgent] Decision: {dec}\n")
        return dec


if __name__ == "__main__":
    adv = ExitAdvisor()
    ag  = MainAgent(adv)

    print("הכנס הודעות, או 'quit' ליציאה.")
    while True:
        u = input("> ")
        if u.lower() in ("quit","exit"):
            break
        ag.run_step(u)



# %%
