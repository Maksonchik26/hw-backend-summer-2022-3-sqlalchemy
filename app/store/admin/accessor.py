from typing import TYPE_CHECKING

from sqlalchemy import text, select

from app.admin.models import AdminModel
from app.base.base_accessor import BaseAccessor
from app.web.utils import hash_password

if TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        self.app = app
        await self.create_admin(app.config.admin.email, app.config.admin.password)

    async def get_by_email(self, email: str) -> AdminModel | None:
        async with self.app.database.session() as session:
            result = await session.scalar(select(AdminModel).where(AdminModel.email == email))
            return result

    async def create_admin(self, email: str, password: str) -> AdminModel:
        admin = AdminModel(email=email, password=hash_password(password))
        async with self.app.database.session() as session:
            if not await self.get_by_email(email):
                session.add(admin)
                await session.commit()
                await session.refresh(admin)

                return admin
