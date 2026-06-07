import streamlit as st
import api

from components.post_card import render_post_card
from utils import alert, clean


def render_profile_page():
    uname = st.session_state.view_profile

    if st.button("Back", key="back_profile", icon=":material/arrow_back:"):
        st.session_state.view_profile = None
        st.rerun()

    res = api.api_get_profile(uname, st.session_state.token)

    if res.status_code == 200:
        profile = res.json()
        render_profile_header(profile)
        render_follow_button(profile, uname)
        render_profile_posts(uname)
    else:
        alert("User tidak ditemukan.", "err")


def render_profile_header(profile):
    initial = clean(profile["username"][:1].upper())

    st.markdown(
        f"""
        <div class="profile-card">
          <div class="profile-row">
            <div class="avatar-box">{initial}</div>
            <div>
              <div class="profile-handle">@{clean(profile['username'])}</div>
              <div class="profile-bio">Minimal microblog profile focused on simple posts, replies, saved thoughts, and following.</div>
              <div class="profile-stats">
                <div class="stat-item"><span class="stat-num">{profile['posts_count']}</span><span class="stat-label">Posts</span></div>
                <div class="stat-item"><span class="stat-num">{profile['followers_count']}</span><span class="stat-label">Followers</span></div>
                <div class="stat-item"><span class="stat-num">{profile['following_count']}</span><span class="stat-label">Following</span></div>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_follow_button(profile, uname):
    is_me = profile["id"] == st.session_state.user["id"]

    if is_me:
        return

    label = "Unfollow" if profile["is_following"] else "Follow"
    icon = ":material/person_remove:" if profile["is_following"] else ":material/person_add:"

    if st.button(label, key="follow_btn", icon=icon, use_container_width=True):
        res = api.api_toggle_follow(uname, st.session_state.token)

        if res.status_code == 200:
            st.rerun()


def render_profile_posts(uname):
    st.markdown(
        '<div class="section-title">Posts</div>',
        unsafe_allow_html=True,
    )

    res = api.api_search_posts(uname, st.session_state.token)

    if res.status_code == 200:
        user_posts = [
            post
            for post in res.json()
            if post["owner"]["username"] == uname
        ]

        if not user_posts:
            st.markdown(
                '<div class="empty-state">No posts yet</div>',
                unsafe_allow_html=True,
            )
        else:
            for index, post in enumerate(user_posts):
                render_post_card(
                    post,
                    show_actions=True,
                    ctx=f"profile_{index}_",
                )
    else:
        alert("Gagal memuat postingan.", "err")