from fastapi import FastAPI
from loguru import logger

#create a log file format of log_mmddyy
logger.add("logs/log_{time:MMDDYY}.log", rotation="1 day", retention="7 days", level="DEBUG")

app = FastAPI()

logger.info("Starting FastAPI app")
logger.debug("Debug message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
logger.success("Success message")
logger.trace("Trace message")
logger.exception("Exception message")


@app.get("/")
async def root():
    logger.info("Hello World")
    return {"message": "Hello World"}

@app.get("/add/{a}/{b}")
async def divide(a: int, b: int):
    try:
        logger.info("Dividing {a} by {b}", a=a, b=b)
        c= a/b
    except ZeroDivisionError:
        logger.error("Division by zero")
   