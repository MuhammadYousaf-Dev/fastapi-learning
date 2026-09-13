from fastapi import FastAPI,HTTPException,Request, status
#from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from schemas import PostCreate, PostResponse

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

@app.get("/api/posts", response_model=list[PostResponse])
def get_posts():
    return posts

@app.post(
    "/api/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: PostCreate):
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": "April 23, 2025",
    }
    posts.append(new_post)
    return new_post

@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_posts(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
