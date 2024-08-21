from typing import Optional

from fastapi import APIRouter, Depends, status
from pydantic import TypeAdapter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import (
    SBooking,
    SNewBooking,
)
from app.exceptions import PoolCannotBeBookedException
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Занятия"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_booking(
        booking: SNewBooking,
        user: Users = Depends(get_current_user),
) -> Optional[SBooking]:
    booking_to_add = await BookingDAO.add(
        user.id,
        booking.pool_id,
        booking.date_from,
        # booking.time_from,
        booking.date_to,
        # booking.time_to,
    )
    if not booking_to_add:
        raise PoolCannotBeBookedException
    booking_dict = TypeAdapter(SNewBooking).validate_python(booking_to_add).model_dump()
    send_booking_confirmation_email.delay(booking_dict, str(user.email))
    return booking_to_add


@router.delete("/{booking_id}")
async def delete_booking(
        booking_id: int, user: Users = Depends(get_current_user)
) -> None:
    await BookingDAO.delete(id=booking_id, user_id=user.id)
