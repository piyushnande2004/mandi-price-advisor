"""Creates FAKE soybean price data for testing the pipeline. Not real prices."""
import os
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
dates = pd.date_range("2018-01-01", "2025-12-31", freq="D")
n = len(dates)
doy = dates.dayofyear.values
mandis = {"Nagpur": 0, "Amravati": -100, "Akola": -60, "Latur": 40, "Yavatmal": -120}

frames = []
for mandi, offset in mandis.items():
    trend = 3600 + 0.6 * np.arange(n)
    season = -350 * np.cos(2 * np.pi * (doy - 300) / 365)
    noise = pd.Series(rng.normal(0, 60, n)).rolling(7, min_periods=1).mean().values
    modal = trend + season + offset + noise
    arrivals = 800 + 600 * np.cos(2 * np.pi * (doy - 320) / 365) + rng.normal(0, 80, n)

    df = pd.DataFrame({
        "Date": dates,
        "Market": mandi,
        "Commodity": "Soyabean",
        "Min Price": (modal - rng.uniform(50, 150, n)).round(),
        "Max Price": (modal + rng.uniform(50, 150, n)).round(),
        "Modal Price": modal.round(),
        "Quantity": arrivals.clip(min=50).round(),
    })
    keep = (dates.dayofweek != 6) & (rng.random(n) > 0.10)
    frames.append(df[keep])

data = pd.concat(frames, ignore_index=True)

# add some dirt for the cleaning script to catch
bad = data.sample(frac=0.01, random_state=1).index
data.loc[bad, "Modal Price"] = 0
messy = data.sample(frac=0.02, random_state=2).index
data.loc[messy, "Market"] = data.loc[messy, "Market"].str.lower() + " "

os.makedirs("data/raw", exist_ok=True)
data.to_csv("data/raw/soybean_maharashtra.csv", index=False)
print("Saved data/raw/soybean_maharashtra.csv", data.shape)
