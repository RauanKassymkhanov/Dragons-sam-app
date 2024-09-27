from pydantic import BaseModel, Field


class GetDragonsResponseModel(BaseModel):
    dragon_id: str
    name: str
    breed: str
    description: str
    danger_rating: int = Field(ge=1, le=10)
    created_at: str
