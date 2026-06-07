import streamlit as st


def load_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

:root {
  --bg: #0a0a0a;
  --panel: #101010;
  --panel-soft: #151515;
  --line: #2a2a2a;
  --line-strong: #3b3b3b;
  --text: #f1f1f1;
  --muted: #969696;
  --faint: #5e5e5e;
  --black: #050505;
  --mono: 'IBM Plex Mono', monospace;
  --sans: 'Inter', system-ui, sans-serif;
}

.stApp {
  background-color: var(--bg);
  background-image: radial-gradient(rgba(255,255,255,0.11) 1px, transparent 1px);
  background-size: 10px 10px;
}

/* ... (isi lengkap styles.py) */
</style>
""", unsafe_allow_html=True)