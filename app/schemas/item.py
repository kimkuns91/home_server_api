from datetime import datetime

from app.schemas.base import BaseSchema


class ItemBase(BaseSchema):
    name: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseSchema):
    name: str | None = None
    description: str | None = None


class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
