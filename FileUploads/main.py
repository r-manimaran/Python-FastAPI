'''
Different FileUpload techniques using FastAPI
'''
from  fastapi import FastAPI, File, Request, UploadFile
from starlette.formparsers import MultiPartParser
# set this to increase the maximum temp storage size
MultiPartParser.max_file_size = 2 * 1024 * 1024 # 2MB
app = FastAPI()
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/Upload")
async def upload(uploaded_file: UploadFile = File(...)):
    print(upload_file.file)
    
    contents = await uploaded_file.read()
    return {"filename": uploaded_file.filename, "contents": contents,"isFileInMemory":uploaded_file._in_memory}

@app.post("/upload")
async def upload_file(uploaded_file:bytes = File(...)):
    content = uploaded_file
    return {"file_size":len(uploaded_file)}

@app.post("/uploadUsingStream")
async def upload_file_using_stream(request:Request):
    async for chunk in request.stream():
        print(chunk)
    return {"message":"File uploaded successfully"}

#Multiple file upload
@app.post("/multiple/files")
async def upload_files(files: list[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)