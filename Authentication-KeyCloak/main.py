from fastapi import FastAPI, Depends, HTTPException
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2AuthorizationCodeBearer
from jwt import PyJWKClient
import jwt
from typing import Annotated


load_dotenv()

app=FastAPI()

#Keycloak Settings
KEYCLOAK_URL=os.getenv("KEYCLOAK_URL")
KEYCLOAK_REALM=os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID=os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET=os.getenv("KEYCLOAK_CLIENT_SECRET")

TOKEN_URL=f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
AUTH_URL=f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth"
REFRESH_URL=f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
CERT_URL = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTH_URL,
    tokenUrl=TOKEN_URL,
    refreshUrl=REFRESH_URL,
)

async def valid_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    optional_customer_headers = {"User-agent":"custom-user-agent"}
    jwks_client = PyJWKClient(CERT_URL, headers = optional_customer_headers)
    print(jwks_client)
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        print(signing_key)
        data = jwt.decode(token, signing_key.key, algorithms=["RS256"],audience="account",options={"verify_exp":True},)
        return data
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid access token")

@app.get("/")
async def public():
    return {"message": "Public endpoint"}

@app.get("/private",dependencies=[Depends(valid_access_token)])
async def private():
    return {"message": "Private endpoint"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)