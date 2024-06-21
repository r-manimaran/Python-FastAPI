from fastapi import FastAPI
from app.database import Base, engine
from app.api.v1 import person_routers

app = FastAPI()

app.include_router(person_routers.router, prefix="/api")

#create the database
Base.metadata.create_all(engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)