import pytest
from starlette.testclient import TestClient

from auth.models import User
from conftest import session, override_get_async_session
from notes.models import Note
from postgres_config.database import get_async_session
from src.main import memo_app


async def test_prepare_db(session):
    test_note = Note(title='some_title', text='foo_text', owner_email='test@email.com')
    test_user = User(email='test@email.com', name='test')

    session.add(test_user)
    session.add(test_note)

    await session.commit()


async def test_get_home(client: TestClient):
    resp = client.get('/')

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
async def test_get_user_page(client: TestClient, fastapi_dep, jwt_login):
    resp = client.get('/user', cookies={'auth_token': jwt_login})

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
async def test_get_create_note(client: TestClient, fastapi_dep, jwt_login):
    resp = client.get('/create_note', cookies={'auth_token': jwt_login})

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
async def test_post_create_note(client: TestClient, fastapi_dep, jwt_login):
    resp = client.post(
        '/create_note',
        data={
            'title': 'test title',
            'text': 'test text'
        },
        cookies={'auth_token': jwt_login}
    )

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
async def test_get_all_notes_by_user(client: TestClient, fastapi_dep, jwt_login):
    resp = client.get('/notes', cookies={'auth_token': jwt_login})

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
async def test_get_note_by_id(client: TestClient, fastapi_dep, jwt_login):
    resp = client.get('/notes/1', cookies={'auth_token': jwt_login})
    resp_inv = client.get('/notes/!', cookies={'auth_token': jwt_login})
    resp_inv_id = client.get('/notes/000000', cookies={'auth_token': jwt_login})

    assert resp.status_code == 200
    assert resp_inv.status_code == 422
    assert resp_inv_id.status_code == 404
