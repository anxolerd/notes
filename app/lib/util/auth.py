import logging

from aiohttp.web import Request
from aiohttp.web import HTTPFound
from aiohttp.web import HTTPForbidden

import app.dao.user as user_dao


log = logging.getLogger(__name__)


def authorize(roles):
    def __decorator(func):
        async def __decorated(request):
            user = await get_auth_user(request)
            if not user:
                return HTTPFound('/login')
            if not set(user.roles).intersection(set(roles)):
                return HTTPForbidden()
            return await func(request)
        return __decorated
    return __decorator


async def get_auth_user(request: Request):
    session_id = get_session_id(request)
    if session_id:
        with await request.app['redis_pool'] as redis:
            user_id = await redis.get(session_id)
        if user_id:
            user = await user_dao.get(request.app, int(user_id))
            return user
    return None


def get_session_id(request: Request):
    session_id = request.cookies.get('X-SESSION-ID')
    return session_id


async def login(app, username, password, key, answer):
    log.info('login attempt %s', username)
    user = await user_dao.get_by_username(app, username)
    log.info('user is %s', user)
    if user and user.password == password:
        log.info('password correct')
        func = build_polynom(user.polynomial_coef)
        if func(key) == answer:
            return user
        log.error('wrong answer ex %s act %s key %s', func(key), answer, key)
    return None


def build_polynom(coefs):
    powers = range(len(coefs))[::-1]
    coefs = coefs[::]

    def func(x):
        sum = 0
        for coef, power in zip(coefs, powers):
            sum += coef * (x**power)
        return sum
    return func
