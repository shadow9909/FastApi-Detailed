from urllib import response
from fastapi import APIRouter, Depends
from schemas import ArticleDisplay, ArticleBase
from db.database import get_db
from sqlalchemy.orm import Session
from db.db_article import create_article, get_article
from schemas import UserBase
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/article'
)


@router.post('/')
def create(request: ArticleBase, db: Session = Depends(get_db), user: UserBase = Depends(get_current_user)):
    return create_article(db, request)


@router.get('/{id}')
def get(id: int, db: Session = Depends(get_db), user: UserBase = Depends(get_current_user)):
    return {'data': get_article(db, id), 'current_user': user}
