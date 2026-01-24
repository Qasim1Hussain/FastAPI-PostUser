from fastapi import APIRouter, Depends, status, HTTPException

from .. import schemas, utils, database_model
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(tags=["User"])

@router.post("/createuser", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOutResponse)
def create_user(created_user: schemas.CreateUser, db: Session = Depends(get_db)):
    hash_password = utils.hash(created_user.password)
    created_user.password = hash_password

    user = database_model.Users(**created_user.model_dump())
    db.add(user)
    db.commit()

    db.refresh(user)
    return user

@router.get('/user/{id}',status_code=status.HTTP_200_OK, response_model= schemas.UserOutResponse)
def get_user(id: int = id, db: Session = Depends(get_db)):
    user =db.query(database_model.Users).filter(database_model.Users.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not found")
    return user.first()
