from fastapi import APIRouter
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from database import SessionDep
from models import User, Post
from schemas import PostResponse, UserResponse, UserCreate, UserUpdate
from sqlalchemy import select


router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserCreate, db: SessionDep):
    result = await db.scalar(
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
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: SessionDep):
    user: User | None = await db.get(User, user_id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/{user_id}/posts", response_model=list[PostResponse])
async def get_user_posts(user_id: int, db: SessionDep):
    user = await db.get(
        User, user_id, options=[selectinload(User.posts).selectinload(Post.author)]
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user.posts


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate, db: SessionDep):
    user: User | None = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user_update.username or user_update.email:
        result = db.scalar(
            select(User).where(
                (
                    (User.username == user_update.username)
                    | (User.email == user_update.email)
                )
                & (User.id != user_id)
            )
        )
        if result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists",
            )
    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: SessionDep):
    user: User | None = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    await db.delete(user)
    await db.commit()
