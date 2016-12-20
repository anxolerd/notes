import aiohttp_debugtoolbar
import aioredis
import asyncpg
from aiohttp.web import Application
from aiohttp_debugtoolbar import toolbar_middleware_factory
from aiohttp_jinja2 import request_processor
from aiohttp_jinja2 import setup as setup_jinja2
from jinja2 import FileSystemLoader

import app.handlers.admin as admin_handler
import app.handlers.notes as notes_handler
import app.handlers.root as root_handler
from app.ctx_processors import user_processor
from app.middleware import security_log_middleware


async def init_app(loop):
    host = '0.0.0.0'
    port = 5000

    app = Application(loop=loop, middlewares=[
        toolbar_middleware_factory,
        security_log_middleware,
    ])
    # Create a database connection pool
    app['pool'] = await asyncpg.create_pool(database='vagga', user='vagga', port=5433)
    app['redis_pool'] = await aioredis.create_pool(('localhost', 6379))

    app.router.add_route('GET', '/', root_handler.index)
    app.router.add_route('GET', '/login', root_handler.login)
    app.router.add_route('POST', '/login', root_handler.login)
    app.router.add_route('GET', '/logout', root_handler.logout)
    app.router.add_route('GET', '/profile', root_handler.profile)
    app.router.add_route('POST', '/profile', root_handler.profile)

    app.router.add_route('GET', '/admin', admin_handler.index)
    app.router.add_route('GET', '/admin/', admin_handler.index)
    app.router.add_route('GET', '/admin/categories', admin_handler.categories)
    app.router.add_route('GET', '/admin/category/create', admin_handler.create_category)
    app.router.add_route('POST', '/admin/category/create', admin_handler.create_category)
    app.router.add_route('GET', '/admin/category/{id:\d+}/edit', admin_handler.edit_category)
    app.router.add_route('POST', '/admin/category/{id:\d+}/edit', admin_handler.edit_category)
    app.router.add_route('GET', '/admin/security_log', admin_handler.security_log)

    app.router.add_route('GET', '/notes', notes_handler.index)
    app.router.add_route('GET', '/notes/', notes_handler.index)
    app.router.add_route('GET', '/notes/{cat}/notes', notes_handler.category)
    app.router.add_route('GET', '/notes/create', notes_handler.create_note)
    app.router.add_route('POST', '/notes/create', notes_handler.create_note)
    app.router.add_route('GET', '/notes/{id:\d+}/read', notes_handler.read)

    setup_jinja2(
        app,
        context_processors=[user_processor, request_processor],
        loader=FileSystemLoader('app/templates')
    )

    aiohttp_debugtoolbar.setup(app, intercept_redirects=False)

    handler = app.make_handler()
    srv = await loop.create_server(handler, host, port)

    return srv, handler
