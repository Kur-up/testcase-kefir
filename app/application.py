from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .api import router_auth
from .api import router_users
from .api import router_admin

from .db import queries_users
from .db import queries_cities

title = "Kefir Python Junior Test"
description = """
# testcase-kefir #
The project was created to pass a test assignment<br>
for the role of a developer in the Kefir company.
<br><br>
Technologies and stack: 
* FastAPI
* PostgresSQL
* Alembic
* SQLAlchemy
* Docker
* passlib
"""

app = FastAPI(
    title=title,
    description=description,
    version="0.1.0",
    contact={
        "name": "Lev Kurapov",
        "url": "https://github.com/Kur-up/testcase-kefir",
        "email": "kurup.performance@gmail.com",
    },
)

app.include_router(router_auth)
app.include_router(router_users, prefix="/users")
app.include_router(router_admin, prefix="/private")


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def startup():
    await queries_users.add_super_user()
    await queries_cities.add_default_cities()


@app.exception_handler(Exception)
async def server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Что-то пошло не так, мы уже исправляем эту ошибку"},
    )


@app.get("/health", include_in_schema=False)
async def health():
    """Необходимо для деплоя, проверяет жив ли контейнер с сервисом"""
    return JSONResponse(status_code=200, content="OK")
