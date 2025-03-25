from fastapi import FastAPI
from fastapi import Depends
import logging_config, config,models,schemas, crud
from routers import todos
from fastapi.middleware.cors import CORSMiddleware

# setup logging
logger = logging_config.setup_logging()

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(todos.router)

# dependency injection to get the config
def get_config():
    return config.Settings()

@app.get("/inform")
def info(settings: config.Settings = Depends(get_config)):
    return {
        "app_name": settings.app_name,
        "database_name": settings.database_name     
    }

@app.get("/")
def root(settings: config.Settings = Depends(get_config)):
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)