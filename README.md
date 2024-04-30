# RandomFactsQuiz
Random Facts Quiz is a simple and engaging web application that presents users with true/false trivia questions about interesting facts. This application was created as the final project of the Software Quality and Reliability course in Innopolis University.
## Install Dependencies 
to install dependencies run following command in the main directory of the project:
``` commandline
    cd some_path_for_project/RandomFactsQuiz/
    poetry install
```
## Run Locally
To run the application locally, you need to set up postgres database and create .env to write there information to connect to your db.
Then you need to apply migrations with the following commands():
```commandline
    alembic upgrade head
```
If previous step is done, then you need to start fastAPI service with the following command:
```commandline
    poetry run python -m  random_quiz
```
After that run streamlit with the following command:
```commandline
streamlit run .\random_quiz\streamlit_front.py
```

## Testing
For test use the following command:
```commandline
poetry run python -m pytest --verbosity=2 --showlocals --cov=random_quiz --cov-report html --cov-fail-under=60
```
so far coverage of the tests is 61.72%

## Linting
I use Flake8 for linting:
```commandline
flake8 .
```