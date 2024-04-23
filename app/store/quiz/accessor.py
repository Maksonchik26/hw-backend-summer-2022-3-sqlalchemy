from collections.abc import Iterable
from sqlalchemy import select, ScalarResult
from sqlalchemy.orm import selectinload

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    AnswerModel,
    QuestionModel,
    ThemeModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> ThemeModel:
        theme = ThemeModel(title=title)
        async with self.app.database.session() as session:
            session.add(theme)
            await session.commit()
            await session.refresh(theme)

            return theme

    async def get_theme_by_title(self, title: str) -> ThemeModel | None:
        async with self.app.database.session() as session:
            result = await session.scalar(select(ThemeModel).where(ThemeModel.title == title))

            return result

    async def get_theme_by_id(self, id_: int) -> ThemeModel | None:
        async with self.app.database.session() as session:
            result = await session.scalar(select(ThemeModel).where(ThemeModel.id == id_))

            return result

    async def list_themes(self) -> ScalarResult[ThemeModel]:
        async with self.app.database.session() as session:
            result = await session.scalars(select(ThemeModel))

            return result

    async def create_question(
        self, title: str, theme_id: int, answers: Iterable[AnswerModel]
    ) -> QuestionModel:
        async with self.app.database.session() as session:
            question = QuestionModel(title=title, theme_id=theme_id, answers=answers)
            session.add(question)
            await session.commit()

            return question

    async def get_question_by_title(self, title: str) -> QuestionModel | None:
        async with self.app.database.session() as session:
            result = await session.scalar(select(QuestionModel).
                                          options(selectinload(QuestionModel.answers)).
                                          where(QuestionModel.title == title))

            return result

    async def list_questions(
        self, theme_id: int | None = None
    ) -> ScalarResult[QuestionModel]:
        async with self.app.database.session() as session:
            if theme_id:
                result = await session.scalars(select(QuestionModel).
                                               options(selectinload(QuestionModel.answers)).
                                               where(QuestionModel.theme_id == theme_id))
            else:
                result = await session.scalars(select(QuestionModel).options(selectinload(QuestionModel.answers)))

            return result
