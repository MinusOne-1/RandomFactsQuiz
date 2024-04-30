from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from random_quiz.schemas.auth.user import User
from random_quiz.utils.get_question import get_random_questions
from random_quiz.utils.quiz.databse import add_quiz, add_questions, \
    get_untaked_quiz_from_db, \
    get_question_n_for_quiz_from_db, \
    check_user_association_with_quiz_db, \
    update_quiz_correct_answer_db


async def generate_quiz(number_of_questions: int,
                        session: AsyncSession, user: User):
    questions = get_random_questions(number_of_questions)
    quiz = await add_quiz(session, user, number_of_questions)
    await add_questions(session, questions, quiz)
    return quiz


async def get_untaked_quiz(user: User, session: AsyncSession):
    quiz = await get_untaked_quiz_from_db(session, user)
    return quiz


async def update_quiz_correct_answer(
        user: User, quiz_id: UUID4,
        correct_answer: int, session: AsyncSession):
    if check_user_association_with_quiz_db(session, user, quiz_id):
        quiz = await update_quiz_correct_answer_db(
            session, quiz_id, correct_answer)
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such question in this quiz")
        return quiz
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of the quiz",
        )


async def get_question_N_for_quiz(
        session: AsyncSession,
        user: User, quiz_id: UUID4,
        question_indx: int):
    if check_user_association_with_quiz_db(session, user, quiz_id):
        question = await get_question_n_for_quiz_from_db(
            session,
            quiz_id,
            question_indx)
        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such question in this quiz", )
        return question
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of the quiz",
        )
