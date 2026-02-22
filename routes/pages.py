from fastapi import APIRouter, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import selectinload


from database import SessionDep
from models import Post, User

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@router.get("/", name="home")
@router.get("/posts", name="posts")
async def home(request: Request, db: SessionDep):
    result = await db.execute(select(Post).options(selectinload(Post.author)))
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "title": "Home"},
    )


@router.get("/posts/{post_id}")
async def post_page(request: Request, post_id: int, db: SessionDep):
    post = await db.get(Post, post_id, options=[selectinload(Post.author)])
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return templates.TemplateResponse(
        "post.html",
        {
            "request": request,
            "post": post,
            "title": post.title,
        },
    )


@router.get("/users/{user_id}/posts")
async def user_posts_page(
    request: Request,
    user_id: int,
    db: SessionDep,
):
    user = await db.get(User, user_id,options=[selectinload(User.posts)])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    posts = user.posts
    return templates.TemplateResponse(
        request,
        "user_posts.html",
        {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
    )
