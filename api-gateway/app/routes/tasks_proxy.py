from io import BytesIO
from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse,Response,StreamingResponse
from app.schemas import AddTaskRequest,DeleteTaskRequest,PatchTaskRequest
import httpx
from app.utils.auth_utils import get_user_id_from_token,verify_token_and_get_user_id



router = APIRouter()
# TASK_SERVICE_URL = "http://localhost:1025/tasks"
TASK_SERVICE_URL = "http://host.docker.internal:1025/tasks"



@router.get("/tasks")
async def proxy_get_tasks(user_id: int = Depends(verify_token_and_get_user_id)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TASK_SERVICE_URL}/tasks", params={"user_id": user_id})
    return response.json()

@router.post("/tasks")
async def proxy_add_task(payload: AddTaskRequest, user_id: int = Depends(verify_token_and_get_user_id)):
    payload.user_id = user_id
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{TASK_SERVICE_URL}/tasks", json=payload.model_dump())
    if response.status_code >= 400:
        return JSONResponse(status_code=response.status_code, content=response.json())
    return response.json()

@router.delete("/tasks")
async def proxy_delete_task(payload: DeleteTaskRequest, user_id: int = Depends(verify_token_and_get_user_id)):
    payload.user_id = user_id
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method="DELETE",
            url=f"{TASK_SERVICE_URL}/tasks",
            json=payload.model_dump()
        )
        if response.status_code >= 400:
            return JSONResponse(status_code=response.status_code, content=response.json())

        if response.status_code == 204:
            return JSONResponse(status_code=204, content={"message": "Task deleted successfully"})

        return JSONResponse(status_code=response.status_code, content=response.json())

@router.patch("/tasks")
async def proxy_patch_task(payload: PatchTaskRequest, user_id: int = Depends(verify_token_and_get_user_id)):
    payload.user_id = user_id
    async with httpx.AsyncClient() as client:
        response = await client.patch(f"{TASK_SERVICE_URL}/tasks", json=payload.model_dump())
    if response.status_code >= 400:
        return JSONResponse(status_code=response.status_code, content=response.json())
    return response.json()

    
@router.get("/tasks/export", response_class=StreamingResponse)
async def proxy_export_tasks_as_pdf(user_id: int = Depends(verify_token_and_get_user_id)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{TASK_SERVICE_URL}/tasks/export",
            params={"user_id": user_id}
        )

    if response.status_code != 200:
        return JSONResponse(status_code=response.status_code, content=response.json())

    return StreamingResponse(
        BytesIO(response.content),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=tasks_user_{user_id}.pdf"
        }
    )