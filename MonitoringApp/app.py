from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

app=FastAPI()
Instrumentator().instrument(app=app).expose(app=app)

class Item(BaseModel):
    id: int
    name: str

items=[]

@app.get("/items")
def get_items():
    return items

@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return {"message": "Item created successfully", item: item  }

@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")