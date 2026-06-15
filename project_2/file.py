from fastapi import APIRouter, UploadFile, File
import os
import shutil

router = APIRouter()


# @router.post("/upload")
# def file_upload(file: UploadFile = File(...)):
#     return {
#         "filename" : file.filename,
#         "content_type" : file.content_type
#     }

UPLOAD_DIR = "uploads"


@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }