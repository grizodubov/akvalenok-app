import pytest
from pydantic import EmailStr

from app.users.dao import UserDAO


@pytest.mark.parametrize(
    "user_id,email,exists",
    [
        (1, "test@test.com", True),
        (2, "artem@example.com", True),
        (3, "noone@test.com", False),
    ],
)
async def test_find_user_by_id(user_id: int, email: EmailStr, exists: bool):
    user = await UserDAO.find_one_or_none(id=user_id)

    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
