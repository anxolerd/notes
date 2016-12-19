import logging
import random

from aiohttp.web import Request
from aiohttp.web_exceptions import HTTPFound
from aiohttp_jinja2 import template

from app.forms.root import LoginForm
from app.lib.util.auth import get_session_id, get_auth_user
from app.lib.util.auth import login as login_user
from app.lib.util.session import create_session, terminate_session

log = logging.getLogger(__name__)


@template('index.html')
async def index(request):
    return {}


@template('login.html')
async def login(request: Request):
    if await get_auth_user(request):
        raise HTTPFound('/')

    key = random.randint(1, 10)
    form = LoginForm(await request.post(), key=key)
    if request.method == 'POST' and form.validate():
        app = request.app
        user = await login_user(
            app=app,
            username=form.username.data,
            password=form.password.data,
            key=form.key.data,
            answer=form.answer.data,
        )
        if user:
            session_id = await create_session(app, user.id)
            resp = HTTPFound('/')
            resp.set_cookie('X-SESSION-ID', session_id)
            raise resp
    return {'form': form}


@template('logout.html')
async def logout(request):
    app = request.app
    session_id = get_session_id(request)
    await terminate_session(app, session_id)
    resp = HTTPFound('/')
    resp.del_cookie('X-SESSION-ID')
    return resp
