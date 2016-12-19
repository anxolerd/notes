from aiohttp.web import Request
from aiohttp.web_exceptions import HTTPFound, HTTPForbidden, HTTPNotFound
from aiohttp_jinja2 import template

import app.dao.category as category_dao
import app.dao.note as note_dao
import app.dao.user as user_dao
from app.forms.notes import NoteForm
from app.lib.util.auth import authorize, get_auth_user
from app.model import Note


@authorize(['admin', 'writer'])
@template('/notes/index.html')
async def index(request: Request):
    user = await get_auth_user(request)
    categories = await category_dao.get_by_roles(request.app, user.roles)
    return {'categories': categories}


@authorize(['admin', 'writer'])
@template('/notes/note.html')
async def create_note(request: Request):
    user = await get_auth_user(request)
    categories = await category_dao.get_by_roles(request.app, user.roles)
    form = NoteForm(await request.post())
    form.category.choices = [(c.id, c.name) for c in categories]
    if request.method == 'POST' and form.validate():
        note = Note(
            author_id=user.id,
            category_id=form.category.data,
            title=form.title.data,
            text=form.text.data,
        )
        await note_dao.create(request.app, note)
        category = await category_dao.get(request.app, form.category.data)
        raise HTTPFound('/notes/{cat}/notes'.format(cat=category.name))
    return {'form': form}


@authorize(['admin', 'writer'])
@template('/notes/category.html')
async def category(request: Request):
    user = await get_auth_user(request)
    category_name = request.match_info['cat']
    category = await category_dao.get_by_name(request.app, category_name)
    if not set(user.roles).intersection(category.allowed_roles):
        raise HTTPForbidden()
    notes = await note_dao.get_by_category_id(request.app, category.id)
    return {'notes': notes}


@authorize(['admin', 'writer'])
@template('/notes/read.html')
async def read(request: Request):
    user = await get_auth_user(request)
    note_id = int(request.match_info['id'])
    note = await note_dao.get(request.app, note_id)
    if not note:
        raise HTTPNotFound()
    category = await category_dao.get(request.app, note.category_id)
    if not set(user.roles).intersection(category.allowed_roles):
        raise HTTPForbidden()
    author = await user_dao.get(request.app, note.author_id)
    return {'author': author, 'note': note, 'category': category}
