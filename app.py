import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Mandi Price Advisor", layout="wide")
st.title("Mandi Price Forecaster + Sell/Hold Advisor")
st.caption("Step 1: data explorer. Forecasts and the advisor come next.")

try:
    df = pd.read_csv("data/processed/soybean_clean.csv", parse_dates=["date"])
except FileNotFoundError:
    st.error("Run `python -m src.cleaning` first to create data/processed/soybean_clean.csv")
    st.stop()

mandis = sorted(df["mandi"].unique())
chosen = st.sidebar.multiselect("Mandi", mandis, default=mandis[:2])
view = df[df["mandi"].isin(chosen)]

c1, c2, c3 = st.columns(3)
c1.metric("Rows", f"{len(view):,}")
c2.metric("Latest modal price (Rs/qtl)", f"{view.sort_values('date')['modal_price'].iloc[-1]:,.0f}" if len(view) else "-")
c3.metric("Date range", f"{view['date'].min():%Y-%m-%d} to {view['date'].max():%Y-%m-%d}" if len(view) else "-")

st.plotly_chart(px.line(view, x="date", y="modal_price", color="mandi",
                        title="Modal price (Rs/quintal)"), use_container_width=True)
st.plotly_chart(px.line(view, x="date", y="arrivals", color="mandi",
                        title="Arrivals"), use_container_width=True)

# ---------------- Baselines ----------------
st.header("Baseline forecasts")
st.caption("Simple forecasts every later model must beat. Run `python -m src.baseline` first.")

try:
    scores = pd.read_csv("data/processed/baseline_scores.csv")
    preds = pd.read_csv("data/processed/baseline_predictions.csv", parse_dates=["origin"])
except FileNotFoundError:
    st.info("Run `python -m src.baseline` to create the baseline results.")
    st.stop()

st.subheader("Error by model and horizon (lower is better)")
st.dataframe(scores.pivot(index="model", columns="horizon", values="MAPE_pct")
             .rename_axis(columns="days ahead").round(2), use_container_width=True)
st.caption("Values are MAPE %, averaged over all mandis and all past forecast dates.")

col_a, col_b = st.columns(2)
mandi_pick = col_a.selectbox("Mandi", sorted(preds["mandi"].unique()))
horizon_pick = col_b.selectbox("Days ahead", sorted(preds["horizon"].unique()))
sel = preds[(preds["mandi"] == mandi_pick) & (preds["horizon"] == horizon_pick)].copy()
sel["target_date"] = sel["origin"] + pd.to_timedelta(sel["horizon"], unit="D")

actual = sel.drop_duplicates("target_date")[["target_date", "actual"]].assign(model="actual").rename(columns={"actual": "price"})
fc = sel[["target_date", "model", "pred"]].rename(columns={"pred": "price"})
plot_df = pd.concat([actual, fc])
st.plotly_chart(px.line(plot_df, x="target_date", y="price", color="model",
                        title=f"{mandi_pick}: forecast vs actual, {horizon_pick} days ahead"),
                use_container_width=True)
