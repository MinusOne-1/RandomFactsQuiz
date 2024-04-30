from pydantic import BaseModel


class Question(BaseModel):
    text: str
    correct_answer: bool
    question_index: int
    quiz_id: int

    class Config:
        orm_mode = True
