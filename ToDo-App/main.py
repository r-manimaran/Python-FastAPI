from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers import todos,auth
import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

#mount the routes
app.include_router(auth.router)
app.include_router(todos.router)


#Add the middlewware for cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)