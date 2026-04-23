from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, ForeignKey, Text, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .organization import Organization
    from .session import QuizSession

class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_url: Mapped[Optional[str]] = mapped_column(String(500))
    max_players: Mapped[int] = mapped_column(default=50)
    is_public: Mapped[bool] = mapped_column(default=False)
    
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))

    organization: Mapped["Organization"] = relationship(back_populates="quizzes")
    questions: Mapped[List["Question"]] = relationship(back_populates="quiz", cascade="all, delete-orphan", order_by="Question.position")
    sessions: Mapped[List["QuizSession"]] = relationship(back_populates="quiz")

class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id"))
    text: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(500))
    type: Mapped[str] = mapped_column(String(20), default="multiple_choice") 
    time_limit: Mapped[int] = mapped_column(default=20) 
    points: Mapped[int] = mapped_column(default=1000)
    position: Mapped[int] = mapped_column(default=0)  
    engagement_tip: Mapped[Optional[str]] = mapped_column(Text) 

    quiz: Mapped["Quiz"] = relationship(back_populates="questions")
    options: Mapped[List["QuestionOption"]] = relationship(back_populates="question", cascade="all, delete-orphan")

class QuestionOption(Base):
    __tablename__ = "question_options"
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    text: Mapped[str] = mapped_column(String(255))
    is_correct: Mapped[bool] = mapped_column(default=False)

    question: Mapped["Question"] = relationship(back_populates="options")