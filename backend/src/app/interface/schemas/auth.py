from pydantic import BaseModel, EmailStr, Field, field_validator


class PasswordStrengthMixin:

    @field_validator("password")
    def password_strength(cls, v):

        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        
        return v 


class RegisterUser(PasswordStrengthMixin, BaseModel):

    email: EmailStr
    username: str = Field(min_length=8)
    password: str = Field(min_length=8)


class LoginUser(PasswordStrengthMixin, BaseModel):

    email: EmailStr
    password: str = Field(min_length=8)
