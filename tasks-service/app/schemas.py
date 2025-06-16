from pydantic import BaseModel
from sqlalchemy import Integer
from app.models import Task,TaskStatus
from typing import List,Optional
from datetime import datetime

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    position: int
    created_at: datetime
    status: str
    class Config: 
        from_attributes = True

class GetTasksRequest(BaseModel):
    user_id:int

class GetTasksResponse(BaseModel):
    Tasks: List[TaskResponse]
    
    class Config:
        from_attributes = True
    
class AddTaskRequest(BaseModel):
    user_id: int
    title:str
    description:str
    due_date: datetime | None = None

class DeleteTaskRequest(BaseModel):
    user_id: int
    task_id:int

class ModifyTaskRequest(BaseModel):
    user_id: int
    task_id:int
    title:str
    description:str
    position:int

class PatchTaskRequest(BaseModel):
    user_id:int
    task_id: int
    title: str| None = None
    description:str| None = None
    position: int| None = None
    due_date: str| None = None
    status: str| None = None
    class Config:
        use_enum_values = True





