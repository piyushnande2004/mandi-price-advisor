import pandas as pd
from src.cleaning import clean


def test_clean_removes_zero_prices_and_normalizes_names():
    raw = pd.DataFrame({
        "date": ["2024-01-01", "2024-01-01", "2024-01-02"],
        "mandi": ["nagpur ", "Nagpur", "Nagpur"],
        "modal_price": [4000, 0, 4100],
        "arrivals": [100, 50, 120],
    })
    out = clean(raw)
    assert (out["modal_price"] > 0).all()
    assert out["mandi"].unique().tolist() == ["Nagpur"]
    assert len(out) == 2
