from app.lib.util.auth import get_auth_user


async def user_processor(request):
    user = await get_auth_user(request)
    return {'auth_user': user}
