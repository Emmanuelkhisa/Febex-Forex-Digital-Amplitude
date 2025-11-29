# 📘 **FEBEX HDA — Hybrid Digital Amplitude System**

*A Session-Structured Market Bias Engine Inspired by Febex Digital Amplitude*

---

## 🔥 Overview

**FEBEX HDA** is an advanced market-bias engine that analyzes the Forex market using a combination of:

### ✔ Digital Direction

### ✔ 3-Day Pattern Digital Amplitude

### ✔ Volatility-Weighted Strength (ATR-normalized)

### ✔ Hybrid Digital Amplitude (HDA)

This hybrid model captures both **directional structure** (session bias patterns) and **true candle amplitude** (range/volatility magnitude) — creating a unique “market heartbeat” signal.

The HDA system is designed for:

* Session-based market analytics
* Trend strength detection
* Market bias visualization
* Pattern-driven momentum modeling
* Direction-volatility hybrid analysis

---

## 🧪 What Makes Febex HDA Unique?

Traditional indicators treat price direction and volatility separately.

FEBEX HDA combines them.

It integrates:

1. **Binary Session Outcome (0/1)**
2. **Digital Amplitude (3-day pattern logic)**
3. **ATR-Normalized Volatility Amplitude**
4. **Directionally-Weighted Strength Score**

This creates a single, readable signal that shows:

* When sessions are strongly bullish
* When sessions are weak or indecisive
* When volatility confirms or contradicts direction
* When structural reversals begin forming

---

# 📚 Core Concepts

---

## 1. **Binary Session Outcome**

Each session is encoded into:

* **1 = bullish / upward bias**
* **0 = bearish / downward bias**
* **Doji = inverse of previous binary**
  *(to avoid directionless disruption)*

---

## 2. **Digital Amplitude (3-Day Pattern Rule)**

Digital Amplitude evaluates the **last 3 session outcomes**.

```
011 → +1  
111 → +1  
100 → -1  
000 → -1  
otherwise → 0
```

Interpretation:

* **+1** = structural bullish tendency
* **-1** = structural bearish tendency
* **0**  = noise / mixed pattern

---

## 3. **Volatility Amplitude (ATR-Normalized Range)**

Each session’s price amplitude:

```
range = high - low
amplitude = range / ATR(14)
```

This gives volatility in units of average range:

* 0.5 = half ATR
* 1.0 = average session
* 2.5 = strong expansion

---

## 4. **Directional Strength Score**

Volatility must respect direction.

So the amplitude is signed:

```
strength = amplitude * ( +1 or -1 depending on session direction )
```

---

## 5. **Hybrid Digital Amplitude (HDA)**

The **final signal** adds pattern logic + volatility strength:

```
HDA = DigitalAmplitude + StrengthScore
```

Examples:

* Strong bullish pattern → **+3.0**
* Weak mixed candle → **0**
* Violent bearish reversal → **–4.2**

This is the core "Hybrid Amplitude Wave".

---

# 📂 Project Structure

```
Febex-HDA/
│
├── data/
│   └── forex_session_data_blocks.csv     # Stored session data
│
├── modules/
│   ├── amplitude.py                      # Core amplitude & HDA logic
│   ├── data_input.py                     # Input system for binary & OHLC data
│   ├── plotting.py                       # Digital + Hybrid amplitude charts
│   └── utils.py                          # File checks, date helpers, etc
│
├── main.py                               # CLI menu program
│
└── README.md                             # Documentation
```

---

# 🛠 Installation & Requirements

### Requirements

```
Python 3.8+
pandas
matplotlib
numpy
```

### Install dependencies

```bash
pip install pandas matplotlib numpy
```

---

# 🚀 How to Use

---

## **1. Run the Program**

```bash
python main.py
```

You will see:

```
--- FEBEX HYBRID DIGITAL AMPLITUDE ---
1. Input Data Block
2. View Amplitude Chart
3. Exit
```

---

## **2. Input Session Data**

Select:

```
1 → Input Data Block
```

You’ll provide:

* Date range
* Session set (Asian / London / NY / Tokyo)
* 3-digit binary pattern
* OHLC values

The system automatically:

* Skips weekends
* Stores into CSV
* Prepares for amplitude computation

---

## **3. Visualize Amplitude Waves**

Select:

```
2 → View Amplitude Chart
```

You’ll see a dual-plot:

* **Digital Amplitude (classic Febex)**
* **Hybrid Digital Amplitude (volatility-weighted)**

The result shows:

* Market structure shifts
* Session-specific volatility expansions
* Reversal signals
* Trend continuation patterns

---

# 📊 Example Output Chart

* **Cyan** = Digital Amplitude (±1)
* **Yellow** = Hybrid Digital Amplitude (continuous wave)

Interpretation:

* Spikes = volatility bursts
* Smooth curves = structural trends
* Divergence = early trend-change warning

---

# 🔮 Future Extensions (Roadmap)

The system architecture supports future upgrades:

### 🚧 Coming Features

* Automatic OHLC extraction from **TradingView CSV**
* Direct OHLC from **MT5 Terminal**
* Probability map for digital patterns
* Forecasting model using hybrid distributions
* Heatmap of HDA ranges per session
* AI-based session bias predictor (LSTM/Transformer)
* Web dashboard (Plotly Dash)

---

# 🤝 Contribution

Pull requests, refinements, and analytics enhancements are welcome.

If you build advanced Febex-based indicators, feel free to contribute!

---

# 📄 License

MIT License — free to modify and distribute.

---

# ⭐ If you like this project

Please **star** the repository — it helps!

---

