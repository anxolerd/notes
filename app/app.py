import aioredis
import asyncpg
from aiohttp.web import Application
from aiohttp_jinja2 import setup as setup_jinja2
from aiohttp_jinja2 import request_processor
from jinja2 import FileSystemLoader

import app.handlers.admin as admin_handler
import app.handlers.root as root_handler
from app.ctx_processors import user_processor


async def init_app(loop):
    host = '0.0.0.0'
    port = 5000

    app = Application(loop=loop)
    # Create a database connection pool
    app['pool'] = await asyncpg.create_pool(database='vagga', user='vagga', port=5433)
    app['redis_pool'] = await aioredis.create_pool(('localhost', 6379))

    app.router.add_route('GET', '/', root_handler.index)
    app.router.add_route('GET', '/login', root_handler.login)
    app.router.add_route('POST', '/login', root_handler.login)
    app.router.add_route('GET', '/logout', root_handler.logout)

    app.router.add_route('GET', '/admin/', admin_handler.index)

    setup_jinja2(
        app,
        context_processors=[user_processor, request_processor],
        loader=FileSystemLoader('app/templates')
    )

    handler = app.make_handler()
    srv = await loop.create_server(handler, host, port)

    return srv, handler
