# Study Mate (AK)

AK is a WhatsApp AI study assistant. This repository is built step by step.

## Setup (Windows PowerShell)

```powershell
cd D:\Study-Mate
.\env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If activation is blocked:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

Copy `.env.example` to `.env` and adjust the values. Never commit `.env`.

## Run the app

```powershell
uvicorn backend.main:app --reload
```

Open http://127.0.0.1:8000/docs for the API documentation.

## Run tests

```powershell
python -m pytest -v
```

## Run Ruff (lint)

```powershell
ruff check .
```

## Continuous integration

On every push to `main` and every pull request to `main`, GitHub Actions
installs dependencies, runs `ruff check .` and then `python -m pytest -v`.
The workflow fails if either step fails.