# SkillProof

> **Don't just claim your skills. Prove them through actual work.**

SkillProof is a practical skill-verification platform for students. It lets students choose real-world tasks, work inside a controlled Workroom, receive context-aware AI guidance, submit their work for evaluation, complete an understanding check, and build evidence of demonstrated ability.

## What is included

- React + Vite frontend
- FastAPI + SQLAlchemy backend
- SQLite database for the MVP
- Account-scoped persistence: work sessions, auto-saves, versions and evidence are keyed to the signed-in account UID
- Dynamic Task Library (not limited to a fixed 12 tasks)
- Course → Subject → Skill → Task structure
- Seeded tasks across B.Com, B.Sc Data Science, BCA, BBA, Chemistry, Physics, Mathematics, Biotechnology, BA English and B.Des
- Admin-ready `POST /api/tasks` endpoint for adding more tasks
- Workroom with task brief, work area, version saving and evidence flow
- Context-aware SkillGuide with optional OpenAI Responses API integration
- Safe fallback mentor when no API key is configured
- AI evaluation + understanding check demo flow
- Evidence-based profile and activity pages
- Profile editing

## Run locally

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# Optional: enable the real AI SkillGuide
# copy .env.example to .env and add your OpenAI API key

uvicorn app.main:app --reload --port 8000
```

Backend docs: `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.

## Real AI SkillGuide

The backend supports an optional OpenAI-powered SkillGuide. Put your key in `backend/.env`:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-5.6-luna
```

The mentor receives the task context, current student work and recent conversation, then is instructed to give hints and debugging guidance rather than a submit-ready solution. If no key is configured, the app clearly reports that the mentor is in demo/fallback mode instead of pretending the canned reply is live AI. The fallback also varies by task/question so it does not silently repeat one generic message.

Do **not** commit `.env` or an API key to GitHub.

## Task system

Tasks are stored in the database, so the frontend does not need to be changed when new tasks are added. Each task can include:

- course
- subject
- skill
- title
- difficulty
- estimated time
- real-world scenario
- requirements
- dataset/resource
- starter work
- evaluation criteria

Create a new task through the API:

`POST /api/tasks`

The Task Library automatically supports the new task.

## Product workflow

`Real-World Task → Workroom → SkillGuide → Student Work → Evidence → AI Evaluation → Understanding Check → Skill Demonstrated`

## Important MVP limitation

The `Run` button does not execute arbitrary student code on the FastAPI server. It returns a safe demo response. A production deployment should use an isolated sandbox/container runner for code execution.


## UX updates
- First-run profile registration flow for student name, degree/course, college, email and professional links.
- Persistent registration state for the demo.
- Global Back button with in-app navigation history.
- Top-right profile shortcut to Edit Profile.
- Registration is intentionally profile onboarding, not password authentication; full auth can be added later.

### Before testing the real mentor

1. Copy `backend/.env.example` to `backend/.env`.
2. Set `OPENAI_API_KEY=...`.
3. Keep `OPENAI_MODEL=gpt-5.6-luna` unless you intentionally choose another available model.
4. Start FastAPI from the project with `uvicorn app.main:app --reload --port 8000` while your working directory is `backend`, or use the included environment loading that resolves `backend/.env` directly.
5. In Workroom, the SkillGuide status should change to `Live AI mentor` after your first question.


## Account-based auto-save & resume

SkillProof sends the authenticated Firebase UID to the FastAPI backend as `X-User-Id`. Work sessions, versions and evidence are stored against that UID. The Workroom auto-saves changes to the database and the app resumes the latest session for the same account after sign-in. Logging out removes only the local session token; it does not delete saved work.

### Firebase setup
1. Create a Firebase project.
2. Enable Google and Email/Password sign-in providers.
3. Copy the web app config into `frontend/.env` using `.env.example`.
4. Run the frontend and backend.

> For a production deployment, replace the demo UID header trust with Firebase ID-token verification on the FastAPI server. The MVP keeps this boundary simple for hackathon development.
