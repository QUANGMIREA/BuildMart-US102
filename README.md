# BuildMart – teaching demo for software engineering

This repo is deliberately a **small process demonstration**, not a finished webshop.

The `main` and `develop` branches are a baseline **before** User Story US-102.
The `feature/US-102-product-unit` branch contains the complete, locally tested change.
Create the real Azure DevOps User Story and link it to your Pull Request.

## Run locally

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python -m scripts.migrate
python -m pytest -q --cov=app --cov-report=term-missing --cov-fail-under=80
python -m uvicorn app.main:app --reload
```

Open http://localhost:8000/products and http://localhost:8000/docs.

See `HUONG_DAN_VI.md` for a step-by-step Azure DevOps guide; see `docs/artifacts/ARTIFACT_REGISTER_RU.md`.
