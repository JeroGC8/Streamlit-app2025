import streamlit as st

# =========================
# Page + Session bootstrap
# =========================
st.set_page_config(page_title="Settings", page_icon="⚙️", layout="centered")

# Example role value if not present
st.session_state.setdefault("role", "guest")

# "auto" follows OS; "light"/"dark" force those palettes
st.session_state.setdefault("theme_mode", "auto")  # "auto" | "light" | "dark"


# =========================
# Theming helper (CSS)
# =========================
def theme_css(mode: str) -> str:
    """
    Returns a <style> block that:
      - Defines light and dark color tokens with CSS variables.
      - Applies to Streamlit's main area and sidebar via stable `data-testid` hooks.
      - Supports 'auto' (prefers-color-scheme), 'light', and 'dark'.
    """
    return f"""
<style>
/* ---------- 1) Base tokens (Light defaults) ---------- */
:root {{
  --bg: #ffffff;
  --bg-alt: #f6f7fb;   /* sidebar / secondary */
  --fg: #111111;
  --muted: #475569;
  --primary: #3b82f6;
  --border: #e5e7eb;
}}

@media (prefers-reduced-motion: no-preference) {{
  [data-testid="stAppViewContainer"],
  [data-testid="stSidebar"] {{
    transition: background-color .2s ease, color .2s ease, border-color .2s ease;
  }}
}}

/* ---------- 2) Conditional palettes ---------- */
{("""
/* AUTO: follow OS preference for dark */
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0E1117;
    --bg-alt: #151923;
    --fg: #E6E9EF;
    --muted: #a0a3ad;
    --primary: #60a5fa;
    --border: #2a2f3a;
  }
}
""" if mode == "auto" else "")}

{("""
/* FORCE LIGHT */
:root {
  --bg: #ffffff;
  --bg-alt: #f6f7fb;
  --fg: #111111;
  --muted: #475569;
  --primary: #3b82f6;
  --border: #e5e7eb;
}
""" if mode == "light" else "")}

{("""
/* FORCE DARK */
:root {
  --bg: #0E1117;
  --bg-alt: #151923;
  --fg: #E6E9EF;
  --muted: #a0a3ad;
  --primary: #60a5fa;
  --border: #2a2f3a;
}
""" if mode == "dark" else "")}

/* ---------- 3) Apply tokens to the app ---------- */

/* Main content area */
[data-testid="stAppViewContainer"] {{
  background: var(--bg);
  color: var(--fg);
}}
.block-container {{
  background: var(--bg);
  color: var(--fg);
}}

a, .stMarkdown a {{
  color: var(--primary);
}}

/* Inputs in main area */
div[data-baseweb="input"] input,
textarea, .stTextInput input, .stNumberInput input, .stTextArea textarea,
.css-10trblm, .stSelectbox div[role="combobox"], .stMultiSelect div[role="combobox"] {{
  background: var(--bg-alt) !important;
  color: var(--fg) !important;
  border: 1px solid var(--border) !important;
}}

.stButton > button, .stDownloadButton > button {{
  background: var(--bg-alt) !important;
  color: var(--fg) !important;
  border: 1px solid var(--border) !important;
}}

hr {{
  border-color: var(--border);
}}

/* ---------- 4) Sidebar (lateral menu) fixes ---------- */
[data-testid="stSidebar"] {{
  background: var(--bg-alt);
  border-right: 1px solid var(--border);
  color: var(--fg);
}}

/* Inherit readable color for all sidebar descendants */
[data-testid="stSidebar"] * {{
  color: var(--fg) !important;
}}

[data-testid="stSidebar"] a {{
  color: var(--primary) !important;
}}

/* Sidebar inputs */
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] .stSelectbox div[role="combobox"],
[data-testid="stSidebar"] .stMultiSelect div[role="combobox"],
[data-testid="stSidebar"] .stNumberInput input {{
  background: var(--bg) !important;
  color: var(--fg) !important;
  border: 1px solid var(--border) !important;
}}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] .stDownloadButton > button {{
  background: var(--bg) !important;
  color: var(--fg) !important;
  border: 1px solid var(--border) !important;
}}

/* Radio/checkbox labels readable + highlight selected */
[data-testid="stSidebar"] label, [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
  color: var(--fg) !important;
}}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] > div[aria-checked="true"] label span {{
  font-weight: 600;
}}
</style>
"""


# Inject CSS ASAP to avoid flash
st.markdown(theme_css(st.session_state.theme_mode), unsafe_allow_html=True)


# =========================
# Sidebar (Theme + Menu)
# =========================
st.sidebar.title("Theme Settings")
mode = st.sidebar.radio(
    "Color theme",
    options=["auto", "light", "dark"],
    format_func=lambda x: {"auto": "Auto (OS)", "light": "Light", "dark": "Dark"}[x],
    index=["auto", "light", "dark"].index(st.session_state.theme_mode),
    help="Auto follows your operating system preference",
)

if mode != st.session_state.theme_mode:
    st.session_state.theme_mode = mode
    st.markdown(theme_css(mode), unsafe_allow_html=True)  # re-apply immediately

st.sidebar.markdown("---")


# =========================
# Main content
# =========================
st.header("Settings")
st.write(f"You are logged in as **{st.session_state.role}**.")
st.title("⚙️ Settings")
st.write("Adjust your preferences here.")


st.markdown("---")
