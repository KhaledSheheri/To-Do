from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AddTaskShareRequest,DeleteTaskShareRequest,GetTasksResponse
from app.services.share_services import create_task_share_service, delete_task_share_service, get_task_share_service

router=APIRouter()

@router.get("/taskshare",response_model=GetTasksResponse)
def get_task_share_route(user_id: int,db: Session=Depends(get_db)):
    return get_task_share_service(user_id,db)

@router.post("/taskshare",status_code=status.HTTP_201_CREATED)
def add_task(payload:AddTaskShareRequest,db: Session = Depends(get_db)):
    return  create_task_share_service(payload, db)

@router.delete("/taskshare",status_code=status.HTTP_200_OK)
def delete_task_share_route(payload:DeleteTaskShareRequest,db: Session = Depends(get_db)):
    return  delete_task_share_service(payload, db)