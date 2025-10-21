import os
import streamlit as st

# ---- Page / app config ----
st.set_page_config(page_title="Data Analytics • AI", page_icon="💠", layout="wide")

# ---- Simple CSS palette (teal + purple) ----
st.markdown(
    """
    <style>
    :root{
      --primary:#00897b;
      --primary-dark:#00695c;
      --accent:#7e57c2;
      --text:#111827;
      --bg:#f6f8fb;
      --card:#ffffff;
    }
    .stApp { background-color: var(--bg); color: var(--text); }
    h1,h2,h3,h4 { color: var(--primary-dark) !important; font-weight:700; }
    .stButton>button {
      background: var(--primary) !important;
      color: white !important;
      border-radius: 8px !important;
      padding: 0.55em 1.05em !important;
      border: none !important;
    }
    .stButton>button:hover { background: var(--primary-dark) !important; transform: scale(1.02); }
    .sidebar .sidebar-content { background-color: var(--card); }
    .stMetric > div { background-color: var(--card); border-radius:8px; padding:8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- Session state & roles ----
if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "PC", "Professor", "Team", "Admin", "Decision Maker", "Citizen"]

# ---- Login / Logout ----
def login():
    st.header("🔐 Log in")
    role = st.selectbox("Choose your role", ROLES, index=0)
    if st.button("Log in"):
        st.session_state.role = role
        st.experimental_rerun()

def logout():
    st.header("🚪 Log out")
    if st.button("Confirm log out"):
        st.session_state.role = None
        st.experimental_rerun()

# ---- Inline page implementations (no external files required) ----
def page_dashboard():
    st.title("📊 Dashboard")
    st.subheader("Overview and KPIs")
    st.write("Quick summary and high-level indicators for decision makers.")
    cols = st.columns(3)
    cols[0].metric("Public Health", "87%", "+2%")
    cols[1].metric("Education Index", "93%", "+1.5%")
    cols[2].metric("Environmental Score", "76%", "—")
    st.divider()
    st.write("Add charts and widgets here (placeholders).")

def page_maps():
    st.title("🗺️ Maps")
    st.write("Interactive city maps, layers and geographic visualizations.")
    st.info("This is a placeholder for your map components.")

def page_maps2():
    st.title("🌎 Other maps")
    st.write("Regional comparisons and alternative map views.")
    st.info("Placeholder for secondary maps.")

def page_ml_analysis():
    st.title("🤖 Machine Learning")
    st.write("Tools for model training, validation and performance review.")
    st.info("Upload datasets and run experiments here (placeholder).")

def page_eda():
    st.title("🔬 Exploratory Data Analysis")
    st.write("Correlation matrices, histograms, and descriptive stats.")
    st.info("EDA widgets and plots go here.")

def page_settings():
    st.title("⚙️ Settings")
    st.write("User preferences, theme and other options.")
    st.checkbox("Enable notifications")
    st.selectbox("Theme", ["Default", "Teal-Purple (current)"])

# ---- Create Page objects using functions (not file paths) ----
role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings_page = st.Page(page_settings, title="Settings", icon=":material/settings:")

# keep titles/icons similar to your original intention
visualization_page = st.Page(page_dashboard, title="Dashboard", icon=":material/monitoring:", default=(role == "Decision Maker"))
maps_page = st.Page(page_maps, title="Maps", icon=":material/map:", default=(role == "Citizen"))
maps2_page = st.Page(page_maps2, title="Other maps", icon=":material/public:", default=(role == "Citizen"))
ml_page = st.Page(page_ml_analysis, title="Machine Learning", icon=":material/neurology:", default=(role == "Admin"))
eda_page = st.Page(page_eda, title="Exploratory Data Analysis", icon=":material/insights:", default=(role == "Admin"))

# ---- Groups (same structure) ----
account_pages = [logout_page, settings_page]
visualization_pages = [visualization_page, maps_page, maps2_page]
ml_pages = [ml_page]
eda_pages = [eda_page]

# ---- Header & sidebar (keeps same structure but nicer) ----
# show logo if image exists; otherwise skip silently
logo_path = "images/horizontal_blue.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=320)

st.title("Data Analytics • AI")

with st.sidebar:
    st.header("Menu")
    st.caption("Available sections:")
    st.markdown(
        "- **Visualization**: Dashboards and maps\n"
        "- **EDA**: Data exploration\n"
        "- **Machine Learning**: Modeling and evaluation\n"
        "- **Account**: Settings and log out"
    )
    st.divider()
    st.caption(f"Current role: {role if role else 'Not logged in'}")
    st.divider()
    # Keep login/logout accessible in sidebar
    if role:
        if st.button("Log out (sidebar)"):
            st.session_state.role = None
            st.experimental_rerun()
    else:
        if st.button("Go to login"):
            # trigger main login page by routing to default (login)
            st.experimental_rerun()

# ---- Small info expander sections (same idea) ----
with st.expander("About this app"):
    st.write(
        "Includes Visualization, EDA, and Machine Learning modules. "
        "Select your role to enable corresponding sections."
    )

with st.expander("Quick access"):
    st.write("Go to Account → Settings to update your preferences or log out.")

# ---- Navigation logic (keeps same role mappings; minimally changed) ----
page_dict = {}

# Map old roles PC/Professor/Team to the new role names if present in session,
# but keep logic flexible — the page access logic below uses the actual role strings
# you set in session_state (so you can still use PC/Professor/Team if you prefer).
# Example: treat "Professor" and "Team" similar to "Admin" for this mapping:
if role in ["Professor", "Team", "Admin"]:
    page_dict["EDA"] = eda_pages
if role in ["Professor", "Team", "PC", "Decision Maker", "Admin"]:
    page_dict["Visualization"] = visualization_pages
if role in ["Professor", "Team", "Admin"]:
    page_dict["Machine Learning"] = ml_pages

# ---- Routing ----
if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    # show login page when no accessible pages for current role
    pg = st.navigation([st.Page(login, title="Login", icon=":material/login:")])

pg.run()
