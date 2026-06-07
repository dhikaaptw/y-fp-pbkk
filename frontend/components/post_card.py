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

    def render_post_actions(post, pid, is_mine, show_comments):
        st.markdown('<div class="post-action-row">', unsafe_allow_html=True)

    if is_mine:
        cols = st.columns([0.9, 0.9, 0.75, 0.75, 0.75, 0.75, 4.2])
    else:
        cols = st.columns([0.9, 0.9, 0.75, 0.75, 4.7])

    like_icon = ":material/favorite:" if post["is_liked"] else ":material/favorite_border:"
    comment_icon = ":material/keyboard_arrow_down:" if show_comments else ":material/chat_bubble_outline:"
    save_icon = ":material/bookmark:" if post["is_saved"] else ":material/bookmark_border:"

    with cols[0]:
        if st.button(
            str(post["like_count"]),
            key=f"like_{pid}",
            help="Like",
            icon=like_icon,
        ):
            api.api_toggle_like(post["id"], st.session_state.token)
            st.rerun()

    with cols[1]:
        if st.button(
            str(post["comment_count"]),
            key=f"cmt_{pid}",
            help="Comments",
            icon=comment_icon,
        ):
            if post["id"] in st.session_state.open_comments:
                st.session_state.open_comments.discard(post["id"])
            else:
                st.session_state.open_comments.add(post["id"])
            st.rerun()

    with cols[2]:
        if st.button(
            "",
            key=f"save_{pid}",
            help="Save",
            icon=save_icon,
        ):
            api.api_toggle_save(post["id"], st.session_state.token)
            st.rerun()

    with cols[3]:
        if st.button(
            "",
            key=f"prof_{pid}",
            help="Profile",
            icon=":material/person:",
        ):
            st.session_state.view_profile = post["owner"]["username"]
            st.rerun()

    if is_mine:
        with cols[4]:
            if st.button(
                "",
                key=f"edit_{pid}",
                help="Edit",
                icon=":material/edit:",
            ):
                st.session_state.edit_post_id = post["id"]
                st.rerun()

        with cols[5]:
            if st.button(
                "",
                key=f"del_{pid}",
                help="Delete",
                icon=":material/delete:",
            ):
                res = api.api_delete_post(post["id"], st.session_state.token)

                if res.status_code == 204:
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if show_comments:
        render_comments(post, pid, ctx)


def render_edit_post_form(post, pid):
    with st.form(f"edit_{pid}"):
        edited_content = st.text_area(
            "Edit post",
            value=post["content"],
            max_chars=280,
            height=80,
        )

        col_save, col_cancel = st.columns(2)

        with col_save:
            save_btn = st.form_submit_button("Save", use_container_width=True)

        with col_cancel:
            cancel_btn = st.form_submit_button("Cancel", use_container_width=True)

    if save_btn:
        res = api.api_update_post(post["id"], edited_content, st.session_state.token)

        if res.status_code == 200:
            st.session_state.edit_post_id = None
            st.rerun()
        else:
            alert("Gagal menyimpan.", "err")

    if cancel_btn:
        st.session_state.edit_post_id = None
        st.rerun()


def render_post_actions(post, pid, is_mine, show_comments):
    if is_mine:
        cols = st.columns([1, 1, 1, 1, 1, 1, 4.3])
    else:
        cols = st.columns([1, 1, 1, 1, 5.2])

    like_icon = ":material/favorite:" if post["is_liked"] else ":material/favorite_border:"
    comment_icon = ":material/keyboard_arrow_down:" if show_comments else ":material/chat_bubble_outline:"
    save_icon = ":material/bookmark:" if post["is_saved"] else ":material/bookmark_border:"

    with cols[0]:
        if st.button(
            str(post["like_count"]),
            key=f"like_{pid}",
            help="Like",
            icon=like_icon,
        ):
            api.api_toggle_like(post["id"], st.session_state.token)
            st.rerun()

    with cols[1]:
        if st.button(
            str(post["comment_count"]),
            key=f"cmt_{pid}",
            help="Comments",
            icon=comment_icon,
        ):
            if post["id"] in st.session_state.open_comments:
                st.session_state.open_comments.discard(post["id"])
            else:
                st.session_state.open_comments.add(post["id"])

            st.rerun()

    with cols[2]:
        if st.button(
            "",
            key=f"save_{pid}",
            help="Save",
            icon=save_icon,
        ):
            api.api_toggle_save(post["id"], st.session_state.token)
            st.rerun()

    with cols[3]:
        if st.button(
            "",
            key=f"prof_{pid}",
            help="Profile",
            icon=":material/person:",
        ):
            st.session_state.view_profile = post["owner"]["username"]
            st.rerun()

    if is_mine:
        with cols[4]:
            if st.button(
                "",
                key=f"edit_{pid}",
                help="Edit",
                icon=":material/edit:",
            ):
                st.session_state.edit_post_id = post["id"]
                st.rerun()

        with cols[5]:
            if st.button(
                "",
                key=f"del_{pid}",
                help="Delete",
                icon=":material/delete:",
            ):
                res = api.api_delete_post(post["id"], st.session_state.token)

                if res.status_code == 204:
                    st.rerun()


def render_comments(post, pid, ctx):
    comments = post.get("comments", [])
    items_html = ""

    if comments:
        for comment in comments:
            items_html += f"""
            <div class="comment-item">
              <span class="comment-user">@{clean(comment['owner']['username'])}</span>
              <span class="comment-text">{clean(comment['content'])}</span>
              <span class="comment-time">{fmt_time(comment['created_at'])}</span>
            </div>
            """
    else:
        items_html = '<div class="small-note" style="padding:0.35rem 0;">No comments yet.</div>'

    st.markdown(
        f'<div class="comment-section">{items_html}</div>',
        unsafe_allow_html=True,
    )

    if comments:
        for comment in comments:
            is_my_comment = (
                st.session_state.user
                and comment["owner_id"] == st.session_state.user["id"]
            )

            if is_my_comment:
                if st.button(
                    "Delete comment",
                    key=f"dc_{ctx}{comment['id']}",
                    icon=":material/delete:",
                ):
                    api.api_delete_comment(comment["id"], st.session_state.token)
                    st.rerun()

    with st.form(f"cmt_form_{pid}", clear_on_submit=True):
        cmt_text = st.text_input(
            "",
            placeholder="Write a comment...",
            label_visibility="collapsed",
            key=f"cmt_inp_{pid}",
        )

        cmt_send = st.form_submit_button("Send", use_container_width=True)

    if cmt_send and cmt_text.strip():
        api.api_add_comment(post["id"], cmt_text, st.session_state.token)
        st.rerun()