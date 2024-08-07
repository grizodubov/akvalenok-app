import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("kot@pes.com", "kotopes", status.HTTP_200_OK),
        ("kot@pes.com", "kot0pes", status.HTTP_409_CONFLICT),
        ("pes@kot.com", "pesokot", status.HTTP_200_OK),
        ("abcd", "pesokot", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_register_user(
        email: str, password: str, status_code: int, get_async_client: AsyncClient
):
    response = await get_async_client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("test@test.com", "test", status.HTTP_200_OK),
        ("artem@example.com", "artem", status.HTTP_200_OK),
        ("wrong@person.com", "artem", status.HTTP_401_UNAUTHORIZED),
    ],
)
async def test_login_user(
        email: str, password: str, status_code: int, get_async_client: AsyncClient
):
    response = await get_async_client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )

    assert response.status_code == status_code
