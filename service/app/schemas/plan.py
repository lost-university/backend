import uuid
from datetime import datetime

from sqlmodel import SQLModel


class PlanRead(SQLModel):
    id: uuid.UUID
    group_version_id: uuid.UUID
    name: str
    content: str
    public_slug: str
    is_favorite: bool
    created_at: datetime
    user_id: uuid.UUID
