from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth import tokengen

# from schemas import schemas
from sqlalchemy.orm import Session
from database.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user(email: str, db: Session = Depends(get_db)):
    # if email in db:
    #     user_dict = db[email]
    #     return schemas.UserInDB(**user_dict)
    pass


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    print("Credentials exception returned from here.")
    return tokengen.verify_token(token, credentials_exception)
