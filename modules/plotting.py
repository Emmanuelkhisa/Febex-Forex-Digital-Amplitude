import matplotlib.pyplot as plt
import pandas as pd
from modules.utils import DATA_FILE
from modules.amplitude import compute_hda

plt.style.use("dark_background")

def plot_session():
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        print("No data.")
        return

    sets = df["Session_Set"].unique().tolist()
    for i,s in enumerate(sets): print(f"{i+1}. {s}")
    idx = int(input("Choose: ")) - 1
    name = sets[idx]

    subset = df[df["Session_Set"] == name].reset_index(drop=True)
    hda_df = compute_hda(subset)

    x = list(range(1, len(hda_df)+1))

    plt.figure(figsize=(12,6))
    plt.plot(x, hda_df["DigitalAmp"], label="Digital Amplitude", color="cyan")
    plt.plot(x, hda_df["HDA"], label="Hybrid Digital Amplitude", color="yellow")

    plt.title(f"Febex HDA — {name} Sessions")
    plt.xlabel("Day #")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()
