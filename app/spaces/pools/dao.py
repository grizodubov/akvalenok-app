from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.spaces.pools.models import Pools


class PoolDAO(BaseDAO):
    model = Pools

    @classmethod
    async def find_all(  # type: ignore[override]
            cls, space_id: int, time_from: date, time_to: date
    ):
        """
        WITH booked_pools AS (
            SELECT pool_id, COUNT(pool_id) AS pools_booked
            FROM bookings
            WHERE (time_from >= '2023-05-15' AND time_from <= '2023-06-20') OR
                  (time_from <= '2023-05-15' AND time_to > '2023-05-15')
            GROUP BY pool_id
        )
        SELECT
            -- все столбцы из pools,
            (quantity - COALESCE(pools_booked, 0)) AS pools_left FROM pools
        LEFT JOIN booked_pools ON booked_pools.pool_id = pools.id
        WHERE space_id = 1
        """
        booked_pools = cls.get_booked_pools(time_from, time_to)

        get_pools = (
            select(
                Pools.__table__.columns,
                (Pools.price * (time_to - time_from).days).label("total_cost"),
                (Pools.quantity - func.coalesce(booked_pools.c.pools_booked, 0)).label(
                    "pools_left"
                ),
            )
            .join(booked_pools, booked_pools.c.pool_id == Pools.id, isouter=True)
            .where(Pools.space_id == space_id)
        )
        async with async_session_maker() as session:
            pools = await session.execute(get_pools)
            return pools.mappings().all()

    @classmethod
    def get_booked_pools(cls, time_from: date, time_to: date):
        booked_pools = (
            select(Bookings.pool_id, func.count(Bookings.pool_id).label("pools_booked"))
            .select_from(Bookings)
            .where(
                or_(
                    and_(
                        Bookings.time_from >= time_from,
                        Bookings.time_from <= time_to,
                        ),
                    and_(
                        Bookings.time_from <= time_from,
                        Bookings.time_to > time_from,
                        ),
                ),
            )
            .group_by(Bookings.pool_id)
            .cte("booked_pools")
        )
        return booked_pools
