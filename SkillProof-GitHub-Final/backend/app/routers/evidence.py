from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db, get_auth_uid
from ..models import Evidence

router = APIRouter(prefix="/api/evidence", tags=["evidence"])

def pack(e):
    return {"id": e.id, "session_id": e.session_id, "task_title": e.task_title, "skill": e.skill, "score": e.score, "capabilities": e.capabilities, "evaluation": e.evaluation or {}, "understanding": e.understanding or {}, "created_at": e.created_at.isoformat()}

@router.get("")
def list_evidence(db: Session = Depends(get_db), uid: str = Depends(get_auth_uid)):
    return [pack(e) for e in db.query(Evidence).filter(Evidence.auth_uid == uid).order_by(Evidence.created_at.desc()).all()]

@router.get("/{evidence_id}")
def get_evidence(evidence_id: int, db: Session = Depends(get_db), uid: str = Depends(get_auth_uid)):
    e = db.query(Evidence).filter(Evidence.id == evidence_id, Evidence.auth_uid == uid).first()
    if not e: raise HTTPException(404, "Evidence not found")
    return pack(e)
