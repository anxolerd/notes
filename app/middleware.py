from aiohttp.web import Request, HTTPException

import app.dao.security_log as security_log_dao
from app.lib.util.auth import get_auth_user


async def security_log_middleware(app, handler):
    async def middleware_handler(request: Request):
        user = await get_auth_user(request)
        try:
            response = await handler(request)
            if user and response.status == 404:
                await security_log_dao.create_status_404(app, user.id, request.rel_url.raw_path)
            elif user and response.status == 403:
                await security_log_dao.create_status_403(app, user.id, request.rel_url.raw_path)
            elif user:
                await security_log_dao.create_status_200(app, user.id, request.rel_url.raw_path)
            return response
        except HTTPException as ex:
            if user and ex.status == 404:
                await security_log_dao.create_status_404(app, user.id, request.rel_url.raw_path)
            elif user and ex.status == 403:
                await security_log_dao.create_status_403(app, user.id, request.rel_url.raw_path)
            raise

    return middleware_handler
