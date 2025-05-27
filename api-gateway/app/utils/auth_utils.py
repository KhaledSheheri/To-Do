import httpx
from fastapi import HTTPException, status,Request,Header,Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="not-used") 

# AUTH_SERVICE_URL = "http://localhost:80/auth"
AUTH_SERVICE_URL = "http://host.docker.internal:80/auth"  


async def get_user_id_from_token(request: Request) -> int:
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(
                f"{AUTH_SERVICE_URL}/me",
                headers={"Authorization": token}
            )
            res.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=res.status_code, detail="Invalid token")

    user = res.json()
    return user.get("id") 


async def verify_token_and_get_user_id(token: str = Depends(oauth2_scheme)):
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{AUTH_SERVICE_URL}/verify", json={"token": token})
        if res.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        data = res.json()
        return data["user"]["id"]