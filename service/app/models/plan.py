import uuid
from datetime import datetime

from pydantic import NaiveDatetime
from sqlmodel import Field, SQLModel


class Plan(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    group_version_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(nullable=False)
    content: str
    public_slug: str | None
    bookmark: bool = Field(default=False)
    # naive like the existing `timestamp without time zone` column
    created_at: NaiveDatetime = Field(default_factory=datetime.now)
    user_id: uuid.UUID = Field(nullable=False, foreign_key="user.id")
