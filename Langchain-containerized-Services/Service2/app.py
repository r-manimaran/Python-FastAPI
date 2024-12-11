from fastapi import FastAPI
import logging
import os
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.schema import(
    AIMessage,
    HumanMessage,
    SystemMessage
)

from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
)

ROLE_CLASS_MAP = {
    "system": SystemMessage,
    "user": HumanMessage,
    "assistant": AIMessage,
}

load_dotenv()
PG_CONNECTION_STRING = "postgresql+psycopg2://admin:admin@postgres:5432/vectordb"
COLLECTION_NAME = "vectordb"

# Setup logging
logging.basicConfig(level=logging.INFO)
logging  = logging.getLogger(__name__)

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    messages: List[Message]

embeddings = OpenAIEmbeddings()
chat = ChatOpenAI(temperature=0)

store = PGVector(
    collection_name=COLLECTION_NAME,
    connection_string=PG_CONNECTION_STRING,
    embedding_function=embeddings,
)

retriever = store.as_retriever()

prompt_template = """
You are a helpful assistant. Answer the question based on the following context:
{context}

Please provide  the most suitable response for the users question.
Answer:
"""
prompt = PromptTemplate(
    template=prompt_template, input_variables=["context"]
)
system_message_prompt = SystemMessagePromptTemplate(prompt = prompt)

def create_message(conversation):
    return [ROLE_CLASS_MAP[message.role](content = message.content) for message in conversation]

def format_docs(docs):
    formatted_docs = []
    for doc in docs:
        formatted_doc = "Source: "+doc.metadata['source']
        formatted_docs.append(formatted_doc)
    return "\n".join(formatted_docs)

app = FastAPI()

#setup middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/service2/{conversation_id}")
async def service3(conversation_id: str, conversation: Conversation):
   logging.info(f"Service 2 received conversation_id: {conversation_id}")
   query = conversation.messages[-1].content
   
   docs = retriever.get_relevant_documents(query)
   
   docs =format_docs(docs)

   prompt = system_message_prompt.format(context=docs)
   messages = [prompt]+ create_messages(conversation = conversation.messages)

   result = chat(messages)
   return {"id": conversation_id, "reply": result.content}



@app.get("/")
async def root():
    return {"message": "Hello World From Service 2"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)