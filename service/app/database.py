import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()

postgres_url = f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(postgres_url, echo=True)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
