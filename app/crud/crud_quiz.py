from sqlalchemy.orm import Session
from app.models.quiz import Quiz
from app.models.question import Question
from app.schemas.quiz import QuizCreate, QuizUpdate

def get_quiz(db: Session, quiz_id: int):
    """Get quiz by ID."""
    return db.query(Quiz).filter(Quiz.id == quiz_id).first()

def get_quizzes(db: Session, skip: int = 0, limit: int = 10):
    """Get all quizzes with pagination."""
    return db.query(Quiz).offset(skip).limit(limit).all()

def get_user_quizzes(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    """Get quizzes created by a user."""
    return db.query(Quiz).filter(Quiz.creator_id == user_id).offset(skip).limit(limit).all()

def create_quiz(db: Session, quiz: QuizCreate, creator_id: int):
    """Create a new quiz with questions."""
    db_quiz = Quiz(
        title=quiz.title,
        description=quiz.description,
        creator_id=creator_id
    )
    db.add(db_quiz)
    db.flush()
    
    # Add questions
    for question in quiz.questions:
        db_question = Question(
            quiz_id=db_quiz.id,
            text=question.text,
            option_a=question.option_a,
            option_b=question.option_b,
            option_c=question.option_c,
            option_d=question.option_d,
            correct_answer=question.correct_answer
        )
        db.add(db_question)
    
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def update_quiz(db: Session, quiz_id: int, quiz_update: QuizUpdate):
    """Update quiz."""
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz:
        update_data = quiz_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_quiz, field, value)
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
    return db_quiz

def delete_quiz(db: Session, quiz_id: int):
    """Delete quiz and its questions."""
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz:
        db.delete(db_quiz)
        db.commit()
    return db_quiz
