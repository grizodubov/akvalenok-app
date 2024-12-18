import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, SpacesAdmin, PoolsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.spaces.router import router as router_spaces
from app.images.router import router as router_images
from app.importer.router import router as router_importer
from app.logger import logger
from app.pages.router import router as router_pages
from app.users.router import router_auth, router_users


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # before execute app
    print("start app")
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    # after execute app

    # if settings.MODE != "TEST":
    # Подключение Sentry для мониторинга ошибок. Лучше выключать на период локального тестирования
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )


app = FastAPI(
    title="Запись в бассейн",
    version="0.1.0",
    root_path="/api",
    lifespan=lifespan
)


# @app.get("/sentry-debug")
# async def trigger_error():
#     """Simulate an error to test Sentry."""
#     division_by_zero = 1 / 0


app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_spaces)
app.include_router(router_bookings)

app.include_router(router_images)
app.include_router(router_importer)

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
app = VersionedFastAPI(app,
   version_format='{major}',
   prefix_format='/api/v{major}',
   description='Greet users with a nice message',
   lifespan=lifespan
)
app.include_router(router_pages)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(SpacesAdmin)
admin.add_view(PoolsAdmin)
admin.add_view(BookingsAdmin)

app.mount("/static", StaticFiles(directory="app/static"), "static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()  # засекаем время
    response = await call_next(request)  # обработка запроса и получение ответа
    process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    logger.info(
        "Request handling time",
        extra={"process_time": round(process_time, 4)},
    )
    response.headers["X-Process-Time"] = str(process_time)
    return response  # возврат ответа
