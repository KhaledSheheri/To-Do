from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import get_session
from app.schemas import AddTaskShareRequest,DeleteTaskShareRequest,GetTasksResponse
from app.services.share_services import create_task_share_service, delete_task_share_service, get_task_share_service

router=APIRouter()

@router.get("/",response_model=GetTasksResponse)
def get_task_share_route(user_id: int,session: Session=Depends(get_session)):
    return get_task_share_service(user_id,session)

@router.post("/",status_code=status.HTTP_201_CREATED)
def add_task(payload:AddTaskShareRequest,session: Session = Depends(get_session)):
    return  create_task_share_service(payload, session)

@router.delete("/",status_code=status.HTTP_200_OK)
def delete_task_share_route(payload:DeleteTaskShareRequest,session: Session = Depends(get_session)):
    return  delete_task_share_service(payload, session)