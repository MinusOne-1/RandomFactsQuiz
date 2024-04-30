from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from random_quiz.db.models.base import BaseTable


class Quiz(BaseTable):
    __tablename__ = "quiz"

    user_id = Column(
        ForeignKey('user.id', ondelete="SET NULL", onupdate="SET NULL"),
        nullable=True,
        doc="Foreign key to the user who took the quiz",
    )
    num_questions = Column(
        Integer,
        nullable=False,
        doc="Number of questions in the quiz",
    )
    num_correct = Column(
        Integer,
        nullable=True,
        doc="Number of correct answers in the quiz",
    )

    questions = relationship("Question", back_populates="quiz")
