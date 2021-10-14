from datetime import datetime, timedelta
from typing import Optional
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
# from pydantic import BaseModel
# from schemas import schemas
from routes import users
from fastapi import HTTPException, status

SECRET_KEY = 'b1ab5323dc7c3807a2788652aaca963fe5d2be8b6d37094f8fdc1d921b6b485a'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_HOURS = 168


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str,
                 credentials_exception=HTTPException(
                              status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="Could not validate credentials",
                              headers={"WWW-Authenticate": "Bearer"},
                                                    )
                 ):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        # token_data = schemas.TokenData(email=email)

        user = users.get_user_by_details(email)

        if user is None:
            raise credentials_exception

        return user

    except JWTError:
        raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    # if user is None:
    #     raise credentials_exception
    # return user
