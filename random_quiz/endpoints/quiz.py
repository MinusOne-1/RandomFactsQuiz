from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from random_quiz.db.connection import get_session
from random_quiz.db.models import User
from random_quiz.schemas.quiz.quiz import Quiz as QuizSchema
from random_quiz.schemas.quiz.question import Question as QuestionSchema
from random_quiz.utils.quiz.business_logic import \
    generate_quiz, \
    get_untaked_quiz, \
    get_question_N_for_quiz, \
    update_quiz_correct_answer
from random_quiz.utils.quiz.databse import get_solved_quizzes_for_user_db
from random_quiz.utils.user import get_current_user

quiz_router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"],
)


@quiz_router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate_quiz_view(
        num_questions: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)):
    # Generate random questions
    quiz = await generate_quiz(num_questions, session, current_user)
    # response with readiness of quiz
    return {"message": "Quiz generated successfully", "quiz_id": quiz.id}


@quiz_router.post("/update_corrects", status_code=status.HTTP_202_ACCEPTED)
async def update_correct_answers_for_quiz(
        quiz_id: UUID4,
        correct_answer: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)):
    await update_quiz_correct_answer(current_user,
                                     quiz_id,
                                     correct_answer,
                                     session)


@quiz_router.get("/take_a_quiz",
                 status_code=status.HTTP_200_OK,
                 response_model=QuizSchema)
async def take_a_quiz_view(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)):
    quiz = await get_untaked_quiz(current_user, session)
    if quiz is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such quiz", )
    return quiz


@quiz_router.get("/show_statistics", status_code=status.HTTP_200_OK)
async def show_statistics(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)):
    quizes = await get_solved_quizzes_for_user_db(session, current_user)
    if quizes is None:
        return []
    return quizes


@quiz_router.get("/take_question",
                 status_code=status.HTTP_200_OK,
                 response_model=QuestionSchema)
async def take_question(
        quiz_id: UUID4,
        question_indx: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)):
    question = await get_question_N_for_quiz(
        session,
        current_user,
        quiz_id,
        question_indx)
    return question
