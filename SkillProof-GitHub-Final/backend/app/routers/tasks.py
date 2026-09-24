from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Task
from ..schemas import TaskIn

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

def serialize(t):
    return {"id":t.id,"course":t.course,"subject":t.subject,"skill":t.skill,"title":t.title,"workspace_type":t.workspace_type,
            "difficulty":t.difficulty,"estimated_minutes":t.estimated_minutes,"description":t.description,
            "scenario":t.scenario,"requirements":t.requirements or [],"resource":t.resource,
            "starter_code":t.starter_code,"evaluation_criteria":t.evaluation_criteria or {},"published":bool(t.published)}

@router.get("")
def list_tasks(course: str | None = Query(None), subject: str | None = Query(None), skill: str | None = Query(None), db: Session = Depends(get_db)):
    q = db.query(Task).filter(Task.published == 1)
    if course: q = q.filter(Task.course == course)
    if subject: q = q.filter(Task.subject == subject)
    if skill: q = q.filter(Task.skill == skill)
    return [serialize(t) for t in q.order_by(Task.course, Task.subject, Task.title).all()]

@router.get("/meta")
def task_meta(db: Session = Depends(get_db)):
    rows = db.query(Task).filter(Task.published == 1).all()
    courses = {}
    for t in rows:
        courses.setdefault(t.course or "Other", set()).add(t.subject or "General")
    return {"courses": [{"name":k,"subjects":sorted(v)} for k,v in sorted(courses.items())]}

@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    t = db.get(Task, task_id)
    if not t: raise HTTPException(404, "Task not found")
    return serialize(t)

@router.post("")
def create_task(data: TaskIn, db: Session = Depends(get_db)):
    t = Task(**data.model_dump())
    db.add(t); db.commit(); db.refresh(t)
    return serialize(t)
