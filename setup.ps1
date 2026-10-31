# One-click setup for Windows PowerShell. Run from the project folder:  .\setup.ps1
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python src/make_sample_data.py
python -m src.cleaning
Write-Host ""
Write-Host "Setup done. Start the app with:  streamlit run app.py"
