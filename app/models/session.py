from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
import enum
from sqlalchemy import Enum, String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .quiz import Quiz, Question, QuestionOption
    from .user import User

class SessionState(enum.Enum):
    LOBBY = "lobby"
    PREVIEW = "preview"   
    ACTIVE = "active"  
    LEADERBOARD = "leaderboard"
    FINISHED = "finished"

class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id"))
    host_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    pin: Mapped[str] = mapped_column(String(6), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    state: Mapped[SessionState] = mapped_column(Enum(SessionState), default=SessionState.LOBBY)
    current_question_id: Mapped[Optional[int]] = mapped_column(ForeignKey("questions.id"))
    state_started_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    quiz: Mapped["Quiz"] = relationship(back_populates="sessions")
    host: Mapped["User"] = relationship(back_populates="hosted_sessions")
    participants: Mapped[List["Participant"]] = relationship(back_populates="session")

class Participant(Base):
    __tablename__ = "participants"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("quiz_sessions.id"))
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    nickname: Mapped[str] = mapped_column(String(50))
    total_score: Mapped[int] = mapped_column(default=0)
    
    session: Mapped["QuizSession"] = relationship(back_populates="participants")
    user: Mapped[Optional["User"]] = relationship(back_populates="participations")
    answer_logs: Mapped[List["AnswerLog"]] = relationship(back_populates="participant")

class AnswerLog(Base):
    __tablename__ = "answer_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("quiz_sessions.id"))
    participant_id: Mapped[int] = mapped_column(ForeignKey("participants.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    option_id: Mapped[int] = mapped_column(ForeignKey("question_options.id")) 
    response_time_ms: Mapped[int] = mapped_column() 
    points_earned: Mapped[int] = mapped_column(default=0)
    is_correct: Mapped[bool] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    participant: Mapped["Participant"] = relationship(back_populates="answer_logs")