import click
import asyncio

from app.app import init_app


@click.command()
def runserver():
    """Run application server"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    srv, handler = loop.run_until_complete(init_app(loop=loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(handler.finish_connections())


if __name__ == '__main__':
    runserver()
