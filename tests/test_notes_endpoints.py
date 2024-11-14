from httpx import AsyncClient

from auth.models import User
from conftest import session
from notes.models import Note


async def test_prepare_db(session):
    test_note = Note(title='some_title', text='foo_text', owner_email='test@email.com')
    test_user = User(email='test@email.com', name='test')

    session.add(test_user)
    session.add(test_note)

    await session.commit()


async def test_get_home(ac: AsyncClient):
    resp = ac.get('/')

    assert resp.status_code == 200


async def test_get_user_page(ac: AsyncClient):
    resp = ac.get('/user')

    assert resp.status_code == 200


async def test_get_create_note(ac: AsyncClient):
    resp = ac.get('/create_note')

    assert resp.status_code == 200


async def test_post_create_note(ac: AsyncClient):
    resp = ac.post(
        '/create_note',
        data={
            'title': 'test title',
            'text': 'test text'
        }
    )

    assert resp.status_code == 200


async def test_get_all_notes_by_user(ac: AsyncClient):
    resp = ac.get('/note')

    assert resp.status_code == 200
    assert resp.content == 'test notes from prepare db'  # not ready


async def test_get_note_by_id(ac):
    resp = ac.get('/note/1')
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data.get('user') == 'test@email.com'
    assert resp_data.get('note') != {}


async def test_get_note_by_id_404(ac: AsyncClient):
    resp_inv = ac.get('/note/!')
    resp_inv_id = ac.get('/note/000000')

    assert resp_inv.status_code == 404
    assert resp_inv_id.status_code == 404
