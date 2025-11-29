import pandas as pd
from datetime import timedelta
from modules.utils import DATA_FILE, ensure_data_file, get_date

SESSION_SETS = {
    'Asian':      ['SYD', 'SYD-TOK', 'TOK'],
    'London':     ['LDN', 'LDN-NY', 'NY'],
    'New York':   ['NY', 'NY-SYD', 'SYD'],
    'Tokyo':      ['TOK', 'TOK-LDN', 'LDN']
}

def input_block():
    ensure_data_file()

    print("\nSession Sets:")
    sets = list(SESSION_SETS.keys())
    for i,s in enumerate(sets): print(f"{i+1}. {s}")

    idx = int(input("Select session set: ")) - 1
    session_name = sets[idx]
    sessions = SESSION_SETS[session_name]

    start = get_date("Start date (YYYY-MM-DD): ")
    end   = get_date("End date (YYYY-MM-DD): ")

    df = pd.read_csv(DATA_FILE)

    current = start
    rows = []

    while current <= end:
        if current.weekday() >= 5:
            current += timedelta(days=1)
            continue

        d = current.strftime("%Y-%m-%d")
        print(f"\nDate: {d} ({session_name})")
        print("Enter 3-digit binary (e.g. 101)")

        binary = input("Binary: ").strip()
        if len(binary) != 3: continue

        o = float(input("Open: "))
        h = float(input("High: "))
        l = float(input("Low: "))
        c = float(input("Close: "))

        rows.append({
            "Date": d,
            "Session_Set": session_name,
            "Session1_Outcome": int(binary[0]),
            "Session2_Outcome": int(binary[1]),
            "Session3_Outcome": int(binary[2]),
            "Open": o, "High": h, "Low": l, "Close": c
        })

        current += timedelta(days=1)

    if rows:
        pd.DataFrame(rows).to_csv(DATA_FILE, mode="a", header=False, index=False)
        print("\nSaved.")
