import streamlit as st
import boto3

USERS = {
    "nouhaila": {
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
    st.title("🔐 Authentification AWS")
    username = st.text_input("Utilisateur")
    password = st.text_input("Mot de passe AWS (Access Key)", type="password")

    if st.button("Connexion"):
        user = USERS.get(username)
        if user and user["aws_access_key"] == password:
            st.session_state["user"] = username
            st.session_state["aws_key"] = user["aws_access_key"]
            st.session_state["aws_secret"] = user["aws_secret_key"]
            st.success(f"Bienvenue, {username}")
            st.experimental_rerun()
        else:
            st.error("Identifiants invalides")

def get_aws_session():
    if "aws_key" in st.session_state and "aws_secret" in st.session_state:
        return boto3.Session(
            aws_access_key_id=st.session_state["aws_key"],
            aws_secret_access_key=st.session_state["aws_secret"],
            region_name="us-east-1"
        )
    else:
        return None
