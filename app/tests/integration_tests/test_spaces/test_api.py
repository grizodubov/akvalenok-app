import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize(
    "location,time_from,time_to,status_code",
    [
        ("Алтай", "2023-11-24", "2023-11-20", status.HTTP_400_BAD_REQUEST),
        ("Алтай", "2023-11-24", "2024-01-08", status.HTTP_400_BAD_REQUEST),
        ("Алтай", "2023-11-24", "2023-12-24", status.HTTP_200_OK),
    ],
)
async def test_get_hotels_by_location_and_time(
        location: str,
        time_from: str,
        time_to: str,
        status_code: int,
        get_async_client: AsyncClient,
):
    response = await get_async_client.get(
        f"/spaces/{location}",
        params={
            "location": location,
            "time_from": time_from,
            "time_to": time_to,
        },
    )

    assert response.status_code == status_code
