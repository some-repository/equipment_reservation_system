# app/main.py
from fastapi import FastAPI
from app.routes import actions
from app.db import init_database
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan (app: FastAPI):
    init_database () # initialise database on application start
    yield

app = FastAPI (
    lifespan = lifespan, # used for initialising database
    title = "Система управления доступом к оборудованию",
    description = "Система для бронирования оборудования на время использования, основанная на "
                "фреймворке FastAPI.",
    version = "0.0.1",
    contact = {
        "name": "Владислав Киселев",
        "email": "example@example.example",
    },
    license_info = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

app.include_router (actions.router)