from sqlalchemy.ext.asyncio import AsyncSession

from random_quiz.schemas.auth.user import User
from random_quiz.utils.get_question import get_random_questions
from random_quiz.utils.quiz.databse import add_quiz, add_questions


async def generate_quiz(number_of_questions: int,
                        session: AsyncSession, user: User):
    questions = get_random_questions(number_of_questions)
    quiz = await add_quiz(session, user, number_of_questions)
    await add_questions(session, questions, quiz)
    return quiz
