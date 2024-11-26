from fastapi import APIRouter, Depends, status
from pydantic import TypeAdapter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import (
    SBooking,
    SBookingInfo,
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
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingInfo]:
    return await BookingDAO.find_all_with_images(user_id=user.id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_booking(
        booking: SNewBooking,
        user: Users = Depends(get_current_user)
) -> SNewBooking:
    booking_to_add = await BookingDAO.add(
        user.id,
        booking.pool_id,
        booking.start_datetime,
        booking.end_datetime,
        booking.lessons_in_a_row
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
