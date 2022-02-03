from urllib import response
from fastapi import APIRouter, Response, Body, Query, Path, Depends
from enum import Enum
from typing import Optional, List, Dict
from pydantic import BaseModel
from schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session
from db.db_user import create_user, get_all_users, get_user_id, update_user_db, delete_user_db
from db.database import get_db

router = APIRouter(
    prefix='/user'
)


@router.post('/', response_model=UserDisplay)
def create(request: UserBase, db: Session = Depends(get_db)):
    return create_user(db, request)


@router.get('/all', response_model=List[UserDisplay])
def all(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.get('/{id}', response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db)):
    return get_user_id(db, id)


@router.put('/{id}', response_model=UserDisplay)
def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
    return update_user_db(id, request, db)


@router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db)):
    return delete_user_db(id, db)
