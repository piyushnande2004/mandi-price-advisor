# Mandi Price Forecaster + Sell/Hold Advisor
> Status: work in progress. Results use synthetic sample data for pipeline testing; real Agmarknet/CEDA data is being integrated.

Forecasts Maharashtra mandi crop prices (starting with soybean) and advises whether to sell now or hold.

## Status
- [x] Project setup, cleaning pipeline, data quality report
- [ ] EDA + seasonal-naive baseline
- [ ] Prophet / LightGBM with time-based validation
- [ ] Forecast intervals
- [ ] Sell/hold advisor + backtest
- [ ] Streamlit app deployment

## Quick start (Windows PowerShell)
```powershell
.\setup.ps1
```
or manually:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/make_sample_data.py   # FAKE data, for testing only
python -m src.cleaning
streamlit run app.py
```

## Data
`data/raw/soybean_maharashtra.csv` currently holds **synthetic sample data** for testing the pipeline.
Replace it with real Agmarknet / CEDA data and update `COLUMN_MAP` in `src/cleaning.py` if the headers differ.
