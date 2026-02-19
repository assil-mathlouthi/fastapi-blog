from fastapi import APIRouter
from fastapi import HTTPException, status
from database import SessionDep
from models import User
from schemas import PostResponse, UserResponse, UserCreate
from sqlalchemy import select



router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: SessionDep):
    result = db.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: SessionDep):
    user: User | None = db.get(User, user_id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/{user_id}/posts", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: SessionDep):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user.posts
