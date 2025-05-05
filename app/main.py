# app/main.py
"""Module starts the application and initializes database if necessary"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import reservation, user, equipment
from app.db import init_database

@asynccontextmanager
async def lifespan (app: FastAPI):
    init_database () # initialize database on application start
    yield

app = FastAPI (
    lifespan = lifespan, # used for initialising database
    title = "Equipment reservation system",
    description = "A simple equipment reservation system for the time of use based on the FastAPI framework.",
    version = "0.0.1",
    contact = {
        "name": "Vladislav Kiselev",
        "email": "example@example.example",
    },
    license_info = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

app.include_router (reservation.router)
app.include_router (user.router)
app.include_router (equipment.router)
