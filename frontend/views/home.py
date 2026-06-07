import streamlit as st
import api
from components.layout import close_shell
from components.post_card import render_post_card
from utils import alert, clean


def render_home_page():
    render_composer()
    render_feed()


def render_composer():
    st.markdown(
        '<div class="composer"><div class="section-title">Share a thought</div>',
        unsafe_allow_html=True,
    )

    with st.form("form_post", clear_on_submit=True):
        content = st.text_area(
            "", placeholder="What are you thinking?",
            max_chars=280, height=86, label_visibility="collapsed",
        )

        col_counter, col_button = st.columns([5, 1])

        with col_counter:
            st.markdown(
                f'<div class="char-count">{len(content)}/280</div>',
                unsafe_allow_html=True,
            )

        with col_button:
            post_btn = st.form_submit_button("Post", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if post_btn:
        if not content.strip():
            alert("Post tidak boleh kosong.", "err")
        else:
            res = api.api_create_post(content, st.session_state.token)
            if res.status_code == 201:
                st.rerun()
            else:
                alert(res.json().get("detail", "Gagal posting"), "err")


def render_feed():
    search_q = st.text_input(
        "", placeholder="Search by username...",
        label_visibility="collapsed", key="search_inp",
    )

    if search_q.strip():
        res_p = api.api_search_posts(search_q.strip(), st.session_state.token)
        st.markdown(
            f'<div class="section-title">Results for @{clean(search_q)}</div>',
            unsafe_allow_html=True,
        )
    else:
        res_p = api.api_get_posts(st.session_state.token)
        st.markdown(
            '<div class="section-title">Feed</div>'
            '<div class="section-subtitle">Recent posts</div>',
            unsafe_allow_html=True,
        )

    if res_p.status_code != 200:
        alert("Gagal memuat post. Pastikan backend berjalan.", "err")
        close_shell()
        st.stop()

    posts = res_p.json()

    if not posts:
        st.markdown('<div class="empty-state">No posts yet</div>', unsafe_allow_html=True)

    for index, post in enumerate(posts):
        render_post_card(post, show_actions=True, ctx=f"home_{index}_")