from uuid import uuid4

import app.dao.security_log as security_log_dao


async def terminate_session(app, session_id):
    with await app['redis_pool'] as redis:
        user_id = int(await redis.get(session_id))
        await security_log_dao.create_logout(app, user_id)
        redis.delete(session_id)


async def create_session(app, user_id):
    session_id = uuid4().hex
    with await app['redis_pool'] as redis:
        redis.setex(session_id, 300, user_id)
    return session_id
