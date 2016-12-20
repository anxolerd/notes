import json
from datetime import datetime, date

from app.model import SecurityLog

SAFE_EVENT_TYPES = (
    EVENT_TYPE_LOGIN_SUCESSFULL,                 # 0
    EVENT_TYPE_PROTECTED_PAGE_ACCESS_SUCESSFUL,  # 1
    EVENT_TYPE_LOGOUT_SUCESSFULL,                # 2
) = range(3)


UNSAFE_EVENT_TYPES = (
    EVENT_TYPE_LOGIN_WRONG_PASSWORD,             # 100
    EVENT_TYPE_LOGIN_WRONG_ANSWER,               # 101
    EVENT_TYPE_PROTECTED_PAGE_ACCESS_FORBIDDEN,  # 102
    EVENT_TYPE_PROTECTED_PAGE_ACCESS_NOT_FOUND,  # 103
) = range(100, 104)


TITLES = {
    EVENT_TYPE_LOGIN_SUCESSFULL: 'Login successful',
    EVENT_TYPE_LOGIN_WRONG_ANSWER: 'Login failed. Wrong answer',
    EVENT_TYPE_LOGIN_WRONG_PASSWORD: 'Login failed. Wrong password',

    EVENT_TYPE_PROTECTED_PAGE_ACCESS_SUCESSFUL: 'Page access successful',
    EVENT_TYPE_PROTECTED_PAGE_ACCESS_FORBIDDEN: 'Page access failed. Forbidden',
    EVENT_TYPE_PROTECTED_PAGE_ACCESS_NOT_FOUND: 'Page access failed. Page does not exists',

    EVENT_TYPE_LOGOUT_SUCESSFULL: 'Logout successful',
}

_sql = ('''
insert into "security_log" (date_created, user_id, event_type, is_safe, metadata)
VALUES ($1, $2, $3, $4, $5)
''')

async def create_login_record(app, user_id):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare(_sql)

            await stmt.fetch(
                datetime.now(),
                user_id,
                EVENT_TYPE_LOGIN_SUCESSFULL,
                True,
                None,
            )


async def create_bad_password(app, user_id):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare(_sql)

            await stmt.fetch(
                datetime.now(),
                user_id,
                EVENT_TYPE_LOGIN_WRONG_PASSWORD,
                False,
                None,
            )


async def create_bad_answer(app, user_id):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare(_sql)

            await stmt.fetch(
                datetime.now(),
                user_id,
                EVENT_TYPE_LOGIN_WRONG_ANSWER,
                False,
                None,
            )


async def create_status_200(app, user_id, url):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare(_sql)

            await stmt.fetch(
                datetime.now(),
                user_id,
                EVENT_TYPE_PROTECTED_PAGE_ACCESS_SUCESSFUL,
                True,
                json.dumps({'url': url}),
            )


async def create_status_403(app, user_id, url):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare(_sql)

            await stmt.fetch(
                datetime.now(),
                user_id,
                EVENT_TYPE_PROTECTED_PAGE_ACCESS_FORBIDDEN,
                False,
                json.dumps({'url': url}),
            )


async def create_status_404(app, user_id, url):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare(_sql)

            await stmt.fetch(
                datetime.now(),
                user_id,
                EVENT_TYPE_PROTECTED_PAGE_ACCESS_NOT_FOUND,
                False,
                json.dumps({'url': url}),
            )


async def create_logout(app, user_id):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare(_sql)

            await stmt.fetch(
                datetime.now(),
                user_id,
                EVENT_TYPE_LOGOUT_SUCESSFULL,
                True,
                None,
            )


async def get_last_day(app):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                select
                    id, date_created, user_id,
                    event_type, is_safe, metadata
                from "security_log"
                order by date_created
            ''')
            results = await stmt.fetch()
    return [
        SecurityLog(**dict(result.items()))
        for result in results
    ]
