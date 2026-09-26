# SkillProof — Frontend + Backend

This repository separates the SkillProof project into frontend and backend folders **without changing the final frontend UI/features**.

## Structure

```text
SkillProof/
├── frontend/
│   ├── index.html
│   └── README.md
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

## Frontend

The final SkillProof HTML is preserved as the frontend application. It contains the current dashboard, authentication demo, task library, task-specific workrooms, SkillGuide, auto-save, versions, run/preview, evaluation, understanding check, skills, proof, profile, activity, logout, and SkillProof logo.

## Backend

FastAPI is provided as a separate backend layer with health/profile/task/work/evaluation/understanding endpoints ready for integration.

**Important:** To honor the request to keep the current features unchanged, the current standalone frontend is not forcibly rewritten to backend authentication/database calls. It continues to use its existing browser-side demo persistence. The backend is separated and ready for the next production integration step.

## Run backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API health: `http://127.0.0.1:8000/api/health`

## Production note

For production deployment, connect the frontend to the FastAPI backend, add a real database, secure authentication, isolated execution, and the selected AI provider. Do not put API secrets in the frontend.
