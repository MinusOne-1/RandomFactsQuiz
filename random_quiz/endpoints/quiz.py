from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from random_quiz.db.connection import get_session
from random_quiz.db.models import User
from random_quiz.utils.quiz.business_logic import generate_quiz
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
