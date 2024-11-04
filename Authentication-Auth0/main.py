from fastapi import FastAPI, Depends, status

app = FastAPI()


@app.get("/api/public")
def public():
    '''This is a public endpoint'''  
    return {"message": "This is a public endpoint"}

@app.get("/api/private", status_code=status.HTTP_200_OK)
def private():
    '''This is a private endpoint'''
    return {"message": "This is a private endpoint"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)