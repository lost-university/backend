import os
from collections.abc import Generator
from typing import Any

from dotenv import load_dotenv
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

postgres_url = f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine = create_engine(postgres_url, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)


def is_database_initialized() -> bool:
    table_names = SQLModel.metadata.tables
    if not table_names:
        return False

    inspector = inspect(engine)
    return all(inspector.has_table(table_name) for table_name in table_names)


def create_db_and_tables() -> None:
    if is_database_initialized():
        print("Database tables already exist!")
        return
    SQLModel.metadata.create_all(engine)
    print("Database tables created!")


def drop_tables() -> None:
    SQLModel.metadata.drop_all(engine)


def get_session() -> Generator[Session, Any]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
