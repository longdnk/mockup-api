from pydantic import BaseModel, Field, validator
from typing import Optional


class UserEntity(BaseModel):
    id: str
    name: str
    address: str
    age: int


class User(BaseModel):
    id: Optional[str] = Field(default=None)
    name: str = Field(..., min_length=1, max_length=255)
    address: str = Field(..., min_length=5, max_length=255)
    age: int = Field(..., ge=10, le=100)

    # Validator để đảm bảo các ràng buộc
    @validator("name")
    def validate_name(cls, value):
        if len(value) < 1 or len(value) > 255:
            raise ValueError("Name must be between 1 and 255 characters.")
        return value

    @validator("address")
    def validate_address(cls, value):
        if len(value) < 5 or len(value) > 255:
            raise ValueError("Address must be between 5 and 255 characters.")
        return value

    @validator("age")
    def validate_age(cls, value):
        if value < 10 or value > 100:
            raise ValueError("Age must be between 10 and 100.")
        return value
