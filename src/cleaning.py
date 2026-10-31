import os
import pandas as pd

# Left side = column name in your CSV (lowercase, spaces -> underscores).
# Adjust if your real file uses different headers.
COLUMN_MAP = {
    "date": "date",
    "market": "mandi",
    "commodity": "crop",
    "min_price": "min_price",
    "max_price": "max_price",
    "modal_price": "modal_price",
    "quantity": "arrivals",
}


def load_raw(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df.rename(columns=COLUMN_MAP)


def clean(df):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "modal_price"])

    for col in ["min_price", "max_price", "modal_price", "arrivals"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["mandi"] = df["mandi"].str.strip().str.title()
    df = df[df["modal_price"] > 0]

    # one row per mandi per day
    df = (df.groupby(["mandi", "date"], as_index=False)
            .agg(modal_price=("modal_price", "mean"),
                 arrivals=("arrivals", "sum")))
    return df.sort_values(["mandi", "date"]).reset_index(drop=True)


def report_quality(df):
    out = df.groupby("mandi").agg(
        first=("date", "min"), last=("date", "max"),
        days=("date", "nunique"),
    )
    out["span_days"] = (out["last"] - out["first"]).dt.days + 1
    out["coverage"] = (out["days"] / out["span_days"]).round(2)
    return out.sort_values("days", ascending=False)


if __name__ == "__main__":
    raw = load_raw("data/raw/soybean_maharashtra.csv")
    cleaned = clean(raw)
    print(report_quality(cleaned).head(15))
    os.makedirs("data/processed", exist_ok=True)
    cleaned.to_csv("data/processed/soybean_clean.csv", index=False)
    print("Saved data/processed/soybean_clean.csv")
