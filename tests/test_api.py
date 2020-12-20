# pylint: disable=E0611
import pytest
from httpx import AsyncClient

from api import api, models, db


@pytest.mark.asyncio
async def test_testing_endpoint():
    async with AsyncClient(app=api.app, base_url="http://test") as ac:
        response = await ac.get("/test")
    assert response.status_code == 200
    assert response.json() == {
        "ok": "Testing",
        "msg": "If you see this message it means you're on the right way."
    }

@pytest.mark.skip(reason="Skipping incomplete test")
async def test_create_user(self):
    async with AsyncClient(app=api.app, base_url="http://test") as ac:
        response = await ac.post(
            '/register',
            json={
                "first_name": "joHn",
                "last_name": "dOE",
                "email": "john.doe@mail.me",
                "username": "asuperuser",
                "password": "Sup3rS@f3P@55w0rd"
            }
        )
    assert response.status_code == 200
    assert response.json() == {
        "ok": "Testing",
        "msg": "If you see this message it means you're on the right way."
    }


@pytest.mark.skip(reason="Skipping incomplete test")
async def test_get_user(self):
    response = await c.get('/user/1')
    assert response.status_code == 200
    assert response.json() == {
        "ok": "Successful",
        "msg": "User hebele created successfully!"
    }


@pytest.mark.skip(reason="Skipping incomplete test")
async def test_get_users(self):
    response = await c.get('/users')
    assert response.status_code == 200
    assert response.json() == {
        "ok": "Successful",
        "msg": "User hebele created successfully!"
    }


@pytest.mark.skip(reason="Skipping incomplete test")
async def test_delete_user(self):
    response = await c.post(
        '/register',
        json={
            "first_name": "joHn",
            "last_name": "dOE",
            "email": "john.doe@mail.me",
            "username": "asuperuser",
            "password": "Sup3rS@f3P@55w0rd"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "ok": "Successful",
        "msg": "User hebele created successfully!"
    }


@pytest.mark.skip(reason="Skipping incomplete test")
async def test_login(self):
    response = await c.post(
        '/register',
        json={
            "first_name": "joHn",
            "last_name": "dOE",
            "email": "john.doe@mail.me",
            "username": "asuperuser",
            "password": "Sup3rS@f3P@55w0rd"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "ok": "Successful",
        "msg": "User hebele created successfully!"
    }


@pytest.mark.skip(reason="Skipping incomplete test")
async def test_change_password(self):
    response = await c.post(
        '/register',
        json={
            "first_name": "joHn",
            "last_name": "dOE",
            "email": "john.doe@mail.me",
            "username": "asuperuser",
            "password": "Sup3rS@f3P@55w0rd"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "ok": "Successful",
        "msg": "User hebele created successfully!"
    }


@pytest.mark.skip(reason="Skipping incomplete test")
async def test_logout(self):
    response = await c.post(
        '/register',
        json={
            "first_name": "joHn",
            "last_name": "dOE",
            "email": "john.doe@mail.me",
            "username": "asuperuser",
            "password": "Sup3rS@f3P@55w0rd"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "ok": "Successful",
        "msg": "User hebele created successfully!"
    }
