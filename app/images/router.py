import shutil

from fastapi import APIRouter, UploadFile, status

from app.tasks.tasks import process_picture

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"],
)


@router.post("/spaces", status_code=status.HTTP_201_CREATED)
async def add_space_image(name: int, file: UploadFile) -> None:
    path = f"app/static/images/{name}.webp"
    with open(path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_picture.delay(path)
