import uuid
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy_utils import EmailType, PhoneNumberType
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base

if TYPE_CHECKING:
    from app.bookings.models import Bookings

class Users(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(EmailType, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)

    role: Mapped[str] = mapped_column(nullable=False, default="client")
    # ФИО Клиента
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    middle_name: Mapped[str] = mapped_column(nullable=True)
    # тел
    phone_number: Mapped[str] = mapped_column(PhoneNumberType, nullable=True, unique=True)
    # Любимый тренер 1
    # Любимый тренер 2

    # ИФ ребенок 1 дата рождения
    # Мед справка до...
    # ИФ ребенок 2 дата рождения
    # Мед справка до...
    # ИФ ребенок 3 дата рождения
    # Мед справка до...

    # Проблемный клиент
    is_problem_client = mapped_column(Boolean, default=False)
    # Контрольная дата
    # Откуда пришёл?
    # Кто привёл?
    # Причина ухода

    # Воронка продаж С переключением статуса

    # Действующий абонемент
    # Дата активации / окончания абонемента.
    # Осталось занятий
    # Не назначенные занятия

    # + Добавить абонемент --> # Чек бокс (выбор)
    # Сумма к оплате
    # Наличные/переводом
    # Архив приобретённых абонементов

    # Дополнительные услуги --> # Чек бокс (выбор)
    # Сумма к оплате
    # Наличные/переводом
    # Архив приобретённых дополнительных услуг

    # Журнал записей комментариев по клиенту.
    # Лог добавления абонементов,
    # покупки дополнительных услуг,
    # комментариев менеджеров с датами и временем записи.

    # date_joined: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now(tz=timezone.utc))
    # register_date = Column(Date, nullable=False, default=func.current_date())
    # refresh_token: Mapped[str] = mapped_column(nullable=True)
    # is_active: Mapped[bool] = mapped_column(default=True)
    # is_superuser: Mapped[bool] = mapped_column(default=False)
    # is_confirmed = Column(Boolean, server_default="FALSE", nullable=False)

    # booking = relationship("Bookings", back_populates="user")
    booking: Mapped[List["Bookings"]] = relationship(back_populates="user")

    def __str__(self):
        return f"Пользователь {self.email}"
