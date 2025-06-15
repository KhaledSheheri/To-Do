from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_session
from app.schemas import AddTaskRequest,DeleteTaskRequest,PatchTaskRequest,TaskResponse,GetTasksResponse,GetTasksRequest
from app.services.tasks_service import create_new_task_service, delete_task_service, export_tasks_pdf_service,patch_task_service, get_tasks_service


router=APIRouter()

@router.get("/",response_model=GetTasksResponse)
def get_tasks(user_id: int,session: Session=Depends(get_session)):
    return get_tasks_service(user_id,session)

@router.post("/", response_model=TaskResponse)
def add_task(payload:AddTaskRequest,session: Session = Depends(get_session)):
    new_task = create_new_task_service(payload, session)
    return  new_task

@router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(payload:DeleteTaskRequest,session: Session = Depends(get_session)):
    delete_task_service(payload, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/", response_model=TaskResponse)
def patch_task(payload: PatchTaskRequest, session: Session = Depends(get_session)):
    updated_task = patch_task_service(payload, session)
    return updated_task

@router.get("/export", response_class=StreamingResponse)
def export_tasks_as_pdf(user_id: int, session: Session = Depends(get_session)):
    return export_tasks_pdf_service(user_id, session)