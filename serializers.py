import re
from pydantic import field_serializer, field_validator
from sqlmodel import SQLModel, Field
from bcrypt import hashpw, gensalt


class UserSerializer(SQLModel):
    name: str = Field(nullable=False)
    email: str = Field(unique=True)

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        if re.match(r'^\w+@\w+\.\w+$', value):
            return value
        else:
            raise ValueError('Invalid email')
        

class UserCreateUpdateSerializer(UserSerializer):
    password: str = Field(nullable=False, min_length=8)

    @field_serializer('password')
    def serialize_password(value: str) -> str:
        hash_password = hashpw(value.encode(), gensalt())
        return hash_password.decode()


class AdvertisementSerializer(SQLModel):
    title: str = Field(nullable=False)
    description: str = Field()
    owner_id: int = Field(foreign_key = "user.id", nullable=False)