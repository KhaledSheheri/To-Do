from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AddTaskShareRequest,DeleteTaskShareRequest
from app.models import TaskShare, Task, User


def get_task_share_service(user_id: int,db: Session):
    shared_owners = (
        db.query(TaskShare.owner_id)
        .filter(TaskShare.receiver_id == user_id)
        .subquery()
    )

    tasks = (
        db.query(Task, User.username.label("owner_name"))
        .join(User, Task.user_id == User.id)
        .filter(Task.user_id.in_(shared_owners))
        .all()
    )

    return {
    "tasks": [
            {
            "task_id": task.Task.id,
            "title": task.Task.title,
            "description": task.Task.description,
            "owner": task.owner_name,
            }
        for task in tasks
        ]
    }


def create_task_share_service(payload:AddTaskShareRequest,db: Session):

    receiver = db.query(User).filter(User.username == payload.receiver_username).first()

    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receiver not found")

    if payload.owner_id == receiver.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot share with yourself")

    existing_share = db.query(TaskShare).filter_by(
        owner_id=payload.owner_id,
        receiver_id=receiver.id
    ).first()

    if existing_share:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Task list already shared with this user")

    share = TaskShare(
        owner_id=payload.owner_id,
        receiver_id=receiver.id
    )

    db.add(share)
    db.commit()

    return {"status": "success", "message": "Tasks shared successfully"}


def delete_task_share_service(payload:DeleteTaskShareRequest,db: Session):
    share = db.query(TaskShare).filter_by(
        owner_id=payload.owner_id,
        receiver_id=payload.receiver_id
    ).first()

    if not share:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task share not found")

    # Delete the share entry
    db.delete(share)
    db.commit()

    return {"status": "success", "message": "Task share revoked successfully"}