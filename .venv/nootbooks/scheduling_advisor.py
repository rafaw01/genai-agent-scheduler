import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy import create_engine, text, MetaData

# --- Load environment and initialize OpenAI client ---
load_dotenv()  # Load variables from .env file
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# --- Database connection setup via secrets.toml ---
conn_str = st.secrets["database"]["connection_string"]
engine = create_engine(conn_str, connect_args={"timeout": 10})
metadata = MetaData(schema='dbo')

# --- Helper to load and preprocess schedule DataFrame ---
def load_schedule_df() -> pd.DataFrame:
    try:
        with engine.connect() as connection:
            data = pd.read_sql_query(text("SELECT * FROM dbo.Schedule"), connection)
    except Exception as e:
        st.error(f"Failed to load schedule: {e}")
        return pd.DataFrame()

    df = pd.DataFrame(data)
    # Clean non-breaking spaces and trim whitespace
    df = df.replace(
        {r'\u00A0': ' ', r'(^\s+|\s+$)': ''},
        regex=True
    )

    # Ensure required columns exist
    required_columns = {'date', 'time', 'available', 'position'}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        st.error(f"Missing columns in schedule data: {missing_columns}")
        return pd.DataFrame()

    # Convert columns
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.time
    # Filter only available slots
    return df[df['available'] == True]

# Initial load
df = load_schedule_df()

class SchedulingAdvisor:
    MONTHS = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }

    @staticmethod
    def get_schedule_options(query: str, df: pd.DataFrame) -> List[Dict[str, Any]]:
        tmp = df.copy()

        if {'date', 'time'}.issubset(tmp.columns):
            tmp['slot_dt'] = pd.to_datetime(
                tmp['date'].astype(str) + ' ' + tmp['time'].astype(str),
                errors='coerce'
            )
        else:
            st.error("Required columns 'date' or 'time' are missing.")
            return []

        professions = tmp['position'].dropna().unique()
        prof = next((p for p in professions if p.lower() in query.lower()), None)
        if prof:
            tmp = tmp[tmp['position'].str.lower() == prof.lower()]

        for name, num in SchedulingAdvisor.MONTHS.items():
            if re.search(rf"\b{name}\b", query.lower()):
                tmp = tmp[tmp['slot_dt'].dt.month == num]
                break

        now = pd.Timestamp.now()
        future = tmp[tmp['slot_dt'] >= now]
        pool = future if not future.empty else tmp
        return pool.sort_values('slot_dt').to_dict(orient='records')

    @staticmethod
    def show_options(pool: List[Dict[str, Any]], start: int = 0) -> None:
        for idx, o in enumerate(pool[start:start+3], start=1):
            d = pd.to_datetime(o['date']).strftime('%Y-%m-%d')
            st.write(f"{idx}. {d} {o['time']} ({o['position']})")
        st.write("4. None of the options applies.")

    @staticmethod
    def confirm_choice(o: Dict[str, Any], df: pd.DataFrame) -> Dict[str, Any]:
        df.loc[
            (df['date'] == o['date']) &
            (df['time'] == o['time']) &
            (df['position'] == o['position']),
            'available'
        ] = False
        confirmed = {
            'date': pd.to_datetime(o['date']).strftime('%Y-%m-%d'),
            'time': str(o['time']),
            'position': o['position'],
            'available': False
        }
        st.success(f"Scheduled: {confirmed['date']} at {confirmed['time']} for {confirmed['position']}")
        return confirmed

    @staticmethod
    def run():
        st.title("Schedule Advisor")
        user_input = st.text_input("Enter profession (and optional month)")
        if not user_input:
            return

        pool = SchedulingAdvisor.get_schedule_options(user_input, df)
        if not pool:
            st.info("No dates available.")
            return

        page_start = 0
        SchedulingAdvisor.show_options(pool, page_start)

        choice = st.number_input("Select 1–4:", min_value=1, max_value=4, step=1)
        if choice <= 3 and page_start + choice - 1 < len(pool):
            SchedulingAdvisor.confirm_choice(pool[page_start + choice - 1], df)
        else:
            st.info("None matched or end of list.")

if __name__ == "__main__":
    SchedulingAdvisor.run()
