import uuid
from datetime import datetime

from sqlalchemy import select, and_, or_, func, insert

from app.dao.base import BaseDAO
from app.bookings.models import Bookings
from app.database import async_session_maker
from app.spaces.pools.models import Pools
from app.logger import logger  # type: ignore


class BookingDAO(BaseDAO):
    models = Bookings

    @classmethod
    async def find_all_with_images(cls, user_id: uuid.UUID):
        async with async_session_maker() as session:
            query = (
                select(
                    # __table__.columns нужен для отсутствия вложенности в ответе Алхимии
                    Bookings.__table__.columns,
                    Pools.__table__.columns,
                )
                .join(Pools, Pools.id == Bookings.pool_id, isouter=True)
                .where(Bookings.user_id == user_id)
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(
            cls,
            user_id: uuid.UUID,
            pool_id: int,
            start_datetime: datetime,
            end_datetime: datetime,
            lessons_in_a_row: int
    ):
        """
            WITH booked_pools AS (
                SELECT * FROM bookings
                WHERE pool_id = 1
                AND (start_datetime >= '2023-05-15' AND start_datetime <= '2023-06-20')
                OR (start_datetime <= '2023-05-15' AND end_datetime > '2023-05-15')
            )
            SELECT pools.quantity - COUNT(booked_pools.pool_id) FROM pools
                LEFT JOIN booked_pools ON booked_pools.pool_id = pools.id
            WHERE pools.id = 1
            GROUP BY pools.quantity, booked_pools.pool_id
        """
        async with async_session_maker() as session:
            booked_pools = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.pool_id == pool_id,
                        or_(
                            and_(
                                Bookings.start_datetime >= start_datetime,
                                Bookings.end_datetime <= end_datetime
                            ),
                            and_(
                                Bookings.start_datetime <= start_datetime,
                                Bookings.end_datetime > start_datetime
                            ),
                        )
                    )
                ).cte("booked_pools")
            )

            """
                SELECT pools.quantity - COUNT(booked_pools.pool_id) FROM pools
                LEFT JOIN booked_pools ON booked_pools.pool_id = pools.id
                WHERE pools.id = 1
                GROUP BY pools.quantity, booked_pools.pool_id
            """

            get_pools_left = (
                select(
                    (Pools.quantity - func.count(booked_pools.c.pool_id)).label("pools_left")
                )
                .select_from(Pools)
                .join(
                    booked_pools, booked_pools.c.pool_id == Pools.id, isouter=True
                )
                .where(Pools.id == pool_id)
                .group_by(Pools.quantity, booked_pools.c.pool_id)
            )
            # print(get_pools_left.compile(engine, compile_kwargs={"literal_binds": True}))

            query = await session.execute(get_pools_left)
            pools_left: int = query.mappings().one().pools_left

            # print(pools_left)

            if pools_left > 0:
                # get_price = select(Pools.price).where(Pools.id == pool_id).cte("get_price")
                get_price = select(Pools.price).filter_by(id=pool_id)
                query = await session.execute(get_price)
                price: int = query.mappings().one().price
                add_booking = (
                    insert(Bookings)
                    .values(
                        pool_id=pool_id,
                        user_id=user_id,
                        start_datetime=start_datetime,
                        end_datetime=end_datetime,
                        price=price,
                    )
                    .returning(
                        Bookings.id,
                        Bookings.user_id,
                        Bookings.pool_id,
                        Bookings.start_datetime,
                        Bookings.end_datetime,
                    )
                )

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.mappings().one()
            else:
                return None
