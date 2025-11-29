import pandas as pd
import numpy as np

# ---------------------------------------------
# 1. Digital Direction with Doji Inversion
# ---------------------------------------------
def digital_direction(o, c, prev):
    if c > o: return 1
    if c < o: return 0
    return 1 - prev  # doji → invert previous


# ---------------------------------------------
# 2. Digital Amplitude (original Febex logic)
# ---------------------------------------------
def digital_amp(series):
    amp = []
    for i in range(len(series)):
        if i < 2:
            amp.append(0)
            continue

        seq = (series[i-2], series[i-1], series[i])
        if seq in [(0,1,1), (1,1,1)]:
            amp.append(1)
        elif seq in [(1,0,0), (0,0,0)]:
            amp.append(-1)
        else:
            amp.append(0)

    return amp


# ---------------------------------------------
# 3. ATR Calculation
# ---------------------------------------------
def atr(df, period=14):
    df["TR"] = df["High"] - df["Low"]
    df["ATR"] = df["TR"].rolling(period).mean()
    return df


# ---------------------------------------------
# 4. Full Hybrid Digital Amplitude Calculation
# ---------------------------------------------
def compute_hda(df):
    df = df.copy()

    # ---- Digital Direction ----
    binary = []
    prev = 0
    for o, c in zip(df["Open"], df["Close"]):
        d = digital_direction(o, c, prev)
        prev = d
        binary.append(d)

    df["Digit"] = binary

    # ---- Digital Amplitude ----
    df["DigitalAmp"] = digital_amp(binary)

    # ---- ATR / Volatility Amplitude ----
    df = atr(df)
    df["Amplitude"] = df["TR"] / df["ATR"]

    # ---- Strength Score ----
    df["Strength"] = df["Amplitude"] * df["Digit"].apply(lambda x: 1 if x == 1 else -1)

    # ---- Hybrid Digital Amplitude ----
    df["HDA"] = df["DigitalAmp"] + df["Strength"]

    return df
