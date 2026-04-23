from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class QuestionSchema(BaseModel):
    text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str

class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None

class QuizCreate(QuizBase):
    questions: List[QuestionSchema] = []

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class QuestionResponse(QuestionSchema):
    id: int
    quiz_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuizResponse(QuizBase):
    id: int
    creator_id: int
    created_at: datetime
    updated_at: datetime
    questions: List[QuestionResponse] = []
    
    class Config:
        from_attributes = True

class QuizListResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    creator_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
