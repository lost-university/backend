import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import plan_router


load_dotenv()
app = FastAPI()

origins = os.getenv("AUTHORIZED_PARTIES").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plan_router.router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "OSTDependency backend"}
