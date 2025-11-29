import os
import pandas as pd
from datetime import datetime

DATA_FILE = "data/forex_session_data_blocks.csv"

def ensure_data_file():
    """Create CSV if missing."""
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "Date", "Session_Set",
            "Session1_Outcome", "Session2_Outcome", "Session3_Outcome",
            "High", "Low", "Open", "Close"
        ])
        df.to_csv(DATA_FILE, index=False)


def get_date(prompt):
    while True:
        try:
            return datetime.strptime(input(prompt), "%Y-%m-%d").date()
        except:
            print("Invalid format. Use YYYY-MM-DD")
