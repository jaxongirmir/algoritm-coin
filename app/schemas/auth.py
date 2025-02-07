from enum import Enum
from uuid import UUID, uuid4
from datetime import date
from typing import Annotated, List, Optional

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    ConfigDict,
    SecretStr,
    StringConstraints,
    constr,
)

from ..service.password import PasswordMixin

config = ConfigDict(from_attributes=True)


class Login(BaseModel):
    model_config = config
    email: EmailStr = Field(
        title="Teacher’s email",
        description="Teacher’s email address",
        examples=["example@example.com"],
    )
    password: SecretStr = Field(
        title="Teacher’s password",
        description="Teacher’s password",
        examples=["@SuperSecret"],
        min_length=6,
    )


class ForgotPassword(BaseModel):
    model_config = config
    email: EmailStr = Field(
        title="Teacher’s email",
        description="Teacher’s email address",
        examples=["example@example.com"],
    )


class ChangePassword(BaseModel, PasswordMixin):
    model_config = config
    old_password: SecretStr = Field(
        title="Teacher’s old password",
        description="Teacher’s old password",
        examples=["@SuperSecret"],
        min_length=6,
    )

    new_password: SecretStr = Field(
        title="Teacher’s new password",
        description="Teacher’s new password",
        examples=["@SuperSecret"],
        min_length=6,
    )
