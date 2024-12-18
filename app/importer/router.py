import codecs
import csv
from typing import Literal

from fastapi import APIRouter, Depends, UploadFile

from app.exceptions import CannotAddDataToDatabaseException, CannotProcessCSVException
from app.importer.utils import TABLE_MODEL_MAP, convert_csv_to_postgres_format
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix="/import",
    tags=["Импорт данных в БД"],
)


@router.post(
    "/{table_name}",
    status_code=201,
    dependencies=[Depends(get_current_user)],
)
async def import_data_to_table(
        file: UploadFile,
        table_name: Literal["spaces", "pools", "bookings"],
):
    model_dao = TABLE_MODEL_MAP[table_name]
    csv_reader = csv.DictReader(codecs.iterdecode(file.file, "utf-8"), delimiter=";")
    data = convert_csv_to_postgres_format(csv_reader)
    file.file.close()
    if not data:
        raise CannotProcessCSVException
    added_data = await model_dao.add_bulk(data)
    if not added_data:
        raise CannotAddDataToDatabaseException
