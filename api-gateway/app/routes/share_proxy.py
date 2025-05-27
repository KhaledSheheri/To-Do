from io import BytesIO
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
import httpx

from app.schemas import AddTaskShareRequest, DeleteTaskShareRequest, GetTasksRequest, GetTasksResponse
from app.utils.auth_utils import verify_token_and_get_user_id

router = APIRouter()
# TASK_SHARE_SERVICE_URL = "http://localhost:1024/taskshare"
TASK_SHARE_SERVICE_URL = "http://host.docker.internal:1024/taskshare"



@router.get("/taskshare")
async def proxy_get_tasks(user_id: int = Depends(verify_token_and_get_user_id)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TASK_SHARE_SERVICE_URL}/taskshare", params={"user_id": user_id})
    return response.json()


@router.post("/taskshare")
async def proxy_add_task_share(payload: AddTaskShareRequest, user_id: int = Depends(verify_token_and_get_user_id)):
    payload.owner_id = user_id  
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TASK_SHARE_SERVICE_URL}/taskshare",
            json=payload.model_dump()
        )
        if response.status_code != 201:
            return JSONResponse(status_code=response.status_code, content=response.json())
        return response.json()

@router.delete("/taskshare")
async def proxy_delete_task_share(payload: DeleteTaskShareRequest, user_id: int = Depends(verify_token_and_get_user_id)):
    payload.owner_id = user_id 
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method="DELETE",
            url=f"{TASK_SHARE_SERVICE_URL}/taskshare",
            json=payload.model_dump()
        )
        if response.status_code != 200:
            return JSONResponse(status_code=response.status_code, content=response.json())
        return Response(status_code=200)
