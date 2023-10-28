from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "password":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.username

app = FastAPI()

@app.get("/openapi.json", tags=["documentation"], dependencies=[Depends(get_current_username)])
async def get_openapi_json():
    from fastapi.openapi.utils import get_openapi
    return get_openapi(...)

@app.get("/docs", tags=["documentation"], dependencies=[Depends(get_current_username)])
async def get_documentation():
    return FileResponse("path/to/docs")
