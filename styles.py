"""
Streamlit Design Makeup - La Forge à Data Position
Following DataGyver philosophy: framework becomes invisible to users
"""

import streamlit as st

# =============================================================================
# COLOR PALETTE - Warm neutrals
# =============================================================================
COLORS = {
    "bg_primary": "#fafaf9",
    "bg_secondary": "#f5f5f4",
    "bg_elevated": "#ffffff",
    "text_primary": "#1c1917",
    "text_secondary": "#57534e",
    "text_muted": "#a8a29e",
    "accent": "#2563eb",
    "accent_hover": "#1d4ed8",
    "border": "#e7e5e4",
    "success": "#22c55e",
    "error": "#ef4444",
}

# =============================================================================
# CSS MODULES
# =============================================================================

PALETTE_CSS = """
:root {
    --color-bg-primary: #fafaf9;
    --color-bg-secondary: #f5f5f4;
    --color-bg-elevated: #ffffff;
    --color-text-primary: #1c1917;
    --color-text-secondary: #57534e;
    --color-text-muted: #a8a29e;
    --color-accent: #2563eb;
    --color-accent-hover: #1d4ed8;
    --color-border: #e7e5e4;
    --color-success: #22c55e;
    --color-error: #ef4444;
}
"""

TYPOGRAPHY_CSS = """
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

h1 { font-weight: 600; letter-spacing: -0.02em; }
h2, h3 { font-weight: 500; }

.stCaption { color: #57534e; font-size: 0.875rem; }
"""

HIDE_CHROME_CSS = """
/* Hide Streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.viewerBadge_container__r5tak { display: none; }
[data-testid="stToolbar"] { display: none; }
.stDeployButton { display: none; }

/* Adjust layout after hiding header */
.block-container { padding-top: 2rem !important; }
"""

HIDE_SIDEBAR_CSS = """
/* Hide sidebar completely */
[data-testid="stSidebar"] { display: none; }
[data-testid="stSidebarNav"] { display: none; }
[data-testid="collapsedControl"] { display: none; }
"""

COMPONENT_CSS = """
/* Primary buttons */
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
    background: var(--color-accent) !important;
    border: none !important;
    font-weight: 500 !important;
    border-radius: 0.5rem !important;
    transition: all 0.2s ease !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover {
    background: var(--color-accent-hover) !important;
    transform: translateY(-1px) !important;
}

/* Secondary buttons */
.stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]) {
    background: transparent !important;
    border: 1px solid var(--color-border) !important;
    border-radius: 0.5rem !important;
    transition: all 0.2s ease !important;
}

.stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]):hover {
    background: var(--color-bg-secondary) !important;
}

/* Expanders */
.stExpander {
    border: 1px solid var(--color-border) !important;
    border-radius: 0.5rem !important;
    box-shadow: none !important;
}

/* Inputs */
.stTextInput input,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    border-radius: 0.5rem !important;
    border-color: var(--color-border) !important;
}

.stTextInput input:focus,
.stSelectbox > div > div:focus-within {
    border-color: var(--color-accent) !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1) !important;
}

/* Radio buttons */
.stRadio > div {
    gap: 0.5rem;
}

.stRadio > div > label {
    padding: 0.75rem 1rem !important;
    border: 1px solid var(--color-border) !important;
    border-radius: 0.5rem !important;
    transition: all 0.2s ease !important;
}

.stRadio > div > label:hover {
    background: var(--color-bg-secondary) !important;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background: var(--color-accent) !important;
    border-radius: 0.25rem !important;
}

/* Dividers */
hr {
    border-color: var(--color-border) !important;
    margin: 2rem 0 !important;
}

/* Alerts/Info boxes */
.stAlert {
    border-radius: 0.5rem !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 0.5rem 0.5rem 0 0 !important;
    padding: 0.75rem 1.5rem !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-weight: 600 !important;
}

/* Download button */
.stDownloadButton > button {
    background: var(--color-accent) !important;
    border: none !important;
    border-radius: 0.5rem !important;
    font-weight: 500 !important;
}

.stDownloadButton > button:hover {
    background: var(--color-accent-hover) !important;
}
"""

# =============================================================================
# COMBINED STYLES
# =============================================================================

ALL_STYLES = f"""
<style>
{PALETTE_CSS}
{TYPOGRAPHY_CSS}
{HIDE_CHROME_CSS}
{COMPONENT_CSS}
</style>
"""

ALL_STYLES_NO_SIDEBAR = f"""
<style>
{PALETTE_CSS}
{TYPOGRAPHY_CSS}
{HIDE_CHROME_CSS}
{HIDE_SIDEBAR_CSS}
{COMPONENT_CSS}
</style>
"""


def inject_styles(hide_sidebar: bool = False):
    """Inject all custom styles into the Streamlit app.

    Args:
        hide_sidebar: If True, also hides the sidebar (for candidate-facing pages)
    """
    if hide_sidebar:
        st.markdown(ALL_STYLES_NO_SIDEBAR, unsafe_allow_html=True)
    else:
        st.markdown(ALL_STYLES, unsafe_allow_html=True)


def render_metric_card(
    label: str,
    value: str,
    delta: str = None,
    description: str = None
) -> None:
    """Render a styled metric card.

    Args:
        label: The metric label (uppercase)
        value: The main value to display
        delta: Optional change indicator (+10%, -5%, etc.)
        description: Optional description text
    """
    delta_html = ""
    if delta:
        color = COLORS["success"] if delta.startswith("+") else COLORS["error"]
        delta_html = f'<div style="color:{color};font-size:0.875rem;margin-top:0.25rem">{delta}</div>'

    desc_html = ""
    if description:
        desc_html = f'<div style="color:{COLORS["text_secondary"]};font-size:0.875rem;margin-top:0.5rem">{description}</div>'

    st.markdown(f"""
    <div style="
        background: {COLORS["bg_elevated"]};
        border-radius: 0.5rem;
        padding: 1.25rem;
        border: 1px solid {COLORS["border"]};
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    ">
        <div style="
            color: {COLORS["text_secondary"]};
            font-size: 0.75rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        ">{label}</div>
        <div style="
            font-size: 1.75rem;
            font-weight: 600;
            color: {COLORS["text_primary"]};
            margin-top: 0.25rem;
        ">{value}</div>
        {delta_html}
        {desc_html}
    </div>
    """, unsafe_allow_html=True)
