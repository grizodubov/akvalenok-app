from datetime import datetime, timezone

from fastapi import Request, Depends
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import TokenExpiredException, IncorrectTokenFormatException, TokenAbsentException, \
    UserIsNotPresentException, IncorrectUserRoleException
from app.users.dao import UsersDAO
from app.users.models import Users


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    # if (not expire) or (datetime.now(timezone.utc) > datetime.fromisoformat(expire)):
    # if (not expire) or (int(expire) < int(datetime.now(timezone.utc).timestamp())):
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user


async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    # if not current_user.is_admin:
    if not current_user.role != "admin":
        raise IncorrectUserRoleException
    return current_user
