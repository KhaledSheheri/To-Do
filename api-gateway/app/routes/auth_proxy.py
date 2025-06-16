from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.schemas import RegisterRequest,LoginRequest,TokenData
import httpx

router = APIRouter()
AUTH_SERVICE_URL = "http://localhost:8001/auth"  
# AUTH_SERVICE_URL = "http://host.docker.internal:80/auth"  


@router.post("/login")
async def proxy_login(request: LoginRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{AUTH_SERVICE_URL}/login",
            json=request.model_dump()  
        )

        if response.status_code != 200:
            return JSONResponse(
                status_code=response.status_code,
                content={"error": response.text}
            )

        return response.json()

@router.post("/register")
async def proxy_register(request: RegisterRequest):
    body = request.model_dump_json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_SERVICE_URL}/register", content=body, headers={"Content-Type": "application/json"})
    return response.json()

@router.post("/verify")
async def proxy_verify(request: TokenData):
    body = request.model_dump_json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_SERVICE_URL}/verify", content=body, headers={"Content-Type": "application/json"})
    return response.json()