from datetime import datetime
from typing import Annotated
from fastapi import Depends, FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from database import Base, engine, get_db
from schemas import PostCreate, PostResponse, UserCreate, UserResponse
from models import User, Post

Base.metadata.create_all(bind=engine)
SessionDep = Annotated[Session, Depends(get_db)]


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates")


## HTML Endpoints
@app.get("/", include_in_schema=False)
def home(request: Request, db: SessionDep):
    posts = db.query(Post).all()
    return templates.TemplateResponse(
        "home.html", {"request": request, "posts": posts, "title": "Vortex"}
    )


@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request, post_id: int, db: SessionDep):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    title: str = post.title[:30]
    return templates.TemplateResponse(
        "post.html",
        {
            "request": request,
            "post": post,
            "title": title,
        },
    )


## API Endpoints


# User Endpoints
@app.post(
    "/api/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
def create_user(user: UserCreate, db: SessionDep):
    result = db.execute(select(User).where(User.username == user.username)).first()

    if result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    result = db.execute(select(User).where(User.email == user.email)).first()
    if result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: SessionDep):
    user: User | None = db.get(User, user_id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.get("/api/users/{user_id}/posts", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: SessionDep):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user.posts


# Post Endpoints


@app.get("/api/posts", response_model=list[PostResponse])
def get_posts(db: SessionDep):
    return db.query(Post).all()


@app.post(
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


@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: SessionDep):
    post = db.get(Post, post_id)
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")


@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


# request validation errors always 422 status code
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
