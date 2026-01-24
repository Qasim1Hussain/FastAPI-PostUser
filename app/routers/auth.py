from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from ..database import get_db
from .. import utils, database_model, oauth2, schemas


router = APIRouter(tags=["Auth"])

@router.post('/login', response_model=schemas.TokenOutResponse)
def login(db: Session = Depends(get_db), user_login: OAuth2PasswordRequestForm = Depends()):
     user_username = user_login.username
     user_password = user_login.password
     user = db.query(database_model.Users).filter(database_model.Users.email == user_username).first()
     print("This is user", user_username)
     if not user:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
     
     if not utils.varify(user_password, user.password):
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
     
     access_token = oauth2.create_token(data={'user_id': user.id})
     return {"access_token": access_token, "token_type": "bearer"}
     

    