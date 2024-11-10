import pytest
from httpx import AsyncClient

from auth.models import User
from conftest import client, async_session


async def test_login_db_prpr():
    async with async_session() as session:
        test_model = User(name='testname', email='1@gail.com')
        await session.add(test_model)
        await session.commit()


async def test_get_login(ac):
    resp = await ac.get('/auth/login')

    assert resp.status_code == 200


async def test_post_login(ac):
    resp = await ac.post(
        '/auth/login',
        data={'email': '1@gail.com'}
    )

    assert resp.status_code == 308


async def test_post_password(ac):
    resp = await ac.post('/auth/password?email=1@gail.com')

    assert resp.status_code == 200


async def test_post_check_password(ac):
    resp = await ac.post(
        '/auth/check_password',
        data={
            'email': '1@gail.com',
            'password': '000000'
        }
    )

    assert resp.status_code == 200


async def test_get_create_user(ac):
    resp = await ac.get('/auth/create_user')
    assert resp.status_code == 200


async def test_post_create_user(ac: AsyncClient):
    resp = await ac.post(
        '/auth/create_user',
        data={
            'username': '+++++',
            'email': 'test1@test.com'
        }
    )

    assert resp.status_code == 201
