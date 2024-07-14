from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers import todos,auth
import models
from database import engine
# Added for Logging
import logging
from logging_config import setup_logging

#Setup the logging
setup_logging()

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Test Endpoint 
@app.get("/")
def read_root():
    logging.info("Root Endpoint called")
    return {"Hello": "World"}

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