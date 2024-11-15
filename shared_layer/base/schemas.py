from pydantic import BaseModel, Field


class DragonRequestModel(BaseModel):
    name: str
    breed: str
    danger_rating: int = Field(ge=1, le=10)
    description: str


class DragonResponseModel(DragonRequestModel):
    dragon_id: str
    created_at: str


class DragonInvalidRequestModel(BaseModel):
    breed: str
    danger_rating: int = Field(ge=1, le=10)
    description: str
