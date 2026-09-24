from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db, get_auth_uid
from ..models import Profile
from ..schemas import ProfileIn

router = APIRouter(prefix="/api/profile", tags=["profile"])

def find_profile(db, uid):
    return db.query(Profile).filter(Profile.auth_uid == uid).first()

@router.get("")
def get_profile(db: Session = Depends(get_db), uid: str = Depends(get_auth_uid)):
    return find_profile(db, uid)

@router.put("")
def update_profile(data: ProfileIn, db: Session = Depends(get_db), uid: str = Depends(get_auth_uid)):
    profile = find_profile(db, uid)
    if profile is None:
        profile = Profile(auth_uid=uid, registered=True)
        db.add(profile)
    for k, v in data.model_dump().items(): setattr(profile, k, v)
    profile.registered = True
    db.commit(); db.refresh(profile)
    return profile

@router.post("/register")
def register_profile(data: ProfileIn, db: Session = Depends(get_db), uid: str = Depends(get_auth_uid)):
    profile = find_profile(db, uid)
    if profile is None:
        profile = Profile(auth_uid=uid)
        db.add(profile)
    for k, v in data.model_dump().items(): setattr(profile, k, v)
    profile.registered = True
    db.commit(); db.refresh(profile)
    return profile
