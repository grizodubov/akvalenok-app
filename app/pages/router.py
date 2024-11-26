from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.bookings.router import add_booking, get_bookings
from app.spaces.pools.router import get_pools_by_time
from app.spaces.router import get_space_by_id, get_spaces_by_location_and_time
from app.utils import format_number_thousand_separator, get_month_days

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.get("/spaces/{location}", response_class=HTMLResponse)
async def get_hotels_page(
        request: Request,
        location: str,
        start_datetime: datetime,
        end_datetime: datetime,
        hotels=Depends(get_spaces_by_location_and_time),
):
    dates = get_month_days()
    if start_datetime > end_datetime:
        end_datetime, start_datetime = start_datetime, end_datetime
    # Автоматически ставим дату заезда позже текущей даты
    start_datetime = max(datetime.today().date(), start_datetime)
    # Автоматически ставим дату выезда не позже, чем через 180 дней
    end_datetime = min((datetime.today() + timedelta(days=180)).date(), end_datetime)
    return templates.TemplateResponse(
        "hotels_and_rooms/hotels.html",
        {
            "request": request,
            "hotels": hotels,
            "location": location,
            "end_datetime": end_datetime.strftime("%Y-%m-%d"),
            "start_datetime": start_datetime.strftime("%Y-%m-%d"),
            "dates": dates,
        },
    )


@router.get("/hotels/{hotel_id}/pools", response_class=HTMLResponse)
async def get_pools_page(
        request: Request,
        date_from: date,
        date_to: date,
        pools=Depends(get_pools_by_time),
        hotel=Depends(get_space_by_id),
):
    date_from_formatted = date_from.strftime("%d.%m.%Y")
    date_to_formatted = date_to.strftime("%d.%m.%Y")
    booking_length = (date_to - date_from).days
    return templates.TemplateResponse(
        "hotels_and_pools/pools.html",
        {
            "request": request,
            "hotel": hotel,
            "pools": pools,
            "date_from": date_from,
            "date_to": date_to,
            "booking_length": booking_length,
            "date_from_formatted": date_from_formatted,
            "date_to_formatted": date_to_formatted,
        },
    )


@router.post("/successful_booking", response_class=HTMLResponse)
async def get_successful_booking_page(
        request: Request,
        _=Depends(add_booking),
):
    return templates.TemplateResponse(
        "bookings/booking_successful.html", {"request": request}
    )


@router.get("/bookings", response_class=HTMLResponse)
async def get_bookings_page(
        request: Request,
        bookings=Depends(get_bookings),
):
    return templates.TemplateResponse(
        "bookings/bookings.html",
        {
            "request": request,
            "bookings": bookings,
            "format_number_thousand_separator": format_number_thousand_separator,
        },
    )
