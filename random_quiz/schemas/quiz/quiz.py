from pydantic import BaseModel, UUID4


class Quiz(BaseModel):
    id: UUID4
    num_questions: int
    num_correct: int | None

    class Config:
        orm_mode = True
