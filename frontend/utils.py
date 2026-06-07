import html
from datetime import datetime
import streamlit as st


def clean(value):
    return html.escape(str(value or ""))


def fmt_time(iso_str):
    try:
        dt = datetime.fromisoformat(iso_str)
        diff = datetime.utcnow() - dt
        seconds = diff.total_seconds()

        if seconds < 60:
            return "now"
        if seconds < 3600:
            return f"{int(seconds // 60)}m"
        if seconds < 86400:
            return f"{int(seconds // 3600)}h"
        if diff.days < 7:
            return f"{diff.days}d"

        return dt.strftime("%b %d")
    except Exception:
        return clean(iso_str)


def alert(msg, kind="ok"):
    cls = "alert-ok" if kind == "ok" else "alert-err"
    st.markdown(
        f'<div class="{cls}">{clean(msg)}</div>',
        unsafe_allow_html=True,
    )