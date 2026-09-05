from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.exceptions import PasswordNotStrenght


class PasswordStrengthMixin:

    @field_validator("password")
    def password_strength(cls, v):

        if not any(char.isdigit() for char in v):
            raise PasswordNotStrenght("Password must contain at least one digit")
        
        if not any(char.isupper() for char in v):
            raise PasswordNotStrenght("Password must contain at least one uppercase letter")
        
        if not any(char.islower() for char in v):
            raise PasswordNotStrenght("Password must contain at least one lowercase letter")
        
        return v 


class RegisterUser(PasswordStrengthMixin, BaseModel):

    email: EmailStr
    username: str = Field(min_length=8)
    password: str = Field(min_length=8)


class LoginUser(PasswordStrengthMixin, BaseModel):

    email: EmailStr
    password: str = Field(min_length=8)


class PasswordBody(PasswordStrengthMixin, BaseModel):
    password: str = Field(min_length=8)


class EmailBody(BaseModel):
    email: EmailStr
