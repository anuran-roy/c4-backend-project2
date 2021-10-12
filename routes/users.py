from fastapi import APIRouter, Depends, status, HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
from schemas import schemas
from models import models
from uuid import UUID
from hashing.hashing import getHash

router = APIRouter(prefix="/user", tags=['Users'])


@router.get('/{id}', response_model=schemas.UserProfile)
async def get_user(id: UUID, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.userid == id).first()

    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not found.")

    return user
    # return {"details": f"User #{id}"}


@router.post('/add', status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    sl, pwd = getHash(str(request.password))
    new_user = models.User(Name=request.name,
                           ContactNum=request.contactnum, Email=request.email,
                           Password=pwd, Salt=sl)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
            "status": status.HTTP_201_CREATED
           }