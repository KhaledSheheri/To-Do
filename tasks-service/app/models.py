from sqlalchemy import Column, Integer, String, Boolean, DateTime,ForeignKey,Enum,DateTime
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
    tasks = relationship("Task", back_populates="owner")

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
    due_date=Column(DateTime, default=None)
    position=Column(Integer,default=0)
    status = Column(Enum(TaskStatus), default=TaskStatus.in_progress)
    owner = relationship("User", back_populates="tasks")


