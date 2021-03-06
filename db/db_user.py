from sqlalchemy.orm import Session
from schemas import UserBase
from .models import DbUser
from .hashing import get_password_hash
from fastapi import HTTPException


def create_user(db: Session, requests: UserBase):

    new_user = DbUser(
        username=requests.username,
        email=requests.email,
        password=get_password_hash(requests.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session):
    return db.query(DbUser).all()


def get_user_id(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f'User with {id} not found')
    return user


def update_user_db(id: int, request: UserBase, db: Session):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f'User with {id} not found')
    if user:
        user.username = request.username
        user.email = request.email
        user.password = get_password_hash(request.password)
        db.commit()
        return user


def delete_user_db(id: int, db: Session):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f'User with {id} not found')
    db.delete(user)
    db.commit()
