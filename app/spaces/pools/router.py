from datetime import date, datetime, timedelta

from fastapi import APIRouter, Query

from app.spaces.pools.dao import PoolDAO
from app.spaces.pools.schemas import SPoolInfo

router = APIRouter()


@router.get("/{space_id}/pools")
async def get_pools_by_time(
        space_id: int,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(
            ..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"
        ),
) -> list[SPoolInfo]:
    pools = await PoolDAO.find_all(space_id, date_from, date_to)
    return pools
