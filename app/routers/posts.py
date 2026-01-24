
from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session


from ..database import get_db
from .. import schemas, database_model, oauth2

router = APIRouter(tags=["Posts"])

@router.get('/posts', status_code=status.HTTP_200_OK, response_model=List[schemas.PostOutResponseVote])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip:int = 0, search:str = ""):
    #posts = db.query(database_model.Posts).filter(database_model.Posts.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(database_model.Posts, func.count(database_model.Votes.post_id).label("Votes")).join(database_model.Votes, database_model.Posts.id==database_model.Votes.post_id, isouter=True).group_by(database_model.Posts.id).all()
    #print(posts)
    posts = list(map(lambda x: x._mapping, posts))
    return posts

@router.get('/post/{id}', status_code=status.HTTP_200_OK, response_model=schemas.PostOutResponseVote)
def get_posts(id: int = id, db: Session = Depends(get_db)):
    post = db.query(database_model.Posts, func.count(database_model.Votes.post_id).label("Votes")).join(database_model.Votes, database_model.Posts.id==database_model.Votes.post_id, isouter=True).group_by(database_model.Posts.id).filter(database_model.Posts.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Not Found with id={id}")
    return post.first()._mapping

@router.post('/createpost', status_code=status.HTTP_201_CREATED, response_model=schemas.PostOutResponse)
def create_post(Inputpost: schemas.CreatePost , db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post = database_model.Posts(owner_id =current_user.id ,**Inputpost.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int = id, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post = db.query(database_model.Posts).filter(database_model.Posts.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Not Found with id={id}")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Post Cannot delete since no authorization")

    post.delete(synchronize_session=False)
    db.commit()

@router.put('/post/{id}', status_code= status.HTTP_200_OK, response_model=schemas.PostOutResponse)
def update_post(updated_input_post: schemas.UpdatePost, id: int = id, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post = db.query(database_model.Posts).filter(database_model.Posts.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Not Found with id={id}")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Post Cannot Update since no authorization")
    
    post.update(updated_input_post.model_dump() ,synchronize_session=False)
    db.commit()
    return post.first()
