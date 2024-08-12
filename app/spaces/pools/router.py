from datetime import date, datetime, timedelta

from fastapi import APIRouter, Query

from app.spaces.pools.dao import PoolDAO
from app.spaces.pools.schemas import SPoolInfo

router = APIRouter()


@router.get("/{space_id}/pools")
async def get_pools_by_time(
        space_id: int,
        time_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        time_to: date = Query(
            ..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"
        ),
) -> list[SPoolInfo]:
    pools = await PoolDAO.find_all(space_id, time_from, time_to)
    return pools
