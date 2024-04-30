import streamlit as st
import requests


# Define the base URL of your FastAPI server
BASE_URL = "http://localhost:8000/api/v1/user"


def login(username, password):
    response = requests.post(
        f"{BASE_URL}/authentication",
        data={"username": username, "password": password}
    )
    return response.json()


def register(username, password, email):
    response = requests.post(
        f"{BASE_URL}/registration",
        json={"username": username, "password": password, "email": email}
    )
    return response.json()


def get_user_info(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    return response.json()


def main():
    st.title("User Authentication")
    # Initialize session state

    option = st.sidebar.selectbox("Menu", ["Login", "Register", "User Info"])

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


if __name__ == "__main__":
    main()
