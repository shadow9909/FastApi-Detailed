from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.staticfiles import StaticFiles
import shutil

router = APIRouter(
    prefix='/files',
    tags=['file']
)


@router.post("/file")
async def create_file(file: bytes = File(...)):
    content = file.decode('utf-8')
    return {"file_size": content}


@router.post('/uploadfile')
def upload_file(upload_file: UploadFile = File(...)):
    path = f"static/{upload_file.filename}"
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return {
        'path': path
    }


router.mount("/static", StaticFiles(directory="static"), name="static")
