from uuid import uuid4


async def terminate_session(app, session_id):
    with await app['redis_pool'] as redis:
        redis.delete(session_id)


async def create_session(app, user_id):
    session_id = uuid4().hex
    with await app['redis_pool'] as redis:
        redis.setex(session_id, 300, user_id)
    return session_id
