import pytest
from httpx import AsyncClient

from conftest import client, async_session


# async def test_login_db_prpr():
#     async with async_session_maker() as session:
#         stmt = ''
#         await session.execute(stmt)
#         await session.commit()

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
