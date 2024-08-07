import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize(
    "pool_id,time_from,time_to,booked_pools,status_code",
    [
        (4, "2030-05-01", "2030-05-15", 3, status.HTTP_201_CREATED),
        (4, "2030-05-02", "2030-05-16", 4, status.HTTP_201_CREATED),
        (4, "2030-05-03", "2030-05-17", 5, status.HTTP_201_CREATED),
        (4, "2030-05-04", "2030-05-18", 6, status.HTTP_201_CREATED),
        (4, "2030-05-05", "2030-05-19", 7, status.HTTP_201_CREATED),
        (4, "2030-05-06", "2030-05-20", 8, status.HTTP_201_CREATED),
        (4, "2030-05-07", "2030-05-21", 9, status.HTTP_201_CREATED),
        (4, "2030-05-08", "2030-05-22", 10, status.HTTP_201_CREATED),
        (4, "2030-05-09", "2030-05-23", 10, status.HTTP_409_CONFLICT),
        (4, "2030-05-10", "2030-05-24", 10, status.HTTP_409_CONFLICT),
    ],
)
async def test_add_and_get_booking(
        pool_id: int,
        time_from: str,
        time_to: str,
        booked_pools: int,
        status_code: int,
        get_authenticated_async_client: AsyncClient,
):
    response = await get_authenticated_async_client.post(
        "/bookings",
        json={
            "room_id": pool_id,
            "date_from": time_from,
            "date_to": time_to,
        },
    )
    assert response.status_code == status_code

    response = await get_authenticated_async_client.get("/bookings")
    assert len(response.json()) == booked_pools


async def test_get_and_delete_bookings(get_authenticated_async_client: AsyncClient):
    response = await get_authenticated_async_client.get("/bookings")
    bookings = [booking["id"] for booking in response.json()]
    for booking in bookings:
        await get_authenticated_async_client.delete(f"/bookings/{booking}")
    response = await get_authenticated_async_client.get("/bookings")
    assert len(response.json()) == 0
