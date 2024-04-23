from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
    String,
    Boolean
)


from app.store.database.sqlalchemy_base import BaseModel


class ThemeModel(BaseModel):
    __tablename__ = "themes"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    # relations
    questions: Mapped["QuestionModel"] = relationship(back_populates="theme", cascade="all, delete")


class QuestionModel(BaseModel):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    # parent
    theme_id: Mapped[int] = mapped_column(ForeignKey("themes.id", ondelete="CASCADE"))
    # relations
    theme: Mapped["ThemeModel"] = relationship(back_populates="questions")
    answers: Mapped[List["AnswerModel"]] = relationship(back_populates="question", cascade="all, delete")


class AnswerModel(BaseModel):
    __tablename__ = "answers"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # parent
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"))
    # relations
    question: Mapped["QuestionModel"] = relationship(back_populates="answers")
