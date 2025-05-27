import io
from fastapi import APIRouter, Depends, HTTPException, status, Response
from datetime import datetime,time,timezone
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AddTaskRequest, DeleteTaskRequest,PatchTaskRequest,GetTasksRequest,TaskResponse,GetTasksResponse
from app.models import Task,User
from app.utils.pdf_exporter import generate_tasks_pdf
from fastapi.responses import StreamingResponse
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()

def get_tasks_service(user_id: int,db: Session):
    tasks = (
            db.query(Task)
            .filter(Task.user_id ==user_id)
            .order_by(Task.position.asc(), Task.created_at.asc())
            .all()
        )
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this user")

    return GetTasksResponse(Tasks=tasks)


def create_new_task_service(payload:AddTaskRequest,db: Session):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User ID does not exist")
    
    new_task=Task(
        user_id=payload.user_id,
        title=payload.title,
        description=payload.description
    )
    if payload.due_date is not None:
        new_task.due_date = payload.due_date

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    if payload.due_date is not None:
        run_datetime = payload.due_date
        new_task.due_date = run_datetime
        if run_datetime <datetime.now(timezone.utc):
            mark_task_as_done(new_task.id, db)
        else:
            scheduler.add_job(
                mark_task_as_done,
                trigger='date',
                run_date=run_datetime,
                args=[new_task.id, db]
            )
    return new_task

def mark_task_as_done(task_id:int,db: Session):
    selected_task=db.query(Task).filter(Task.id==task_id).first()
    selected_task.status = "done"
    db.commit()
    db.refresh(selected_task)



def delete_task_service(payload:DeleteTaskRequest,db: Session):
    selected_task=db.query(Task).filter(Task.id==payload.task_id).first()

    if not selected_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if (selected_task.user_id!= payload.user_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Task Belongs To Another User"
        )

    db.delete(selected_task)
    db.commit()

def patch_task_service(payload: PatchTaskRequest, db: Session):
    selected_task = db.query(Task).filter(Task.id == payload.task_id).first()

    if not selected_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if (selected_task.user_id!= payload.user_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Task Belongs To Another User"
        )

    if payload.title is not None:
        selected_task.title = payload.title
    if payload.description is not None:
        selected_task.description = payload.description
    if payload.position is not None:
        selected_task.position = - payload.position
    if payload.status is not None:
        selected_task.status = payload.status
    if payload.due_date is not None:
        selected_task.due_date = payload.due_date

    db.commit()
    db.refresh(selected_task)
    if payload.due_date is not None:
        run_datetime = payload.due_date
        selected_task.due_date = run_datetime
        if run_datetime <datetime.now(timezone.utc):
            mark_task_as_done(selected_task.id, db)
        else:
            scheduler.add_job(
                mark_task_as_done,
                trigger='date',
                run_date=run_datetime,
                args=[selected_task.id, db]
            )

    return selected_task


def export_tasks_pdf_service(user_id: int, db: Session):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks to export")
    
    pdf_bytes = generate_tasks_pdf(tasks)
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=tasks_user_{user_id}.pdf"
    })