import streamlit as st
import api
from utils import alert


def render_auth_page():
    st.markdown(
        '<div class="section-title">Login & Sign Up</div>'
        '<div class="section-subtitle">Access your timeline</div>',
        unsafe_allow_html=True,
    )

    tab_in, tab_up = st.tabs(["Login", "Sign Up"])

    with tab_in:
        with st.form("form_login"):
            email = st.text_input("Email address", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submit = st.form_submit_button("Enter", use_container_width=True)

        if submit:
            if not email or not password:
                alert("Isi email dan password dulu.", "err")
            else:
                res = api.api_login(email, password)
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.token = data["access_token"]
                    st.session_state.user = data["user"]
                    st.rerun()
                else:
                    alert(res.json().get("detail", "Login gagal"), "err")

    with tab_up:
        with st.form("form_register"):
            username = st.text_input("Username", placeholder="nama_kamu")
            email_r = st.text_input("Email", placeholder="kamu@email.com")
            pass_r = st.text_input("Password", type="password", placeholder="Min. 6 karakter")
            submit_r = st.form_submit_button("Create account", use_container_width=True)

        if submit_r:
            if not username or not email_r or not pass_r:
                alert("Semua field harus diisi.", "err")
            elif len(pass_r) < 6:
                alert("Password minimal 6 karakter.", "err")
            else:
                res = api.api_register(username, email_r, pass_r)
                if res.status_code == 201:
                    alert("Akun berhasil dibuat. Silakan login.")
                else:
                    alert(res.json().get("detail", "Gagal daftar"), "err")