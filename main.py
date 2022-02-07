from http import client
from urllib import response
from exceptions import StoryException
from fastapi import FastAPI, Request, Depends, WebSocket
from router import article, blog, user, product, files
from db import models
from db.database import engine
from fastapi.responses import PlainTextResponse, JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from auth import auth
from fastapi.staticfiles import StaticFiles
import os
from fastapi.templating import Jinja2Templates
import time

dir_path = os.getcwd()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response


# @app.get('/')
# def hello():
#     """[summary]
#     - **id** mandatory path parameter
#     - **id** mandatory path parameter

#     Returns:
#         [type]: [description]
#     """
#     return {'detail': 'Hello World'}


# class BlogType(str, Enum):
#     short = 'short'
#     story = 'story'
#     howto = 'howto'


# @app.post('/blog/{id}', status_code=201, tags=['blog'], summary="Get blog with ID", description="List the blog with the received ID")
# def blog(id: BlogType, response: Response, limit: Optional[int] = 10):
#     response.status_code = 200
#     return {'detail': f"{id} is found"}

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(files.router)

app.include_router(auth.router)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)

clients = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


@app.get('/dependency')
def dependency_demo(req_param: dict = Depends(blog.required_functionality)):
    return req_param


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={"message": "No Stories Please"}
    )


app.mount("/file", StaticFiles(directory="static"), name="static")


# @app.exception_handler(HTTPException)
# def http_exception(request: Request, exc: StoryException):
#     return PlainTextResponse(str(exc), status_code=400)


@app.api_route("/{path_name:path}", methods=["GET"], status_code=404)
async def catch_all(request: Request, path_name: str):
    return {"request_method": request.method, "path_name": path_name}


models.Base.metadata.create_all(engine)
