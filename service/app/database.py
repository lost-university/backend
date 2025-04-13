import os
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

load_dotenv()

postgres_url = f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
print(os.getenv('POSTGRES_PASSWORD'))
engine = create_engine(postgres_url, echo=True)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, any, None]:
    with Session(engine) as session:
        yield session
