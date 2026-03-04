"""
Community REST API – FastAPI router.
Covers: auth (register/login), posts CRUD, comments, likes, image upload, seed data.
"""
import os
import uuid
import shutil
import logging
from typing import Optional, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from .database import get_db, Base, engine
from .models import User, Post, Comment, Like, Bookmark, Role
from .schemas import (
    RegisterRequest, LoginRequest, TokenResponse, UserPublic,
    PostCreate, PostUpdate, PostOut,
    CommentCreate, CommentOut,
    LikeStatus,
)
from .auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, require_auth, require_role,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/community", tags=["Community"])
auth_router = APIRouter(prefix="/api/auth", tags=["Auth"])

# ── ensure tables exist ─────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# Upload dir for community images
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "community_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ═════════════════════════════════════════════════════════════════════
#  AUTH
# ═════════════════════════════════════════════════════════════════════

@auth_router.post("/register", response_model=TokenResponse, status_code=201)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        full_name=req.full_name,
        email=req.email,
        hashed_password=hash_password(req.password),
        role=Role(req.role),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": user.id, "role": user.role.value})
    return TokenResponse(
        access_token=token,
        user=UserPublic(id=user.id, full_name=user.full_name, email=user.email, role=user.role.value),
    )


@auth_router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": user.id, "role": user.role.value})
    return TokenResponse(
        access_token=token,
        user=UserPublic(id=user.id, full_name=user.full_name, email=user.email, role=user.role.value),
    )


@auth_router.get("/me", response_model=UserPublic)
def get_me(user: User = Depends(require_auth)):
    return UserPublic(id=user.id, full_name=user.full_name, email=user.email, role=user.role.value)


# ═════════════════════════════════════════════════════════════════════
#  POSTS
# ═════════════════════════════════════════════════════════════════════

def _post_to_out(post: Post, db: Session, current_user: Optional[User] = None) -> dict:
    like_count = db.query(func.count(Like.id)).filter(Like.post_id == post.id).scalar()
    comment_count = db.query(func.count(Comment.id)).filter(Comment.post_id == post.id).scalar()
    liked_by_me = False
    if current_user:
        liked_by_me = db.query(Like).filter(Like.post_id == post.id, Like.user_id == current_user.id).first() is not None
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "tags": post.tags or "",
        "image_url": post.image_url,
        "created_at": post.created_at.isoformat() if post.created_at else None,
        "updated_at": post.updated_at.isoformat() if post.updated_at else None,
        "author": {
            "id": post.author.id,
            "full_name": post.author.full_name,
            "email": post.author.email,
            "role": post.author.role.value if hasattr(post.author.role, 'value') else post.author.role,
        },
        "like_count": like_count,
        "comment_count": comment_count,
        "liked_by_me": liked_by_me,
    }


@router.get("/posts")
def list_posts(
    search: str = Query("", description="Search title/body"),
    tag: str = Query("", description="Filter by tag"),
    sort: str = Query("latest", description="latest | top"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
):
    q = db.query(Post)
    if search:
        q = q.filter(Post.title.ilike(f"%{search}%") | Post.body.ilike(f"%{search}%"))
    if tag:
        q = q.filter(Post.tags.ilike(f"%{tag}%"))

    if sort == "top":
        # sort by like count desc
        q = (
            q.outerjoin(Like)
            .group_by(Post.id)
            .order_by(desc(func.count(Like.id)))
        )
    else:
        q = q.order_by(desc(Post.created_at))

    posts = q.all()
    return [_post_to_out(p, db, current_user) for p in posts]


@router.post("/posts", status_code=201)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    post = Post(
        author_id=user.id,
        title=data.title,
        body=data.body,
        tags=data.tags,
        image_url=data.image_url,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return _post_to_out(post, db, user)


@router.get("/posts/{post_id}")
def get_post(
    post_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return _post_to_out(post, db, current_user)


@router.patch("/posts/{post_id}")
def update_post(
    post_id: str,
    data: PostUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != user.id and user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorised to edit this post")
    if data.title is not None:
        post.title = data.title
    if data.body is not None:
        post.body = data.body
    if data.tags is not None:
        post.tags = data.tags
    if data.image_url is not None:
        post.image_url = data.image_url
    post.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(post)
    return _post_to_out(post, db, user)


@router.delete("/posts/{post_id}")
def delete_post(
    post_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != user.id and user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorised to delete this post")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}


# ═════════════════════════════════════════════════════════════════════
#  COMMENTS
# ═════════════════════════════════════════════════════════════════════

@router.get("/posts/{post_id}/comments")
def list_comments(post_id: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comments = db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at).all()
    return [
        {
            "id": c.id,
            "body": c.body,
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "author": {
                "id": c.author.id,
                "full_name": c.author.full_name,
                "email": c.author.email,
                "role": c.author.role.value if hasattr(c.author.role, 'value') else c.author.role,
            },
        }
        for c in comments
    ]


@router.post("/posts/{post_id}/comments", status_code=201)
def create_comment(
    post_id: str,
    data: CommentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = Comment(post_id=post_id, author_id=user.id, body=data.body)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return {
        "id": comment.id,
        "body": comment.body,
        "created_at": comment.created_at.isoformat() if comment.created_at else None,
        "author": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role.value if hasattr(user.role, 'value') else user.role,
        },
    }


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != user.id and user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorised to delete this comment")
    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted"}


# ═════════════════════════════════════════════════════════════════════
#  LIKES
# ═════════════════════════════════════════════════════════════════════

@router.post("/posts/{post_id}/like")
def toggle_like(
    post_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    existing = db.query(Like).filter(Like.post_id == post_id, Like.user_id == user.id).first()
    if existing:
        db.delete(existing)
        db.commit()
        liked = False
    else:
        db.add(Like(post_id=post_id, user_id=user.id))
        db.commit()
        liked = True
    count = db.query(func.count(Like.id)).filter(Like.post_id == post_id).scalar()
    return {"like_count": count, "liked_by_me": liked}


@router.get("/posts/{post_id}/likes")
def get_likes(
    post_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    count = db.query(func.count(Like.id)).filter(Like.post_id == post_id).scalar()
    liked = False
    if current_user:
        liked = db.query(Like).filter(Like.post_id == post_id, Like.user_id == current_user.id).first() is not None
    return {"like_count": count, "liked_by_me": liked}


# ═════════════════════════════════════════════════════════════════════
#  IMAGE UPLOAD
# ═════════════════════════════════════════════════════════════════════

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    user: User = Depends(require_auth),
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
        raise HTTPException(status_code=400, detail="Invalid image type")
    filename = f"{uuid.uuid4().hex}{ext}"
    dest = os.path.join(UPLOAD_DIR, filename)
    with open(dest, "wb") as buf:
        shutil.copyfileobj(file.file, buf)
    image_url = f"/community-images/{filename}"
    return {"image_url": image_url}


# ═════════════════════════════════════════════════════════════════════
#  SEED DATA  (auto-inserted once on first run)
# ═════════════════════════════════════════════════════════════════════

def seed_if_empty(db: Session):
    """Insert 5 demo posts + a demo user if DB is empty."""
    if db.query(User).count() > 0:
        return  # already seeded

    logger.info("🌱 Seeding community database …")

    demo = User(
        id="seed_farmer_01",
        full_name="Rajesh Kumar",
        email="rajesh@smartcropx.demo",
        hashed_password=hash_password("password123"),
        role=Role.FARMER,
    )
    demo2 = User(
        id="seed_buyer_01",
        full_name="Priya Sharma",
        email="priya@smartcropx.demo",
        hashed_password=hash_password("password123"),
        role=Role.BUYER,
    )
    admin = User(
        id="seed_admin_01",
        full_name="Admin User",
        email="admin@smartcropx.demo",
        hashed_password=hash_password("admin123"),
        role=Role.ADMIN,
    )
    db.add_all([demo, demo2, admin])
    db.flush()

    posts_data = [
        {
            "author_id": demo.id,
            "title": "Best practices for organic tomato farming",
            "body": (
                "I've been growing organic tomatoes for 5 years now. The key factors "
                "are quality compost, consistent watering, and proper spacing. "
                "Using neem oil spray every 2 weeks helps keep pests away naturally. "
                "Happy to answer questions from fellow farmers!"
            ),
            "tags": "organic,tomato,tips",
        },
        {
            "author_id": demo2.id,
            "title": "Looking for bulk onion suppliers in Maharashtra",
            "body": (
                "Our restaurant chain needs 500 kg of red onions per week. "
                "Looking for reliable farmers who can provide consistent quality "
                "at fair prices. Direct farm-to-kitchen preferred. "
                "Please reply if interested!"
            ),
            "tags": "onion,buying,maharashtra",
        },
        {
            "author_id": demo.id,
            "title": "Dealing with wheat rust – what worked for me",
            "body": (
                "Last season brown leaf rust hit my wheat crop hard. After trying "
                "several approaches, a combination of resistant varieties (HD-3226) "
                "and timely fungicide application saved about 80% of the yield. "
                "Early detection using SmartCropX disease scanner was a game changer."
            ),
            "tags": "wheat,disease,rust,tips",
        },
        {
            "author_id": demo2.id,
            "title": "Soil health workshop this Saturday – Pune",
            "body": (
                "Free workshop on soil testing & improvement techniques at "
                "Krishi Vigyan Kendra, Pune this Saturday 10 AM. Topics include "
                "pH balancing, organic matter enrichment, and micro-nutrient management. "
                "Bring your soil samples for free analysis!"
            ),
            "tags": "soil,workshop,pune,event",
        },
        {
            "author_id": admin.id,
            "title": "Welcome to the SmartCropX Community!",
            "body": (
                "This is your space to share farming knowledge, ask questions, "
                "find buyers & sellers, and stay updated on agricultural best practices. "
                "Please be respectful to fellow members. Happy farming! 🌾"
            ),
            "tags": "announcement,welcome",
        },
    ]
    for pd in posts_data:
        db.add(Post(**pd))

    db.commit()
    logger.info("✅ Seeded 3 users + 5 posts")
