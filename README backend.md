# POPU Backend

FastAPI backend foundation for POPU, the AI-powered epidemiological intelligence platform for Nigeria.

## Phase 0

This phase establishes the API, configuration, CORS, health endpoint, and provider boundary. No database or production epidemiological feed is connected yet.

All epidemiological data must remain explicitly labelled as synthetic until an approved production source is connected and validated.

## Run on Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000/api/v1/health
- http://127.0.0.1:8000/docs
