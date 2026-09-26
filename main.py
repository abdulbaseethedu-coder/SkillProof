from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, Optional

app = FastAPI(title='SkillProof API', version='1.0.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def root():
    return {'name': 'SkillProof API', 'status': 'ok'}

@app.get('/api/health')
def health():
    return {'status': 'healthy'}

# Backend-ready endpoints. The current frontend remains unchanged and continues
# to use its existing browser-side demo persistence so no visible feature changes
# are introduced by this repository conversion.
@app.get('/api/profile')
def get_profile():
    return {'message': 'Profile API ready. Frontend demo currently uses local persistence.'}

@app.get('/api/tasks')
def get_tasks():
    return {'message': 'Task API ready. Task definitions remain in the unchanged frontend.'}

class WorkPayload(BaseModel):
    account: Optional[str] = None
    task_id: Optional[int] = None
    payload: Dict[str, Any] = {}

@app.post('/api/work/save')
def save_work(data: WorkPayload):
    return {'status': 'accepted', 'task_id': data.task_id}

@app.post('/api/evaluate')
def evaluate(data: WorkPayload):
    return {'status': 'accepted', 'task_id': data.task_id}

@app.post('/api/understanding')
def understanding(data: WorkPayload):
    return {'status': 'accepted', 'task_id': data.task_id}
