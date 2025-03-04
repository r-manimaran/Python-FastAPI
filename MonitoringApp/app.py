from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge #Custom Metrics
import time
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from fastapi.responses import Response


REQUEST_COUNT = Counter('http_request_total','Total HTTP Requests',['method','status','path'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Duration', ['method','status', 'path'])
REQUEST_IN_PROGRESS = Gauge('http_requests_in_progress', 'HTTP Requests in Progress',['method','path'])

# System Metrics
CPU_USAGE = Gauge('process_cpu_usage', 'Current CPU usuage in percent')
MEMORY_USAGE = Gauge('process_memory_usage_bytes', 'Current memory usuage in bytes')

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


## Add the Custom metrics in the middleware
@app.middleware("http")
async def add_custom_metrics(request: Request, call_next):
    method = request.method
    path = request.url.path

    REQUEST_IN_PROGRESS.labels(method=method, path=path).inc()
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    REQUEST_IN_PROGRESS.labels(method=method, path=path).dec()
    REQUEST_COUNT.labels(method=method, status=response.status_code, path=path).inc()
    REQUEST_LATENCY.labels(method=method, status=response.status_code, path=path).observe(end_time - start_time)
    return response

def update_system_metrics():
    import psutil
    current_process = psutil.Process()
    CPU_USAGE.set(current_process.cpu_percent())
    # get memory usuage in bytes
    MEMORY_USAGE.set(current_process.memory_info().rss)

@app.get("/metrics")
async def metrics():
    update_system_metrics()
    return Response(content=generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)
    #return Instrumentator().expose(app=app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)