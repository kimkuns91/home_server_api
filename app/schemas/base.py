from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ResponseBase(BaseSchema):
    message: str = "success"


class PaginatedResponse(BaseSchema):
    total: int
    page: int
    size: int
