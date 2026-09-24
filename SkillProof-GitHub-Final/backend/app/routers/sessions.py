from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db, get_auth_uid
from ..models import Task, WorkSession, WorkVersion, Evidence
from ..schemas import SessionIn, VersionIn, CodeIn, MentorIn, CheckIn
from ..services.mentor import mentor_reply
from ..services.evaluator import evaluate, evaluate_understanding

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

def serialize(s):
    return {
        "id": s.id, "status": s.status, "current_code": s.current_code,
        "workspace_state": s.workspace_state or {}, "evaluation": s.evaluation or {}, "understanding": s.understanding or {},
        "task": {
            "id": s.task.id, "course": s.task.course, "subject": s.task.subject, "skill": s.task.skill, "title": s.task.title,
            "workspace_type": s.task.workspace_type, "difficulty": s.task.difficulty, "estimated_minutes": s.task.estimated_minutes,
            "description": s.task.description, "scenario": s.task.scenario, "requirements": s.task.requirements or [],
            "resource": s.task.resource, "starter_code": s.task.starter_code
        },
        "versions": [{"id":v.id,"note":v.note,"created_at":v.created_at.isoformat()} for v in s.versions]
    }

@router.post("")
def start_session(data: SessionIn, db: Session = Depends(get_db), uid: str = Depends(get_auth_uid)):
    task = db.get(Task, data.task_id)
    if not task: raise HTTPException(404, "Task not found")
    s = WorkSession(auth_uid=uid, task_id=task.id, current_code=task.starter_code, workspace_state={})
    db.add(s); db.commit(); db.refresh(s)
    return serialize(s)


@router.get("/resume")
def resume_session(db: Session = Depends(get_db), uid: str = Depends(get_auth_uid)):
    s = db.query(WorkSession).filter(WorkSession.auth_uid == uid).order_by(WorkSession.updated_at.desc()).first()
    return serialize(s) if s else None

@router.get("/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db), uid: str = Depends(get_auth_uid)):
    s = db.query(WorkSession).filter(WorkSession.id == session_id, WorkSession.auth_uid == uid).first()
    if not s: raise HTTPException(404, "Session not found")
    return serialize(s)

@router.post("/{session_id}/versions")
def save_version(session_id: int, data: VersionIn, db: Session = Depends(get_db), uid: str = Depends(get_auth_uid)):
    s = db.query(WorkSession).filter(WorkSession.id == session_id, WorkSession.auth_uid == uid).first()
    if not s: raise HTTPException(404, "Session not found")
    s.current_code = data.code
    s.workspace_state = data.workspace_state or {}
    s.updated_at = datetime.utcnow()
    s.versions.append(WorkVersion(code=data.code, workspace_state=data.workspace_state or {}, note=data.note))
    db.commit(); db.refresh(s)
    return serialize(s)

@router.post("/{session_id}/run")
def run_workspace(session_id: int, data: CodeIn, db: Session = Depends(get_db), uid: str = Depends(get_auth_uid)):
    s = db.query(WorkSession).filter(WorkSession.id == session_id, WorkSession.auth_uid == uid).first()
    if not s: raise HTTPException(404, "Session not found")
    s.current_code = data.code
    s.workspace_state = data.workspace_state or {}
    db.commit(); db.refresh(s)
    return {"output": _preview_output(s.task, data.code, data.workspace_state)}

def _preview_output(task, code: str, state: dict):
    """Safe MVP runner. It never executes arbitrary student code on the API server."""
    wt = (task.workspace_type or "general").lower()
    text = (code or "").strip()
    if wt in {"python", "java", "sql"}:
        lines = len(text.splitlines()) if text else 0
        return f"SkillProof safe preview\nWorkspace: {task.workspace_type}\nWork lines detected: {lines}\n\nExecution sandbox is intentionally isolated from the API server. Configure a container runner for real code execution."
    if wt == "physics":
        return f"Physics Lab preview\nObservations captured: {len([v for v in state.values() if str(v).strip()])}\n\nUse the observations and calculations area to verify your result before submission."
    if wt == "lab":
        return f"Lab Analysis preview\nFields completed: {len([v for v in state.values() if str(v).strip()])}\n\nCheck that your conclusion is supported by the observations."
    if wt in {"spreadsheet", "accounting"}:
        return f"Spreadsheet preview\nCells/fields with input: {len([v for v in state.values() if str(v).strip()])}\n\nReview variance/reconciliation reasoning before submission."
    if wt in {"dashboard", "business"}:
        return f"Analysis preview\nInputs captured: {len([v for v in state.values() if str(v).strip()])}\n\nCheck that each insight is backed by evidence from the task data."
    return f"Workspace preview\nInputs captured: {len([v for v in state.values() if str(v).strip()])}"

@router.post("/{session_id}/mentor")
def mentor(session_id: int, data: MentorIn, db: Session = Depends(get_db), uid: str = Depends(get_auth_uid)):
    s = db.query(WorkSession).filter(WorkSession.id == session_id, WorkSession.auth_uid == uid).first()
    if not s: raise HTTPException(404, "Session not found")
    task = {"title":s.task.title,"course":s.task.course,"subject":s.task.subject,"skill":s.task.skill,"difficulty":s.task.difficulty,"scenario":s.task.scenario,"requirements":s.task.requirements or [],"workspace_type":s.task.workspace_type}
    reply, provider = mentor_reply(data.message, task, data.code or s.current_code, data.history, data.workspace_state or s.workspace_state or {})
    return {"message": reply, "provider": provider, "ai_connected": provider == "openai"}

@router.post("/{session_id}/evaluate")
def evaluate_session(session_id: int, db: Session = Depends(get_db), uid: str = Depends(get_auth_uid)):
    s = db.query(WorkSession).filter(WorkSession.id == session_id, WorkSession.auth_uid == uid).first()
    if not s: raise HTTPException(404, "Session not found")
    result = evaluate(s.task, s.current_code, s.workspace_state or {})
    s.evaluation = result
    s.status = "evaluated"
    s.updated_at = datetime.utcnow()
    db.commit(); db.refresh(s)
    return result

@router.post("/{session_id}/understanding-check")
def understanding_check(session_id: int, data: CheckIn, db: Session = Depends(get_db), uid: str = Depends(get_auth_uid)):
    s = db.query(WorkSession).filter(WorkSession.id == session_id, WorkSession.auth_uid == uid).first()
    if not s: raise HTTPException(404, "Session not found")
    evaluation = s.evaluation or evaluate(s.task, s.current_code, s.workspace_state or {})
    result = evaluate_understanding(s.task, s.current_code, data.answers, evaluation)
    s.understanding = result
    if result.get("passed"):
        existing = db.query(Evidence).filter(Evidence.session_id == s.id).first()
        if not existing:
            ev = Evidence(auth_uid=uid, session_id=s.id, task_title=s.task.title, skill=s.task.skill,
                          score=int(evaluation.get("score", 0)),
                          capabilities=evaluation.get("capabilities", f"Demonstrated practical work for {s.task.title}."),
                          evaluation=evaluation, understanding=result)
            db.add(ev)
        else:
            existing.score = int(evaluation.get("score", existing.score or 0))
            existing.evaluation = evaluation
            existing.understanding = result
        s.status = "demonstrated"
    db.commit(); db.refresh(s)
    return result
