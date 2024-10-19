from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


app = FastAPI()
app.include_router(router, prefix="/api/v1")

