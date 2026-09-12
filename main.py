from fastapi import FastAPI,HTTPException,Request, status
#from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# app is an object of FastAPI() class we can name it any 
app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts: list[dict]=[
    {
        "id": 1,
        "author": "Muhammad Yousaf",   
        "title": "FastAPI is awesome",
        "content": "This framework is really easy to use and super fast",
        "date_posted": "Apirl 20, 2026",
    },
    {
        "id": 2,
        "author": "Malo Fish",
        "title": "Python is great for web development",
        "content": "Python is a great language for web development and FastAPI makes it even better.",
        "date_posted": "Apirl 21,2026",
    },
]

# routes using the same name of our object routes same as urls in Django
# @app.get("/")
# def home():
#     return {"message": "Hello FastAPI"}

@app.get("/", include_in_schema=False)
@app.get("/posts", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts":posts, "title": "Home"},)

@app.get("/api/posts")
def get_posts():
    return posts


@app.get("/api/posts/{post_id}")
def get_posts(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
