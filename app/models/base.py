from sqlalchemy.orm import DeclarativeBase 

class Base(DeclarativeBase):
    pass


from .base import Base
from .user import User, UserRole, PayoutProfile
from .organization import Organization
from .quiz import Quiz, Question, QuestionOption
from .session import QuizSession, Participant, AnswerLog, SessionState
from .wallet import Wallet, Transaction, TransactionType

# This list helps with 'from app.models import *'
__all__ = [
    "Base",
    "User",
    "UserRole",
    "PayoutProfile",
    "Organization",
    "Quiz",
    "Question",
    "QuestionOption",
    "QuizSession",
    "Participant",
    "AnswerLog",
    "SessionState",
    "Wallet",
    "Transaction",
    "TransactionType"
]
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass