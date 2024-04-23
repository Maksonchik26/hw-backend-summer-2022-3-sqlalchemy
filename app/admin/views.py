import aiohttp_session
from aiohttp.web_exceptions import HTTPForbidden

from app.web.app import View
from aiohttp_apispec import docs, request_schema, response_schema

from app.admin.schemes import LoginAdminRequestSchema, AdminResponseSchema, AdminSchema
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response, hash_password


class AdminLoginView(View):
    @docs(tags=["admin"], summary="Login admin", description="Login admin in the app")
    @request_schema(LoginAdminRequestSchema)
    @response_schema(AdminResponseSchema, 200)
    async def post(self):
        email, password = self.data["email"], self.data["password"]

        admin = await self.store.admins.get_by_email(email)
        if not admin or not hash_password(password) == admin.password:
            raise HTTPForbidden

        admin_data = AdminSchema().dump(admin)
        session = await aiohttp_session.new_session(self.request)
        session["admin"] = admin_data
        return json_response(data=admin_data)


class AdminCurrentView(View, AuthRequiredMixin):
    @docs(tags=["admin"], summary="Get current admin", description="Get current admin")
    @response_schema(AdminResponseSchema, 200)
    async def get(self):
        admin = await self.check_auth_admin()

        return json_response(data=AdminSchema().dump(admin))
