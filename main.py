from typing import Optional
from fastapi import FastAPI, Request, Response, Depends
from enum import Enum
from router import blog

app = FastAPI()


@app.get('/')
def hello():
    """[summary]
    - **id** mandatory path parameter
    - **id** mandatory path parameter

    Returns:
        [type]: [description]
    """
    return {'detail': 'Hello World'}


# class BlogType(str, Enum):
#     short = 'short'
#     story = 'story'
#     howto = 'howto'


# @app.post('/blog/{id}', status_code=201, tags=['blog'], summary="Get blog with ID", description="List the blog with the received ID")
# def blog(id: BlogType, response: Response, limit: Optional[int] = 10):
#     response.status_code = 200
#     return {'detail': f"{id} is found"}

app.include_router(blog.router)


@app.get('/dependency')
def dependency_demo(req_param: dict = Depends(blog.required_functionality)):
    return req_param


@app.api_route("/{path_name:path}", methods=["GET"], status_code=404)
async def catch_all(request: Request, path_name: str):
    return {"request_method": request.method, "path_name": path_name}
