from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from schemas import schemas
from models import models

# from uuid import UUID
from hashing.hashing import getHash, checkHash
from auth import tokengen  # , oauth2
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    _ = print(f"\n\n{user.__dict__}\n\n") if user is not None else print("\n\nNone\n\n")

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials."
        )

    salt = user.salt if user is not None else None
    print("\nIs entered password same as stored password?", end=" ")
    print(f"{checkHash(request.password, salt, user.passwd)}\n")
    if not checkHash(request.password, salt, user.passwd):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials."
        )

    # Create JWT token

    access_token_expires = timedelta(hours=tokengen.ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = tokengen.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    print(f"\n\nAccess token = {access_token}\n\n")
    return {"access_token": access_token, "token_type": "bearer"}

    # return {
    #         "status": 200,
    #         "message": "Login successful"
    #        }


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    try:
        sl, pwd = getHash(request.password)
        new_user = models.User(
            Name=request.name,
            ContactNum=request.contactnum,
            Email=request.email,
            Password=pwd,
            Salt=sl,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"status": status.HTTP_201_CREATED, "new user": new_user}

    except Exception:
        return {"detail": f"User with email {request.email} already exists."}


# @router.post("/logout")
# async def logout():
#     pass
