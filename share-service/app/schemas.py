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

class TaskSharedResponse(BaseModel):
    task_id: int
    title: str
    description: str
    owner: str

class GetTasksRequest(BaseModel):
    user_id:int

class GetTasksResponse(BaseModel):
    tasks: List[TaskSharedResponse]
    
    class Config:
        from_attributes = True
    
class AddTaskRequest(BaseModel):
    user_id: int
    title:str
    description:str

class DeleteTaskRequest(BaseModel):
    task_id:int

class ModifyTaskRequest(BaseModel):
    task_id:int
    title:str
    description:str
    position:int

class PatchTaskRequest(BaseModel):
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    position: Optional[int] = None
    status: Optional[TaskStatus] = None
    class Config:
        use_enum_values = True

class AddTaskShareRequest(BaseModel):
    owner_id: int
    receiver_username: str

class DeleteTaskShareRequest(BaseModel):
    owner_id: int
    receiver_id: int

class GetTaskShareRequest(BaseModel):
    task_id: int

