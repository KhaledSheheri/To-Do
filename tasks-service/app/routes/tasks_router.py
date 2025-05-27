from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AddTaskRequest,DeleteTaskRequest,PatchTaskRequest,TaskResponse,GetTasksResponse,GetTasksRequest
from app.services.tasks_service import create_new_task_service, delete_task_service, export_tasks_pdf_service,patch_task_service, get_tasks_service


router=APIRouter()

@router.get("/tasks",response_model=GetTasksResponse)
def get_tasks(user_id: int,db: Session=Depends(get_db)):
    return get_tasks_service(user_id,db)

@router.post("/tasks", response_model=TaskResponse)
def add_task(payload:AddTaskRequest,db: Session = Depends(get_db)):
    new_task = create_new_task_service(payload, db)
    return  new_task

@router.delete("/tasks",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(payload:DeleteTaskRequest,db: Session = Depends(get_db)):
    delete_task_service(payload, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/tasks", response_model=TaskResponse)
def patch_task(payload: PatchTaskRequest, db: Session = Depends(get_db)):
    updated_task = patch_task_service(payload, db)
    return updated_task

@router.get("/tasks/export", response_class=StreamingResponse)
def export_tasks_as_pdf(user_id: int, db: Session = Depends(get_db)):
    return export_tasks_pdf_service(user_id, db)