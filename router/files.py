from fastapi import APIRouter, Depends, File, UploadFile
import shutil
from starlette.responses import FileResponse

import os

router = APIRouter(
    prefix='/file',
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


@router.get('/{fname}')
def download_file(fname: str):
    return FileResponse(os.path.join(os.getcwd(), 'static', fname), media_type='application/octet-stream', filename=fname)
