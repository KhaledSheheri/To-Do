from pydantic import BaseModel
from sqlalchemy import Integer
from app.models import Task,TaskStatus
from typing import List,Optional
from datetime import datetime

class AddTaskShareRequest(BaseModel):
    owner_id: int
    receiver_username: str

class DeleteTaskShareRequest(BaseModel):
    owner_id: int
    receiver_id: int

class TaskSharedResponse(BaseModel):
    task_id: int
    title: str
    description: str
    owner: str

class GetTasksResponse(BaseModel):
    tasks: List[TaskSharedResponse]
    
    class Config:
        from_attributes = True
