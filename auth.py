import streamlit as st
import boto3

USERS = {
    "admin-nouhaila": {
        "aws_access_key": st.secrets["nouhaila_aws_key"],
        "aws_secret_key": st.secrets["nouhaila_aws_secret"]
    },
    "data-analyst": {
        "aws_access_key": st.secrets["analyst_aws_key"],
        "aws_secret_key": st.secrets["analyst_aws_secret"]
    },
    "data-scientist": {
        "aws_access_key": st.secrets["scientist_aws_key"],
        "aws_secret_key": st.secrets["scientist_aws_secret"]
    }
}

def login():
    st.markdown(
    """
    <h2 style='text-align: center; color: blue;'>
        Welcome to AWS-Streamlit APP
    </h2>
    """,
    unsafe_allow_html=True
    )

    username = st.text_input("Username")
    access_key_input = st.text_input("Access Key ID", type="password")
    secret_key_input = st.text_input("Secret Access Key", type="password")

    if st.button("Connexion"):
        user = USERS.get(username)
        if user and \
           user["aws_access_key"].strip() == access_key_input.strip() and \
           user["aws_secret_key"].strip() == secret_key_input.strip():
            st.session_state["user"] = username
            st.session_state["aws_key"] = user["aws_access_key"]
            st.session_state["aws_secret"] = user["aws_secret_key"]
            st.success(f"Bienvenue, {username}")
            st.experimental_rerun()
            return
        else:
            st.error("Identifiants invalides")


def get_aws_session():
    if "aws_key" in st.session_state and "aws_secret" in st.session_state:
        try:
            session = boto3.Session(
                aws_access_key_id=st.session_state["aws_key"],
                aws_secret_access_key=st.session_state["aws_secret"],
                region_name="us-east-1"
            )
            return session
        except Exception as e:
            st.error(f"Erreur de connexion AWS: {e}")
            return None
    return None
