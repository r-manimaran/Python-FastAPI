from fastapi import FastAPI, HTTPException, status, Security
from fastapi.security import APIKeyHeader, APIKeyQuery

#Generate random uniqueu Id as Keys
API_KEYS = [
    "96207bf0-10fs-d9rd-22ff56ddhru1",
    "8a7a8b9c-0d7e-1f2g-3h4i-5j6k7l8m9n0",
    "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p"
]

api_key_query = APIKeyQuery(name="api_key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
)->str:
    if api_key_query in API_KEYS:
        return api_key_query
    if api_key_header in API_KEYS:
        return api_key_header
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )

app = FastAPI()

@app.get("/public")
def root():
    """Public endpoint"""
    return {"message": "This is a public endpoint"}

@app.get("/protected", dependencies=[Security(get_api_key)])
def protected():
    """Protected endpoint"""
    return {"message": "This is a protected endpoint"}

@app.get("/admin", dependencies=[Security(get_api_key)])
def admin():
    """Admin endpoint"""
    return {"message": "This is an admin endpoint"}

@app.get("/private")
def private(api_key: str = Security(get_api_key)):
    """Private endpoint"""
    return {"message": "This is a private endpoint - {api_key}"}