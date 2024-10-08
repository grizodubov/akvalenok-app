from fastapi import APIRouter, Depends
from fastapi import Response
from pydantic import TypeAdapter

from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.models import Users
from app.users.schemas import SUserAuth, SUser

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.post("/register")
async def register_user(user_data: SUserAuth) -> None:
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth) -> dict[str, str]:
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}  # return access_token


@router.post("/logout")
async def logout_user(response: Response) -> dict[str, str]:
    response.delete_cookie("booking_access_token")
    return {"message": "Successfully logged out"}


@router.get("/me")
async def get_current_user(
        current_user: Users = Depends(get_current_user)
) -> SUser:
    return SUser.model_validate(current_user)


@router.get("/all")
async def get_all_users(
        current_user: Users = Depends(get_current_admin_user)
) -> list[SUser]:
    res = await UsersDAO.find_all()
    res = [TypeAdapter(SUser).validate_python(user).model_dump() for user in res]
    return res
