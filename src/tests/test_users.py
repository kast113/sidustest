import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from dirty_equals import IsInstance

from app.api.users.models import Users


async def setup_data(session: AsyncSession):
    user_1 = Users(name="User1", email="user1@email.com", password="password1")
    user_2 = Users(name="User2", email="user2@email.com", password="password2")
    user_3 = Users(name="User3", email="user3@email.com", password="password3")

    session.add_all([user_1, user_2, user_3])
    await session.flush()
    await session.commit()


@pytest.mark.asyncio
async def test_users_create_with_invalid_data(
    ac: AsyncClient, session: AsyncSession
) -> None:
    response = await ac.post(
        "/api/v1/users/",
        json={"description": "description"}
    )
    assert 422 == response.status_code


@pytest.mark.asyncio
async def test_users_create(
    ac: AsyncClient, session: AsyncSession
) -> None:
    user_json = {
        "name": "user9",
        "email": "user9@email.com",
        "password": "password9"
    }
    response = await ac.post(
        "/api/v1/users/",
        json=user_json
    )
    assert 201 == response.status_code
    expected_response = {
        "id": IsInstance(int),
        "name": "user9",
        "email": "user9@email.com"
    }
    assert expected_response == response.json()


@pytest.mark.asyncio
async def test_users_find_not_existen(
    ac: AsyncClient, session: AsyncSession
) -> None:
    response = await ac.get("/api/v1/users/999/")
    assert 404 == response.status_code


@pytest.mark.asyncio
async def test_users_find_one(ac: AsyncClient, session: AsyncSession) -> None:
    user_1 = Users(name="User1", email="user1@email.com", password="password1")
    session.add(user_1)
    await session.flush()

    response = await ac.get(f"/api/v1/users/{user_1.id}/")
    assert 200 == response.status_code

    expected_response = {
        "id": IsInstance(int),
        "name": "User1",
        "email": "user1@email.com"
    }
    assert expected_response == response.json()


@pytest.mark.asyncio
async def test_users_find_all(ac: AsyncClient, session: AsyncSession) -> None:
    await setup_data(session)

    response = await ac.get("/api/v1/users/")
    assert 200 == response.status_code

    expected_response = [
        {
            "id": IsInstance(int),
            "name": "User1",
            "email": "user1@email.com"
        },
        {
            "id": IsInstance(int),
            "name": "User2",
            "email": "user2@email.com"
        },
        {
            "id": IsInstance(int),
            "name": "User3",
            "email": "user3@email.com"
        }
    ]
    assert expected_response == response.json()
