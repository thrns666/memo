import pytest
from starlette.testclient import TestClient

from auth.models import User
from conftest import session, override_get_async_session
from postgres_config.database import get_async_session
from src.main import memo_app


async def test_login_db_prpr(session):
    test_model = User(name='test_name', email='test@email.com')
    session.add(test_model)
    await session.commit()


async def test_get_login(client: TestClient):
    resp = client.get('/auth/login')

    assert resp.status_code == 200


@pytest.mark.parametrize(
    'fastapi_dep',
    [
        (
                memo_app,
                {get_async_session: override_get_async_session}
        )
    ],
    indirect=True
)
async def test_post_login(client: TestClient, fastapi_dep):
    resp = client.post('/auth/login', data={'email': 'test@email.com'})

    assert resp.status_code == 200


async def test_post_password(client: TestClient):
    resp = client.post('/auth/password?email=test@email.com')

    assert resp.status_code == 200


async def test_post_check_password(client: TestClient):
    resp = client.post(
        '/auth/check_password',
        data={
            'email': 'test@email.com',
            'password': '000000'
        }
    )

    assert resp.status_code == 200


async def test_get_create_user(client: TestClient):
    resp = client.get('/auth/create_user')

    assert resp.status_code == 200


@pytest.mark.parametrize(
    'fastapi_dep',
    [
        (
                memo_app,
                {get_async_session: override_get_async_session}
        )
    ],
    indirect=True
)
async def test_post_create_user(client: TestClient, fastapi_dep):
    resp = client.post(
        '/auth/create_user',
        data={
            'username': '+++++',
            'email': 'test1@test.com'
        }
    )

    assert resp.status_code == 201
