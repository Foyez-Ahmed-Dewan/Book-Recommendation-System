from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class AuthResponse(BaseModel):
    message: str
    access_token: str | None = None
    token_type: str | None = None