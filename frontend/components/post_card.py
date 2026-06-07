import streamlit as st
import api
from utils import alert, clean, fmt_time


 def render_post_card(post, show_actions=True, ctx=""):
    pid = f"{ctx}{post['id']}"
    is_mine = st.session_state.user and post["owner_id"] == st.session_state.user["id"]
    card_cls = "post-card post-mine" if is_mine else "post-card"
    show_comments = post["id"] in st.session_state.open_comments
    edited = post.get("updated_at") and post["updated_at"] != post["created_at"]

    if st.session_state.edit_post_id == post["id"]:
        render_edit_post_form(post, pid)
        return

    edited_tag = '<span class="edited-tag">edited</span>' if edited else ""
    username = clean(post["owner"]["username"])
    content = clean(post["content"])

    st.markdown(
        f"""
        <div class="{card_cls}">
          <div class="post-meta">
            <span class="post-username">@{username}</span>
            <span class="dot">·</span>
            <span class="post-time">{fmt_time(post['created_at'])}</span>
            {edited_tag}
          </div>
          <p class="post-content">{content}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not show_actions:
        return
        