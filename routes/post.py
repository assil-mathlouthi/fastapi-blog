from fastapi import APIRouter
from fastapi import HTTPException, status
from database import SessionDep
from models import Post, User
from schemas import PostCreate, PostResponse

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("/api/posts", response_model=list[PostResponse])
def get_posts(db: SessionDep):
    return db.query(Post).all()


@router.post(
    "/api/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse
)
def create_post(post: PostCreate, db: SessionDep):
    user = db.get(User, post.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: SessionDep):
    post = db.get(Post, post_id)
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")

