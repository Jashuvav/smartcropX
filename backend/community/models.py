"""
SQLAlchemy ORM models for Users, Posts, Comments, Likes, Bookmarks.
"""
import uuid
import datetime
from sqlalchemy import (
    Column, String, Text, Integer, Float, DateTime, ForeignKey,
    UniqueConstraint, Enum as SAEnum,
)
from sqlalchemy.orm import relationship
from .database import Base
import enum


# ── helpers ─────────────────────────────────────────────────────────
def _uuid() -> str:
    return uuid.uuid4().hex


def _now():
    return datetime.datetime.utcnow()


# ── enums ───────────────────────────────────────────────────────────
class Role(str, enum.Enum):
    FARMER = "FARMER"
    AGRONOMIST = "AGRONOMIST"
    ADMIN = "ADMIN"


# ── User ────────────────────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id = Column(String(32), primary_key=True, default=_uuid)
    full_name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SAEnum(Role), default=Role.FARMER, nullable=False)
    created_at = Column(DateTime, default=_now)

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")


# ── Post ────────────────────────────────────────────────────────────
class Post(Base):
    __tablename__ = "posts"

    id = Column(String(32), primary_key=True, default=_uuid)
    author_id = Column(String(32), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(300), nullable=False)
    body = Column(Text, nullable=False)
    tags = Column(String(500), default="")          # comma-separated
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=_now)
    updated_at = Column(DateTime, default=_now, onupdate=_now)

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="post", cascade="all, delete-orphan")


# ── Comment ─────────────────────────────────────────────────────────
class Comment(Base):
    __tablename__ = "comments"

    id = Column(String(32), primary_key=True, default=_uuid)
    post_id = Column(String(32), ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(String(32), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=_now)

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")


# ── Like ────────────────────────────────────────────────────────────
class Like(Base):
    __tablename__ = "likes"

    id = Column(String(32), primary_key=True, default=_uuid)
    post_id = Column(String(32), ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(32), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=_now)

    __table_args__ = (UniqueConstraint("post_id", "user_id", name="uq_like_post_user"),)

    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")


# ── Bookmark ────────────────────────────────────────────────────────
class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(String(32), primary_key=True, default=_uuid)
    post_id = Column(String(32), ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(32), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=_now)

    __table_args__ = (UniqueConstraint("post_id", "user_id", name="uq_bookmark_post_user"),)

    post = relationship("Post", back_populates="bookmarks")
    user = relationship("User", back_populates="bookmarks")
