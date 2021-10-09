from fastapi import APIRouter, Depends, status
from database.db import get_db
from sqlalchemy.orm import Session
from schemas import schemas
from models import models

router = APIRouter()

@router.get('/user/{id}', response_model=schemas.UserProfile, tags=['Users'])
async def get_user(id: int, db: Session = Depends(get_db)):
    entry = db.query(models.User).filter(models.User.userid == id).first()
    return entry
    # return {"details": f"User #{id}"}

@router.post('/createuser', status_code = status.HTTP_201_CREATED, tags=['Users'])
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(UserId = request.userid, Name=request.name, ContactNum=request.contactnum, Email=request.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

