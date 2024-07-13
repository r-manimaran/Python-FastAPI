from fastapi import FastAPI

app=FastAPI()

#test endpoint
@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)