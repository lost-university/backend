import uuid
from datetime import datetime

from sqlmodel import SQLModel


class PlanRead(SQLModel):
    id: uuid.UUID
    group_version_id: uuid.UUID
    name: str
    content: str
    is_favorite: bool
    created_at: datetime
    user_id: uuid.UUID


class PlanCreate(SQLModel):
    group_version_id: uuid.UUID | None = None
    name: str
    content: str
    public_slug: str
    is_favorite: bool | None = None
    created_at: datetime | None = None
    user_id: uuid.UUID
