from fastapi import APIRouter, Request, HTTPException, status
from fastapi.templating import Jinja2Templates

from database import SessionDep
from models import Post, User

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@router.get("/", name="home")
@router.get("/posts", name="posts")
def home(request: Request, db: SessionDep):
    posts = db.query(Post).all()
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "title": "Home"},
    )


@router.get("/posts/{post_id}")
def post_page(request: Request, post_id: int, db: SessionDep):
    post = db.get(Post, post_id)
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


@router.get("/users/{user_id}/posts", name="user_posts")
def user_posts_page(
    request: Request,
    user_id: int,
    db: SessionDep,
):
    user = db.get(User, user_id)
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
