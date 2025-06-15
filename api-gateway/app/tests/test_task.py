import pytest
import httpx
from app.database import get_db
from sqlalchemy import insert,select,delete
from app.models import User,Task
from sqlalchemy.orm import Session
from app.utils.password import hash_password,verify_password
from app.schemas import AddTaskRequest


@pytest.fixture
def create_new_task_test_sit_up():
    session=next(get_db())
    test_user= User(
        username="TheTest3",
        hashed_password=hash_password("1"),
    )
    session.add(test_user)
    session.commit()
    session.refresh(test_user)     

    (
        yield test_user
    )
    test_users_tasks=session.execute(select(Task).where(Task.user_id==test_user.id)).scalars()
    for task in test_users_tasks:
        session.delete(task)
    session.delete(test_user)
    session.commit()

@pytest.mark.asyncio
async def test_create_new_task(create_new_task_test_sit_up):
    test_user=create_new_task_test_sit_up
    request=AddTaskRequest(
        user_id=test_user.id,
        title="1",
        description=""
    )

    async with httpx.AsyncClient() as client:
        response=await client.post(
            "http://localhost:8080/tasks/",
            json=request.model_dump()
        )
        assert response.status_code ==200