from datetime import date

from sqlalchemy import and_, func, select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.spaces.models import Spaces
from app.spaces.pools.dao import PoolDAO
from app.spaces.pools.models import Pools


class SpacesDAO(BaseDAO):
    model = Spaces

    @classmethod
    async def find_all(  # type: ignore[override]
            cls, location: str, start_datetime: date, end_datetime: date
    ):
        """
        WITH booked_pools AS (
            SELECT pool_id, COUNT(pool_id) AS pools_booked
            FROM bookings
            WHERE
                (start_datetime >= '2023-05-15' AND start_datetime <= '2023-06-20') OR
                (start_datetime <= '2023-05-15' AND end_datetime > '2023-05-15')
            GROUP BY pool_id
        ),
        booked_spaces AS (
            SELECT space_id, SUM(pools.quantity - COALESCE(pools_booked, 0))
            AS pools_left
            FROM pools
            LEFT JOIN booked_pools ON booked_pools.pool_id = pools.id
            GROUP BY space_id
        )
        SELECT * FROM spaces
        LEFT JOIN booked_spaces ON booked_spaces.space_id = spaces.id
        WHERE pools_left > 0 AND location LIKE '%Алтай%';
        """
        booked_pools = PoolDAO.get_booked_pools(start_datetime, end_datetime)

        booked_spaces = (
            select(
                Pools.space_id,
                func.sum(
                    Pools.quantity - func.coalesce(booked_pools.c.pools_booked, 0)
                ).label("pools_left"),
            )
            .select_from(Pools)
            .join(booked_pools, booked_pools.c.pool_id == Pools.id, isouter=True)
            .group_by(Pools.space_id)
            .cte("booked_spaces")
        )

        get_spaces_with_pools = (
            select(
                Spaces.__table__.columns,
                booked_spaces.c.pools_left,
            )
            .join(booked_spaces, booked_spaces.c.space_id == Spaces.id, isouter=True)
            .where(
                and_(
                    booked_spaces.c.pools_left > 0,
                    Spaces.location.like(f"%{location}%"),
                    )
            )
        )
        async with async_session_maker() as session:
            spaces_with_pools = await session.execute(get_spaces_with_pools)
            return spaces_with_pools.mappings().all()
