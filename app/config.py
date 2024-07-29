# Как верно подметил один из учеников, лучше не создавать уродливую функцию
# get_database_url внутри класса Settings для получения адреса базы данных, а
# пользоваться переменной DATABASE_URL, что мы написали в файле database.py

from pydantic_settings import BaseSettings
# from pydantic import root_validator
from pydantic import PostgresDsn


# №1 создаем класс с настройками, назовем Settings и наследуем от pydantic. Валидируем их типы.
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # @root_validator
    # def get_database_url(cls, v):
    #     v["DATABASE_URL"] = f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PASS']}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
    #     return v
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        """ URL для подключения (DSN)"""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    SECRET_KEY: str
    ALGORITHM: str

    # №2 укажем pydantic из какого файла забирать настройки
    class Config:
        env_file = ".env"


# №3 Создадим экземпляр класса
settings = Settings()

# №4
# settings.DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"


# print(settings.DB_HOST)
# print(settings.DATABASE_URL)