from random_quiz.endpoints.auth import api_router as auth_router
from random_quiz.endpoints.ping import api_router as application_health_router
from random_quiz.endpoints.quiz import quiz_router

list_of_routes = [
    application_health_router,
    auth_router,
    quiz_router
]

__all__ = [
    "list_of_routes",
]
