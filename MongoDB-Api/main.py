from fastapi import FastAPI
from routes import blogs

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(blogs.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)