from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from .database import engine
from .middlewares.auth_middleware import auth_dependency
from .models.plan import Plan

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "OSTDependency backend"}


@app.get("/plans", dependencies=[Depends(auth_dependency)])
async def get_plans(request: Request) -> dict[str, list[Plan]]:
    with Session(engine) as session:
        statement = select(Plan).where(Plan.user_id == request.state.user.id)
        return {"plans": session.exec(statement).all()}
