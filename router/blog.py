from fastapi import APIRouter, Response, Body, Query, Path
from enum import Enum
from typing import Optional, List, Dict
from pydantic import BaseModel

router = APIRouter()


class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'


class Image(BaseModel):
    image: str
    alias: str


class BlogModel(BaseModel):
    id: BlogType
    title: str
    comment: str
    tags: List[str] = []
    metadata: Dict[str, str] = {}
    images: Optional[Image] = None


@router.post('/blog/{id}/{comment_id}', status_code=201, tags=['blog'], summary="Get blog with ID", description="List the blog with the received ID")
def blog(id: BlogType, blog: BlogModel, content: str = Body(..., min_length=10, max_length=50, regex='[a-z\s]*$'),  comment_id: int = Path(None, gt=10, le=15), version: Optional[List[str]] = Query([1.0, 2.0]), limit: Optional[int] = 10):
    # version: Optional[List[str]] = Query(None)
    # response.status_code = 200
    return {'blog': blog}


def required_functionality():
    return {'message': 'FastAPI is important'}
