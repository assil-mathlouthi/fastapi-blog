from fastapi import FastAPI, Request,requests
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates")
posts : list[dict] = [
    {
        "id": 1,
        "title": "Why Electric Vehicles Are the Future of Tunisia",
        "content": "Electric vehicles are gaining momentum in Tunisia due to rising fuel costs and environmental awareness. In this article, we explore government incentives, charging infrastructure challenges, and what this means for the future of mobility.",
        "author": "Assil Mathlouthi",
        "published_at": "2026-02-10T09:30:00",
        "category": "EV & Sustainability"
    },
    {
        "id": 2,
        "title": "Building a Full Stack Mobile App with Flutter and FastAPI",
        "content": "Combining Flutter for the frontend and FastAPI for the backend allows developers to build high-performance applications quickly. We walk through authentication, REST APIs, and deployment strategies for modern apps.",
        "author": "Assil Mathlouthi",
        "published_at": "2026-02-12T14:15:00",
        "category": "Software Engineering"
    },
    {
        "id": 3,
        "title": "Understanding Clean Architecture in Mobile Development",
        "content": "Clean architecture separates business logic from UI and external services. This approach makes your app more scalable, testable, and maintainable over time.",
        "author": "Sarra Ben Ali",
        "published_at": "2026-02-13T11:00:00",
        "category": "Architecture"
    },
    {
        "id": 4,
        "title": "How to Implement JWT Authentication Securely",
        "content": "JWT tokens are widely used for authentication in modern web apps. Learn how to generate, verify, and protect tokens while avoiding common security mistakes.",
        "author": "Mohamed Trabelsi",
        "published_at": "2026-02-14T16:45:00",
        "category": "Backend & Security"
    },
    {
        "id": 5,
        "title": "From Idea to MVP: Shipping Your First Startup App",
        "content": "Launching an MVP requires focusing on core features, validating user needs, and iterating fast. In this guide, we discuss lean development strategies and real-world lessons from indie founders.",
        "author": "Assil Mathlouthi",
        "published_at": "2026-02-15T10:20:00",
        "category": "Startup"
    }
]


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "posts": posts,"title":"Vortex"})
   

