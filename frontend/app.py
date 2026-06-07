import streamlit as st

from components.auth import render_auth_page
from components.layout import close_shell, render_topbar
from session import init_session
from styles import load_styles
from views.home import render_home_page
from views.profile import render_profile_page
from views.saved import render_saved_page

st.set_page_config(
    page_title="Y",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed",
)

load_styles()
init_session()
render_topbar()

if not st.session_state.token:
    render_auth_page()
    close_shell()
    st.stop()

if st.session_state.view_profile:
    render_profile_page()
    close_shell()
    st.stop()

tab_home, tab_saved = st.tabs(["Home", "Saved"])

with tab_home:
    render_home_page()

with tab_saved:
    render_saved_page()

close_shell()