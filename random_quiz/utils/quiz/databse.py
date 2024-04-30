from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from random_quiz.db.models import User, Quiz, Question
from random_quiz.schemas.quiz.quiz import Quiz as QuizSchema
from random_quiz.schemas.quiz.question import Question as QuestionSchema


async def add_quiz(session: AsyncSession, user: User, num_questions: int):
    quiz = Quiz(user_id=user.id, num_questions=num_questions)
    session.add(quiz)
    await session.commit()
    await session.refresh(quiz)
    return QuizSchema.from_orm(quiz)


async def get_untaked_quiz_from_db(
        session: AsyncSession, user: User) -> QuizSchema:
    stmt = select(Quiz).where(
        Quiz.user_id == user.id,
        Quiz.num_correct.is_(None))
    result = await session.execute(stmt)
    quiz = result.scalars().first()
    return QuizSchema.from_orm(quiz) if quiz else None


async def update_quiz_correct_answer_db(
        session: AsyncSession,
        quiz_id: UUID4, correct_answer: int):
    quiz = await session.get(Quiz, quiz_id)
    if quiz:
        quiz.num_correct = correct_answer
        await session.commit()
        return True
    else:
        return False


async def get_solved_quizzes_for_user_db(
        session: AsyncSession,
        user: User) -> list[QuizSchema]:
    stmt = select(Quiz).filter(
        Quiz.user_id == user.id,
        Quiz.num_correct.isnot(None))
    result = await session.execute(stmt)
    quizzes = result.scalars().all()
    quizzes = [QuizSchema.from_orm(i) for i in quizzes]
    return quizzes


async def check_user_association_with_quiz_db(
        session: AsyncSession,
        user: User, quiz_id: UUID4) -> bool:
    # Retrieve the quiz by ID
    quiz = await session.get(Quiz, quiz_id)
    if quiz:
        return quiz.user_id == user.id
    else:
        return False


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


async def get_question_n_for_quiz_from_db(
        session: AsyncSession,
        quiz_id: UUID4,
        question_index: int) -> QuestionSchema:
    stmt = select(Question).where(Question.quiz_id == quiz_id,
                                  Question.question_index == question_index)
    result = await session.execute(stmt)
    question = result.scalars().first()
    return QuestionSchema.from_orm(question) if question else None
