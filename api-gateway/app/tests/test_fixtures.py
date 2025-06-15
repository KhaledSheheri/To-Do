import pytest
import httpx
from app.database import get_db
from sqlalchemy import insert,select,delete
from app.models import User,Task
from sqlalchemy.orm import Session
from app.utils.password import hash_password,verify_password
from app.schemas import AddTaskRequest
import pytest_asyncio

@pytest.fixture
def div_session():
    return next(get_db())

@pytest_asyncio.fixture
async def client():
    return httpx.AsyncClient()