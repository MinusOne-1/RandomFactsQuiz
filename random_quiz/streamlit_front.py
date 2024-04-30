import streamlit as st
import requests

# Define the base URL of your FastAPI server
BASE_USER_URL = "http://localhost:8000/api/v1/user"
BASE_QUIZ_URL = "http://localhost:8000/api/v1/quiz"


def login(username, password):
    response = requests.post(
        f"{BASE_USER_URL}/authentication",
        data={"username": username, "password": password}
    )
    return response.json()


def register(username, password, email):
    response = requests.post(
        f"{BASE_USER_URL}/registration",
        json={"username": username, "password": password, "email": email}
    )
    return response.json()


def get_user_info(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_USER_URL}/me", headers=headers)
    return response.json()


def generate_quiz(num_questions, token):
    response = requests.post(
        f"{BASE_QUIZ_URL}/generate",
        headers={"Authorization": f"Bearer {token}"},
        params={'num_questions': num_questions}
    )
    return response.status_code


def upload_correct_answers_for_quiz(quiz_id, correct_answers, token):
    response = requests.post(
        f"{BASE_QUIZ_URL}/update_corrects",
        headers={"Authorization": f"Bearer {token}"},
        params={'quiz_id': quiz_id, 'correct_answer': correct_answers}
    )
    return response.status_code


def take_a_quiz(token):
    response = requests.get(
        f"{BASE_QUIZ_URL}/take_a_quiz",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        return response.json()


def take_question(quiz_id, question_idx, token):
    response = requests.get(
        f"{BASE_QUIZ_URL}/take_question",
        params={"quiz_id": quiz_id, "question_indx": question_idx},
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json() if response.status_code == 200 else None


def get_statistics(token):
    response = requests.get(
        f"{BASE_QUIZ_URL}/show_statistics",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json() if response.status_code == 200 else None


def main():
    st.title("User Authentication")
    # Initialize session state

    option = st.sidebar.selectbox("Menu",
                                  ["Login",
                                   "Register",
                                   "User Info",
                                   'Generate Quiz',
                                   'Show Statistics'])

    if option == "Login":
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username and password:
                response = login(username, password)
                if "access_token" in response:
                    st.session_state.token = response["access_token"]
                    st.write(st.session_state.token)
                    st.success("Login successful!")
                else:
                    st.error("Login failed!")
            else:
                st.warning("Please enter username and password!")

    elif option == "Register":
        st.header("Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        if st.button("Register"):
            if username and password and email:
                response = register(username, password, email)
                if "message" in response:
                    st.success(response["message"])
                else:
                    st.error("Registration failed!")
            else:
                st.warning("Please enter username, password, and email!")

    elif option == "User Info":
        st.header("User Information")
        if 'token' in st.session_state.keys():
            user_info = get_user_info(st.session_state.token)
            st.write("token:", st.session_state.token)
            st.write("User Info:", user_info)
        else:
            st.warning("Please login to view user information!")

    elif option == "Generate Quiz":
        if 'take_quiz' not in st.session_state.keys():
            st.header("Generate Quiz")
            num_questions = st.number_input("Number of Questions",
                                            min_value=1, step=1)
            if st.button("Generate"):
                if num_questions:
                    if 'token' in st.session_state.keys():
                        response_code = generate_quiz(num_questions,
                                                      st.session_state.token)
                        if response_code == 201:
                            st.success("Quiz generated successfully. "
                                       + "You can now take the quiz!")
                            st.session_state.quiz = \
                                take_a_quiz(st.session_state.token)
                            st.session_state.correct_answers = 0
                            st.session_state.question_indx = 0
                        else:
                            st.error("Failed to generate quiz!")
                    else:
                        st.warning("Please login to generate a quiz")
                else:
                    st.warning("Please enter the number of questions!")
    elif option == "Show Statistics":
        st.header("Show Statistics")
        statistics = get_statistics(st.session_state.token)
        if statistics:
            st.write("Statistics:")
            st.write("Correct Answers | Total Questions")
            for quiz in statistics:
                st.write(f"{quiz['num_correct']} | {quiz['num_questions']}")
    if 'quiz' in st.session_state.keys():
        st.header('Take Quiz')
        if st.button("Next question!"):
            if 'quiz_done' in st.session_state.keys():
                st.write("Correct Answers:",
                         st.session_state.correct_answers,
                         "out of",
                         st.session_state.quiz["num_questions"])
                upload_correct_answers_for_quiz(
                    st.session_state.quiz['id'],
                    st.session_state.correct_answers,
                    st.session_state.token)
                st.session_state.pop('quiz')
                st.session_state.pop('correct_answers')
                st.session_state.pop('correct_answer')
                st.session_state.pop('question_indx')
                st.session_state.pop('quiz_done')

            else:
                question_data = take_question(st.session_state.quiz['id'],
                                              st.session_state.question_indx,
                                              st.session_state.token)
                if question_data:
                    st.write("Question",
                             st.session_state.question_indx,
                             ":", question_data['text'])
                    st.session_state.correct_answer = question_data[
                        'correct_answer']

                if st.button("True"):
                    st.write(str(st.session_state.correct_answer))
                    if "True" == str(st.session_state.correct_answer):
                        st.success("The answer is correct!")
                        st.session_state.correct_answers += 1
                    else:
                        st.error("Wrong answer!..")
                elif st.button("False"):
                    if "False" == str(st.session_state.correct_answer):
                        st.success("The answer is correct!")
                        st.session_state.correct_answers += 1
                    else:
                        st.error("Wrong answer!..")
                st.session_state.question_indx += 1
                if (st.session_state.question_indx >=
                        st.session_state.quiz['num_questions']):
                    st.session_state.quiz_done = True
        elif st.button("True"):
            st.write(str(st.session_state.correct_answer))
            if "True" == str(st.session_state.correct_answer):
                st.success("The answer is correct!")
                st.session_state.correct_answers += 1
            else:
                st.error("Wrong answer!..")
        elif st.button("False"):
            if "False" == str(st.session_state.correct_answer):
                st.success("The answer is correct!")
                st.session_state.correct_answers += 1
            else:
                st.error("Wrong answer!..")


if __name__ == "__main__":
    main()
