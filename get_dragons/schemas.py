from pydantic import BaseModel, Field


class GetDragonsResponseModel(BaseModel):
    name: str
    breed: str
    description: str
    danger_rating: int = Field(ge=1, le=10)
