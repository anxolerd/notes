from aiohttp_jinja2 import template

from app.lib.util.auth import authorize


@template('admin/index.html')
@authorize(['admin'])
def index(request):
    return {}
