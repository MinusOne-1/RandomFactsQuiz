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


def main():
    st.title("User Authentication")
    # Initialize session state

    option = st.sidebar.selectbox("Menu",
                                  ["Login",
                                   "Register",
                                   "User Info",
                                   'Generate Quiz'])

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
                    else:
                        st.error("Failed to generate quiz!")
                else:
                    st.warning("Please login to generate a quiz")
            else:
                st.warning("Please enter the number of questions!")


if __name__ == "__main__":
    main()
