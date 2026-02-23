"""
Pydantic schemas for request / response validation.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ── Auth ────────────────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=120)
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=6)
    role: str = Field("FARMER", pattern="^(FARMER|BUYER|ADMIN)$")


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserPublic"


class UserPublic(BaseModel):
    id: str
    full_name: str
    email: str
    role: str

    class Config:
        from_attributes = True


# ── Posts ───────────────────────────────────────────────────────────
class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    body: str = Field(..., min_length=1)
    tags: str = Field("", max_length=500)
    image_url: Optional[str] = None


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    body: Optional[str] = Field(None, min_length=1)
    tags: Optional[str] = None
    image_url: Optional[str] = None


class PostOut(BaseModel):
    id: str
    title: str
    body: str
    tags: str
    image_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    author: UserPublic
    like_count: int = 0
    comment_count: int = 0
    liked_by_me: bool = False

    class Config:
        from_attributes = True


# ── Comments ────────────────────────────────────────────────────────
class CommentCreate(BaseModel):
    body: str = Field(..., min_length=1)


class CommentOut(BaseModel):
    id: str
    body: str
    created_at: datetime
    author: UserPublic

    class Config:
        from_attributes = True


# ── Likes ───────────────────────────────────────────────────────────
class LikeStatus(BaseModel):
    like_count: int
    liked_by_me: bool


# allow forward-ref in TokenResponse
TokenResponse.model_rebuild()
