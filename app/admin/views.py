from typing import cast

from sqladmin import ModelView

from app.bookings.models import Bookings
from app.spaces.models import Spaces
from app.spaces.pools.models import Pools
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [cast(str, Users.id), cast(str, Users.email)]
    column_details_exclude_list = [cast(str, Users.hashed_password)]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class SpacesAdmin(ModelView, model=Spaces):
    column_list = [c.name for c in Spaces.__table__.columns] + [
        Spaces.pool,
    ]
    name = "Помещение"
    name_plural = "Помещения"
    icon = "fa-solid fa-space"


class PoolsAdmin(ModelView, model=Pools):
    column_list = [c.name for c in Pools.__table__.columns] + [
        Pools.space,
        Pools.booking,
    ]
    name = "Бассейн"
    name_plural = "Бассейны"
    icon = "fa-solid fa-pool"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.columns] + [
        Bookings.user,
        Bookings.pool,
    ]
    name = "Занятие"
    name_plural = "Занятия"
    icon = "fa-solid fa-book"
