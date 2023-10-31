from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import APIKeyQuery

app = FastAPI()

api_key = APIKeyQuery(name="api_key", auto_error=False)

def verify_token(api_key: str = Depends(api_key)):
    correct_api_key = "mysecretpassword"
    if api_key != correct_api_key:
        raise HTTPException(status_code=401, detail="Incorrect API Key")
    return api_key

@app.get("/docs", tags=["documentation"], include_in_schema=False)
async def custom_swagger_ui_html(req: Request, api_key: str = Depends(verify_token)):
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(openapi_url=req.url_for("openapi_schema"))

@app.get("/openapi.json", tags=["documentation"], include_in_schema=False)
async def openapi_schema(api_key: str = Depends(verify_token)):
    from fastapi.openapi.utils import get_openapi
    return get_openapi(title="Custom schema", version=1, routes=app.routes)
