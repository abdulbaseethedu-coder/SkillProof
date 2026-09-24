from pydantic import BaseModel

class ProfileIn(BaseModel):
    name: str
    degree: str = ""
    college: str = ""
    email: str = ""
    linkedin: str = ""
    github: str = ""
    about: str = ""

class TaskIn(BaseModel):
    course: str = ""
    subject: str = ""
    skill: str
    title: str
    workspace_type: str = "general"
    difficulty: str = "Beginner"
    estimated_minutes: int = 30
    description: str = ""
    scenario: str = ""
    requirements: list[str] = []
    resource: str = ""
    starter_code: str = ""
    evaluation_criteria: dict[str, str] = {}

class SessionIn(BaseModel):
    task_id: int

class VersionIn(BaseModel):
    code: str = ""
    workspace_state: dict = {}
    note: str = ""

class CodeIn(BaseModel):
    code: str = ""
    workspace_state: dict = {}

class MentorIn(BaseModel):
    message: str
    code: str = ""
    workspace_state: dict = {}
    history: list[dict] = []

class CheckIn(BaseModel):
    answers: dict[str, str] = {}
