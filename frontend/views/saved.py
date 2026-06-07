import streamlit as st
import api

from components.post_card import render_post_card
from utils import alert


def render_saved_page():
    st.markdown(
        '<div class="section-title">Saved</div>'
        '<div class="section-subtitle">Your thought archive</div>',
        unsafe_allow_html=True,
    )

    res_saved = api.api_get_saved_posts(st.session_state.token)

    if res_saved.status_code != 200:
        alert("Gagal memuat post tersimpan.", "err")
        return

    saved = res_saved.json()

    if not saved:
        st.markdown(
            '<div class="empty-state">No saved posts</div>',
            unsafe_allow_html=True,
        )
    else:
        for index, post in enumerate(saved):
            render_post_card(
                post,
                show_actions=True,
                ctx=f"saved_{index}_",
            )