from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid
import shutil

router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_SIZE = 5 * 1024 * 1024  # 5 MB

ALLOWED_TYPES = [
    "image/jpeg",
    "image/png",
    "application/pdf",
]

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG and PDF files are allowed."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    MAX_SIZE = 5 * 1024 * 1024

    current_size = 0

    while chunk := await file.read(1024 * 1024):

        current_size += len(chunk)

        if current_size > MAX_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File too large"
            )

    # ⭐ Reset the pointer
    await file.seek(0)

    extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{extension}"

    # 5. Save file
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Now save
    with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": unique_filename,
        "path": file_path,
    }