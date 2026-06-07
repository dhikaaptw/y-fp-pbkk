import streamlit as st

def init_session():
    for key, value in [
        ("token", None),
        ("user", None),
        ("edit_post_id", None),
        ("open_comments", set()),
        ("view_profile", None),
    ]:
        if key not in st.session_state:
            st.session_state[key] = value


def logout():
    for key in ["token", "user", "edit_post_id", "view_profile"]:
        st.session_state[key] = None
    st.session_state.open_comments = set()
    st.rerun()