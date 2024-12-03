from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.config import settings
from app.users.auth import authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.users.schemas import SUserAuth


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        # email, password = str(form["username"]), str(form["password"])
            #However, I realized that using ** to unpack the dictionary into keyword arguments is a more idiomatic way to create a Pydantic model instance, and it's not necessary to use model_validate explicitly.
            #try:
            #   user_data = SUserAuth(**{"email": form["username"], "password": form["password"]})
            # except ValidationError as e:
            #   # Handle validation error
            #   return False
        user_data = SUserAuth(**{"email": form["username"], "password": form["password"]})
        email, password = user_data.email, user_data.password

        user = await authenticate_user(email, password)
        if user:
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        user = await get_current_user(token)
        if not user:
            return False
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
