from fastapi import FastAPI, HTTPException, Depends, Request

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != "mysecretkey":
        raise HTTPException(status_code=401, detail="Unauthorized")

app = FastAPI()

@app.get("/openapi.json", tags=["documentation"], dependencies=[Depends(verify_api_key)])
async def get_openapi_json():
    from fastapi.openapi.utils import get_openapi
    return get_openapi(...)

@app.get("/docs", tags=["documentation"], dependencies=[Depends(verify_api_key)])
async def get_documentation():
    return FileResponse("path/to/docs")
