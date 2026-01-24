from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError

from .routers import auth
from .database import get_db
from . import database_model
from .config import settings

# This get the token for us
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES =settings.access_token_expire_minutes


def create_token(data: dict):
    data_copy = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_copy.update({'exp': expire})

    token_encoded = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
    return token_encoded


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credential_exception =  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        token_decoded = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        id:str = token_decoded.get("user_id")
        if not id:
            raise credential_exception
    except JWTError:
        raise credential_exception

    user = db.query(database_model.Users).filter(database_model.Users.id == id).first()
    return user
