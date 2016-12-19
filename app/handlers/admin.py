from aiohttp.web import Request, HTTPNotFound
from aiohttp.web_exceptions import HTTPFound
from aiohttp_jinja2 import template

import app.dao.category as category_dao
from app.forms.admin import CategoryForm
from app.lib.util.auth import authorize
from app.model import Category


@authorize(['admin'])
@template('admin/index.html')
async def index(request: Request):
    return {}


@authorize(['admin'])
@template('admin/categories.html')
async def categories(request: Request):
    limit = request.rel_url.query.get('limit', 10)
    offset = request.rel_url.query.get('offset', 0)
    categories_ = await category_dao.get_all(request.app, limit, offset)
    return {'categories': categories_, 'limit': limit, 'offset': offset}


@authorize(['admin'])
@template('admin/category.html')
async def create_category(request: Request):
    form = CategoryForm(await request.post())
    if request.method == 'POST' and form.validate():
        category = Category(
            name=form.name.data,
            allowed_roles=form.allowed_roles.data,
        )
        await category_dao.create(request.app, category)
        raise HTTPFound('/admin/categories')

    return {'form': form}


@template('admin/category.html')
async def edit_category(request: Request):
    category_id = request.match_info['id']
    category = await category_dao.get(request.app, int(category_id))
    if not category:
        raise HTTPNotFound
    form = CategoryForm(await request.post(), obj=category)
    if request.method == 'POST' and form.validate():
        category = Category(
            name=form.name.data,
            allowed_roles=form.allowed_roles.data,
        )
        await category_dao.update(request.app, category)
        raise HTTPFound('/admin/categories')

    return {'form': form}

