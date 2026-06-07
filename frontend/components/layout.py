import streamlit as st
from session import logout
from utils import clean


def render_topbar():
    st.markdown('<div class="main-shell">', unsafe_allow_html=True)

    left_col, center_col, right_col = st.columns([2, 2, 2])

    with left_col:
        if st.session_state.user:
            if st.button("Logout", key="topbar_logout", icon=":material/logout:"):
                logout()

    with center_col:
        if st.button("◆ Y", key="topbar_home", use_container_width=True):
            st.session_state.view_profile = None
            st.session_state.edit_post_id = None
            st.rerun()

    with right_col:
        if st.session_state.user:
            username = clean(st.session_state.user["username"])
            if st.button(f"@{username}", key="topbar_profile",
                         use_container_width=True, icon=":material/person:"):
                st.session_state.view_profile = st.session_state.user["username"]
                st.rerun()

    st.markdown('<div class="page-pad">', unsafe_allow_html=True)


def close_shell():
    st.markdown("</div></div>", unsafe_allow_html=True)