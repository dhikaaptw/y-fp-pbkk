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
  --sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

html, body, [class*="css"] {
  font-family: var(--sans);
  color: var(--text);
}

.stApp {
  background-color: var(--bg);
  background-image: radial-gradient(rgba(255,255,255,0.11) 1px, transparent 1px);
  background-size: 10px 10px;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
  max-width: 760px;
  padding-top: 2.4rem;
  padding-bottom: 4rem;
}

/* =========================
   Functional Topbar
========================= */

.main-shell > div[data-testid="stHorizontalBlock"] {
  height: 38px;
  border-bottom: 1px solid var(--line);
  margin-bottom: 1.15rem;
  padding: 0 1rem;
  align-items: center;
}

.main-shell > div[data-testid="stHorizontalBlock"] .stButton > button {
  background: transparent !important;
  border: none !important;
  color: var(--muted) !important;
  padding: 0.15rem 0.35rem !important;
  font-family: var(--mono) !important;
  font-size: 0.63rem !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
}

.main-shell > div[data-testid="stHorizontalBlock"] .stButton > button:hover {
  color: var(--text) !important;
  background: transparent !important;
}

.main-shell > div[data-testid="stHorizontalBlock"] div:nth-child(2) .stButton > button {
  color: var(--text) !important;
  font-weight: 700 !important;
  font-size: 0.9rem !important;
}

.topbar {
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--line);
  position: relative;
  margin-bottom: 1.15rem;
}

.brand {
  font-family: var(--mono);
  font-size: 0.9rem;
  font-weight: 700;
  letter-spacing: -0.04em;
  color: var(--text);
}

.brand::before {
  content: '◆';
  font-size: 0.68rem;
  margin-right: 0.35rem;
}

.topbar-right {
  position: absolute;
  right: 1rem;
  top: 0.46rem;
  font-family: var(--mono);
  font-size: 0.63rem;
  color: var(--muted);
}

.page-pad { padding: 0 1.7rem; }

.section-title {
  font-family: var(--mono);
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--text);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin: 0.45rem 0 0.25rem;
}

.section-subtitle {
  font-family: var(--mono);
  color: var(--faint);
  font-size: 0.58rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 1rem;
}

.stTabs [data-baseweb="tab-list"] {
  gap: 0.45rem;
  border-bottom: 1px solid var(--line);
  padding-bottom: 0.55rem;
}

.stTabs [data-baseweb="tab"] {
  height: auto;
  background: transparent;
  border: 1px solid var(--line);
  border-radius: 0;
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.62rem;
  font-weight: 600;
  padding: 0.28rem 0.64rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.stTabs [aria-selected="true"] {
  background: var(--text) !important;
  color: var(--black) !important;
  border-color: var(--text) !important;
}

.stTextInput input,
.stTextArea textarea {
  background: var(--panel) !important;
  border: 1px solid var(--line) !important;
  border-radius: 0 !important;
  color: var(--text) !important;
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  box-shadow: none !important;
}

.stTextArea textarea { min-height: 86px !important; }

.stTextInput input:focus,
.stTextArea textarea:focus {
  border-color: var(--line-strong) !important;
  box-shadow: none !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder { color: var(--faint) !important; }

label[data-testid="stWidgetLabel"] {
  font-family: var(--mono) !important;
  color: var(--muted) !important;
  font-size: 0.62rem !important;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.stButton > button,
.stFormSubmitButton > button {
  border-radius: 0 !important;
  border: 1px solid var(--line) !important;
  background: var(--panel) !important;
  color: var(--muted) !important;
  font-family: var(--mono) !important;
  font-size: 0.62rem !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
  min-height: 0 !important;
  padding: 0.35rem 0.62rem !important;
  line-height: 1.35 !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
  border-color: var(--text) !important;
  background: var(--text) !important;
  color: var(--black) !important;
}

.stFormSubmitButton > button[kind="primaryFormSubmit"],
.stFormSubmitButton > button {
  background: var(--text) !important;
  border-color: var(--text) !important;
  color: var(--black) !important;
}

.composer {
  border-bottom: 1px solid var(--line);
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}

.post-card {
  border-bottom: 1px solid var(--line);
  padding: 0.9rem 0 0.75rem;
}

.post-card:hover { border-color: var(--line-strong); }

.post-mine {
  border-left: 2px solid var(--text);
  padding-left: 0.75rem;
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 0.42rem;
  margin-bottom: 0.45rem;
}

.post-username {
  font-family: var(--mono);
  font-size: 0.66rem;
  font-weight: 700;
  color: var(--text);
  text-transform: uppercase;
}

.post-time, .dot, .edited-tag {
  font-family: var(--mono);
  font-size: 0.58rem;
  color: var(--faint);
  text-transform: uppercase;
}

.post-content {
  font-size: 0.76rem;
  line-height: 1.62;
  color: var(--text);
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.comment-section {
  border: 1px solid var(--line);
  background: var(--panel);
  padding: 0.62rem 0.72rem;
  margin: 0.55rem 0 0.35rem;
}

.comment-item {
  display: flex;
  gap: 0.65rem;
  padding: 0.42rem 0;
  border-bottom: 1px solid var(--line);
  align-items: flex-start;
}

.comment-item:last-child { border-bottom: 0; }

.comment-user {
  min-width: 70px;
  font-family: var(--mono);
  font-size: 0.6rem;
  font-weight: 700;
  color: var(--muted);
  text-transform: uppercase;
}

.comment-text {
  flex: 1;
  color: var(--text);
  font-size: 0.72rem;
  line-height: 1.45;
}

.comment-time {
  font-family: var(--mono);
  font-size: 0.55rem;
  color: var(--faint);
  white-space: nowrap;
}

.profile-card {
  border-bottom: 1px solid var(--line);
  padding: 1.2rem 0 1.35rem;
  margin-bottom: 1rem;
}

.profile-row {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.avatar-box {
  width: 58px;
  height: 58px;
  border: 1px solid var(--line-strong);
  background: linear-gradient(135deg, #191919, #080808);
  display: grid;
  place-items: center;
  font-family: var(--mono);
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--text);
}

.profile-handle {
  font-family: var(--mono);
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 0.4rem;
}

.profile-bio {
  max-width: 460px;
  color: var(--muted);
  font-size: 0.72rem;
  line-height: 1.55;
  margin-bottom: 0.8rem;
}

.profile-stats { display: flex; gap: 1.55rem; }

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.04rem;
}

.stat-num {
  font-family: var(--mono);
  font-size: 0.76rem;
  font-weight: 700;
  color: var(--text);
}

.stat-label {
  font-family: var(--mono);
  font-size: 0.52rem;
  color: var(--faint);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.alert-ok, .alert-err {
  border-radius: 0;
  padding: 0.55rem 0.8rem;
  font-family: var(--mono);
  font-size: 0.65rem;
  margin: 0.5rem 0;
}

.alert-ok {
  background: #0e1a12;
  border: 1px solid #284431;
  color: #8fd8a7;
}

.alert-err {
  background: #1d0d0d;
  border: 1px solid #4c2222;
  color: #e08383;
}

.char-count {
  font-family: var(--mono);
  font-size: 0.58rem;
  color: var(--faint);
  text-align: right;
  padding-top: 0.28rem;
}

.empty-state {
  text-align: center;
  color: var(--faint);
  font-family: var(--mono);
  font-size: 0.65rem;
  padding: 2.5rem 0;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.small-note {
  font-family: var(--mono);
  color: var(--faint);
  font-size: 0.58rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
                
/* =========================
   Minimal Box Action Buttons
========================= */

.post-action-row div[data-testid="stHorizontalBlock"] {
  gap: 0.65rem;
}

.post-action-row .stButton > button {
  background: #000000 !important;
  border: 1px solid var(--line) !important;
  border-radius: 0 !important;
  color: var(--text) !important;

  padding: 0.18rem 0.45rem !important;
  min-height: 28px !important;

  font-family: var(--mono) !important;
  font-size: 0.65rem !important;
  font-weight: 500 !important;
  text-transform: none !important;
  letter-spacing: 0 !important;

  box-shadow: none !important;
}

.post-action-row .stButton > button:hover {
  background: #050505 !important;
  border-color: var(--text) !important;
  color: var(--text) !important;
}

.post-action-row .stButton > button:focus {
  box-shadow: none !important;
  outline: none !important;
}

.post-action-row .stButton > button span {
  gap: 0.3rem !important;
}

.post-action-row .stButton > button svg {
  width: 16px !important;
  height: 16px !important;
}
</style>
""", unsafe_allow_html=True)