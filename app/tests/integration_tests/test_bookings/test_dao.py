from datetime import date

import pytest
from httpx import AsyncClient

from app.bookings.dao import BookingDAO


async def test_and_get_booking():
    new_booking = await BookingDAO.add(
        user_id=2,
        pool_id=2,
        time_from=date(2023, 7, 10),
        time_to=date(2023, 7, 24),
    )

    assert new_booking.user_id == 2
    assert new_booking.pool_id == 2

    new_booking = await BookingDAO.find_one_or_none(id=new_booking.id)

    assert new_booking is not None


@pytest.mark.parametrize(
    "user_id,pool_id",
    [
        (2, 2),
        (2, 3),
        (1, 4),
        (1, 4),
    ],
)
async def test_booking_crud(user_id: int, pool_id: int, get_async_client: AsyncClient):
    new_booking = await BookingDAO.add(
        user_id=user_id,
        pool_id=pool_id,
        time_from=date(2023, 11, 25),
        time_to=date(2023, 12, 21),
    )
    assert new_booking.user_id == user_id
    assert new_booking.room_id == pool_id

    added_booking = await BookingDAO.find_one_or_none(id=new_booking.id)
    assert added_booking is not None

    await BookingDAO.delete(id=added_booking.id, user_id=user_id)
    deleted_booking = await BookingDAO.find_one_or_none(id=added_booking.id)
    assert deleted_booking is None
