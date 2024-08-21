import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize(
    "location,date_from,date_to,status_code",
    [
        ("Алтай", "2023-11-24", "2023-11-20", status.HTTP_400_BAD_REQUEST),
        ("Алтай", "2023-11-24", "2024-01-08", status.HTTP_400_BAD_REQUEST),
        ("Алтай", "2023-11-24", "2023-12-24", status.HTTP_200_OK),
    ],
)
async def test_get_hotels_by_location_and_time(
        location: str,
        date_from: str,
        date_to: str,
        status_code: int,
        get_async_client: AsyncClient,
):
    response = await get_async_client.get(
        f"/spaces/{location}",
        params={
            "location": location,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code
