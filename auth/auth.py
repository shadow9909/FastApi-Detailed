from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import DbUser
from db.hashing import verify_password
from .oauth2 import create_access_token

router = APIRouter(
    tags=['authentication']
)


@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    if not (verify_password(user.password, request.password)):
        raise HTTPException(
            status_code=400, detail="Incorrect username or passwords")

    access_token = create_access_token(
        {'username': user.username})
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}
