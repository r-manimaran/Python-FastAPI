from fastapi import APIRouter

from models.blog import Blog

blogs = []

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)

#endpoint for create a new Blog Post and store locally
@router.post("/blog")
async def create_blog(newblog:Blog):
    #store the blog post locally
    #we will use a list to store the blog posts  
    blogs.append(newblog)
    return {"message": "Blog created successfully"}

#endpoint to get a blog post by id
@router.get("/blog/{id}")
async def get_blog(id: int):
    return {"message": f"Blog with id {id}"}

#endpoint to list all the blogs
@router.get("/blogs")
async def get_blogs():
    return blogs
   