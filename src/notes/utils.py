import base64

from notes.models import Note

# Make it by JWT
async def create_share_link(note: Note, url: str):
    link_body = f'{note.owner_email}+{note.id}'
    link = base64.b64encode(str.encode(link_body))

    data_res_dict = {
        "success": True,
        "link": url + '/' + link.decode('UTF-8')
    }

    return data_res_dict
