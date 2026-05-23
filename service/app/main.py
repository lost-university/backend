import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_db_and_tables
from .routers import config_router, plan_router

load_dotenv()


async def initialize_database() -> None:
    create_db_and_tables()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await initialize_database()
    yield


app = FastAPI(lifespan=lifespan)

origins = os.getenv("AUTHORIZED_PARTIES").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(config_router.router)
app.include_router(plan_router.router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "OSTDependency backend"}
