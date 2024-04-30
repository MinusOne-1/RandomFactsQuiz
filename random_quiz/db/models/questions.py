from sqlalchemy import Column, ForeignKey, Integer, Boolean, TEXT
from sqlalchemy.orm import relationship
from random_quiz.db.models.base import BaseTable


class Question(BaseTable):
    __tablename__ = "question"

    quiz_id = Column(

        ForeignKey('quiz.id', ondelete="SET NULL", onupdate="SET NULL"),
        nullable=True,
        doc="Foreign key to the quiz this question belongs to",
    )
    text = Column(
        TEXT,
        nullable=False,
        doc="Text of the question",
    )
    correct_answer = Column(
        Boolean,
        nullable=False,
        doc="Correct answer of the question (boolean)",
    )
    question_index = Column(
        Integer,
        nullable=False,
        doc="Index of the question in the quiz",
    )

    quiz = relationship("Quiz", back_populates="questions")
