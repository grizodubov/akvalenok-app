from datetime import date, datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache
from pydantic import TypeAdapter

from app.exceptions import CannotBookSpaceForLongPeriod, DateFromCannotBeAfterDateTo
from app.spaces.dao import SpacesDAO
from app.spaces.pools.router import router as router_pool
from app.spaces.schemas import SSpace

router = APIRouter(
    prefix="/spaces",
    tags=["Помещения"],
)
router.include_router(router_pool)


@router.get("/{location}")
@cache(expire=30)
async def get_spaces_by_location_and_time(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(
            ..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"
        ),
) -> list[SSpace]:
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31:
        raise CannotBookSpaceForLongPeriod
    spaces = await SpacesDAO.find_all(location, date_from, date_to)
    spaces_parsed = TypeAdapter(list[SSpace]).validate_python(spaces)
    return spaces_parsed


@router.get("/id/{space_id}")
async def get_space_by_id(
        space_id: int,
) -> Optional[SSpace]:
    return await SpacesDAO.find_one_or_none(id=space_id)
