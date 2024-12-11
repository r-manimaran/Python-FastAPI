from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import redis
import requests
import json
from typing import List

# Add Logging
logging.basicConfig(level=logging.INFO)
logging = logging.getLogger(__name__)

r = redis.Redis(host="redis", port=6379, db=0)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    messages: List[Message]


@app.get("/")
def read_root():
    return {"message": "Hello World From Service 1"}

@app.get("/api/service1/{conversation_id}")
async def get_conversation(conversation_id: str):
    logging.info(f"Getting conversation {conversation_id}")
    existing_conversation_json = r.get(conversation_id)
    if existing_conversation_json is None:
        logger.info(f"Conversation {conversation_id} not found in Redis")
        return {"error": "Conversation not found"}
    else:
        existing_conversation = json.loads(existing_conversation_json)
        return existing_conversation

@app.post("/api/service1/{conversation_id}")
async def post_conversation(conversation_id: str, conversation: Conversation):
    logging.info(f"Posting conversation {conversation_id}")
    existing_conversation_json = r.get(conversation_id)

    if existing_conversation_json is not None:
        logger.info(f"Conversation {conversation_id} already exists in Redis")
        existing_conversation = json.loads(existing_conversation_json)
    else:
        existing_conversation = {"conversation":[{"role":"system","content":"You are a helpful assitant"}]}
    
    existing_conversation["conversation"].append(conversation.dict()["messages"][-1])

    response = requests.post(f"http://service2:80/api/service2/{conversation_id}", json=existing_conversation)
    response.raise_for_status()
    assitant_message = response.json()["reply"]

    existing_conversation["conversation"].append({"role":"assistant","content":assitant_message})
      
    conversation_json = json.dumps(existing_conversation)
    r.set(conversation_id, conversation_json)

    return existing_conversation


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)