from fastapi import FastAPI, Request,HTTPException,status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]

@app.get("/",include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "posts": posts,"title":"Vortex"})
   

@app.get("/posts")
def get_posts():
    return posts

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = next((post for post in posts if post["id"] == post_id),None)
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{post_id} not found")