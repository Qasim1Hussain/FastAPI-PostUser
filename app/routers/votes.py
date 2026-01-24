from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database_model, database, oauth2, schemas

router = APIRouter(tags=["Tags"])

@router.post('/votes')
def get_votes(votes: schemas.DoVoting, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    post = db.query(database_model.Posts).filter(database_model.Posts.id == votes.post_id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found")
    post_vote =  db.query(database_model.Votes).filter(database_model.Votes.post_id == votes.post_id,database_model.Votes.user_id == current_user.id)
    post_vote_already = post_vote.first()
    if votes.dir ==1:
        if post_vote_already:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted")
        new_vote = database_model.Votes(post_id= votes.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Post has been voted"}
    else:
        if not post_vote_already:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exists")
        post_vote.delete(synchronize_session=False)
        db.commit()
        return {"Message": "Post has been unvoted"}
    pass