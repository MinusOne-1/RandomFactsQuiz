from sqlalchemy.ext.asyncio import AsyncSession

from random_quiz.db.models import User, Quiz, Question
from random_quiz.schemas.quiz.quiz import Quiz as QuizShema


async def add_quiz(session: AsyncSession, user: User, num_questions: int):
    quiz = Quiz(user_id=user.id, num_questions=num_questions)
    session.add(quiz)
    await session.commit()
    await session.refresh(quiz)
    return QuizShema.from_orm(quiz)


async def add_questions(session: AsyncSession, questions: list, quiz: Quiz):
    for index, question_data in enumerate(questions):
        correct_bool = True
        if question_data['correct_answer'] == 'False':
            correct_bool = False
        question = Question(
            quiz_id=quiz.id,
            text=question_data['question'],
            correct_answer=correct_bool,
            question_index=index
        )
        session.add(question)
    await session.commit()
