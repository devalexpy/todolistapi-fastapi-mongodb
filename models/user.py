# Python
from bson import ObjectId
from bson.objectid import ObjectId
from typing import Optional
# Pydantic
from pydantic import BaseModel, Field, EmailStr


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


class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=5,
        max_length=20,
    )
    email: str = EmailStr(...)


class UserSingUp(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=20
    )

    class Config:
        schema_extra = {
            "example": {
                "username": "new_user",
                "email": "new_email@example.com",
                "password": "new_password",
            }
        }


class UserLogin(BaseModel):
    username: str = Field(
        ...,
        min_length=5,
        max_length=20,
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=20
    )

    class Config:
        schema_extra = {
            "example": {
                "username": "new_user",
                "password": "new_password",
            }
        }


class UserUpdateBasicInfo(BaseModel):
    username: Optional[str] = Field(
        min_length=5,
        max_length=20,
    )

    email: Optional[str] = EmailStr()

    class Config:
        schema_extra = {
            "example": {
                "(username or email)": "new_value",
            }
        }


class UserUpdatePassword(BaseModel):
    old_password: str = Field(
        ...,
        min_length=8,
        max_length=20
    )
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=20
    )

    class Config:
        schema_extra = {
            "example": {
                "old_password": "old_password",
                "new_password": "new_password",
            }
        }


class UserOut(UserBase):
    user_id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "5e8f8f8f8f8f8f8f8f8f8f8f",
                "username": "new_user",
                "email": "new_email@example.com"
            }
        }
