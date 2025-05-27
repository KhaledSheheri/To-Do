from sqlalchemy import Column, Integer, String, Boolean, DateTime,ForeignKey,Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owned_tasks = relationship("Task", back_populates="owner")
    shared_with_users = relationship("TaskShare", foreign_keys="[TaskShare.owner_id]", back_populates="owner")
    tasks_shared_with_me = relationship("TaskShare", foreign_keys="[TaskShare.receiver_id]", back_populates="receiver")

class TaskStatus(enum.Enum):
    in_progress = "in_progress"
    done = "done" 

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, default="", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    position=Column(Integer,default=0)
    status = Column(Enum(TaskStatus), default=TaskStatus.in_progress)
    owner = relationship("User", back_populates="owned_tasks")
  
class TaskShare(Base):
    __tablename__ = "taskshare"
    owner_id = Column(Integer,ForeignKey("users.id"),primary_key=True)
    receiver_id = Column(Integer,ForeignKey("users.id"),primary_key=True)
    owner = relationship("User", foreign_keys=[owner_id], back_populates="shared_with_users")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="tasks_shared_with_me")



