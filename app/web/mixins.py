import aiohttp_session
from aiohttp.abc import StreamResponse
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden

from app.web.app import Request, Application


class AuthRequiredMixin:
    async def check_auth_admin(self):
        if self.request.admin is None:
            raise HTTPUnauthorized
        return self.request.admin
