from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import get_session
from app.schemas import AddTaskShareRequest,DeleteTaskShareRequest
from app.models import TaskShare, Task, User
from sqlalchemy import select


def get_task_share_service(user_id: int,session: Session):
    shared_owners= session.execute(select(TaskShare.owner_id).where(TaskShare.receiver_id==user_id)).scalars()
    tasks= session.execute(select(Task,User.username).where(Task.user_id.in_(shared_owners)).join(Task, Task.user_id == User.id)).all()
    return {
    "tasks": [
            {
            "task_id": task.Task.id,
            "title": task.Task.title,
            "description": task.Task.description,
            "owner": task.username
            }
        for task in tasks
        ]
    }

def create_task_share_service(payload:AddTaskShareRequest,session: Session):
    receiver = session.execute(select(User).where(User.username==payload.receiver_username)).scalar_one_or_none()

    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receiver not found")

    if payload.owner_id == receiver.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot share with yourself")

    existing_share=session.execute(select(TaskShare).where(TaskShare.owner_id==payload.owner_id,
                                                           TaskShare.receiver_id==receiver.id)).scalar_one_or_none()

    if existing_share:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Task list already shared with this user")

    share = TaskShare(
        owner_id=payload.owner_id,
        receiver_id=receiver.id
    )

    session.add(share)
    session.commit()
    return {"status": "success", "message": "Tasks shared successfully"}


def delete_task_share_service(payload:DeleteTaskShareRequest,session: Session):
    share=session.execute(select(TaskShare).where(TaskShare.owner_id==payload.owner_id,
                                                  TaskShare.receiver_id==payload.receiver_id)
                                                  ).scalar_one_or_none()
    if not share:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task share not found")
    # Delete the share entry
    session.delete(share)
    session.commit()
    return {"status": "success", "message": "Task share revoked successfully"}