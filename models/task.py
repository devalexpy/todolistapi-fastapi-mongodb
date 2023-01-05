from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Status(str, Enum):
    done = "done"
    pending = "pending"


class TaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=5,
        max_length=50
    )
    description: str = Field(
        ...,
        min_length=5,
        max_length=200
    )


class TaskCreate(TaskBase):
    status: Optional[Status] = Field(default=Status.pending)
    user_id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "My first task",
                "description": "This is my first task",
                "user_id": "60e1c1c1c1c1c1c1c1c1c1c1"
            }
        }


class TaskUpdate(TaskBase):
    title: Optional[str] = Field(
        None,
        min_length=5,
        max_length=50
    )
    description: Optional[str] = Field(
        None,
        min_length=5,
        max_length=200
    )

    class Config:
        schema_extra = {
            "example": {
                "(title or description)": "(content)",
            }
        }


class TaskOut(BaseModel):
    task_id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(
        ...,
        min_length=5,
        max_length=50
    )
    description: str = Field(
        ...,
        min_length=5,
        max_length=200
    )
    status: Status = Field(default=Status.pending)
    user_id: PyObjectId = Field(default_factory=PyObjectId, alias="user_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "60e1c1c1c1c1c1c1c1c1c1c1",
                "title": "My first task",
                "description": "This is my first task",
                "status": "pending",
                "user_id": "60e1c1c1c1c1c1c1c1c1c1c1"
            }
        }
