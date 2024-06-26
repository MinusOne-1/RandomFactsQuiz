from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from random_quiz.config import get_settings
from random_quiz.db.connection import get_session
from random_quiz.db.models import User
from random_quiz.schemas import RegistrationForm, RegistrationSuccess, Token
from random_quiz.schemas import User as UserSchema
from random_quiz.utils.user import authenticate_user, \
    create_access_token, \
    delete_user, \
    get_current_user, \
    register_user

api_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@api_router.post(
    "/authentication",
    status_code=status.HTTP_200_OK,
    response_model=Token,
)
async def authentication(
        _: Request,
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session),
):
    """
        Authenticates a user based on provided username and password.
        On successful authentication, returns an access token.
        """
    user = await authenticate_user(session,
                                   form_data.username,
                                   form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@api_router.post(
    "/registration",
    status_code=status.HTTP_201_CREATED,
    response_model=RegistrationSuccess,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad parameters for registration",
        },
    },
)
async def registration(
        _: Request,
        registration_form: RegistrationForm = Body(...),
        session: AsyncSession = Depends(get_session),
):
    """
    Registers a new user with provided registration form data.
    """
    is_success, message = await register_user(session, registration_form)
    if is_success:
        return {"message": message}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message,
    )


@api_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def get_me(
        _: Request,
        current_user: User = Depends(get_current_user),
):
    """
       Retrieves information about the currently authenticated user.
       """
    return UserSchema.from_orm(current_user)


@api_router.delete(
    "/takeout",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def takeout(
        _: Request,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    """
    Deletes the currently authenticated user's account.
    """
    await delete_user(session, current_user)
