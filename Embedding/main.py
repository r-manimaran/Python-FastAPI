from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
from fastapi import HTTPException


# initialize the App
app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded")

#pydantic model for the input data
class InputData(BaseModel):
    query: str

#Endpoints
@app.get("/")
def home():
    return {"message": "Embedding your query using Sentece-transformer"}

@app.post("/embeddings", response_model = list)
async def get_embeddings(data: InputData):
    query = data.query
    try:
        # compute the embeddings using the query
        embeddings = model.encode(query)
        print("Embeddings computed")
        # convert Numpy array to list
        embeddings_list = embeddings.tolist()
        return embeddings_list

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)