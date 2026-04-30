from dataclasses import dataclass
import os
import plotly.graph_objects as go
import streamlit as st

THEME_SESSION_KEY = "dashboard_theme"
DEFAULT_THEME_KEY = "sage"

@dataclass(frozen=True)
class DashboardTheme:
    key: str
    label: str
    description: str
    mode: str
    background: str
    surface: str
    surface_alt: str
    surface_highlight: str
    sidebar_background: str
    text: str
    muted_text: str
    accent: str
    accent_soft: str
    accent_text: str
    border: str
    shadow: str
    chart_colors: tuple[str, ...]

THEMES = {
    "midnight": DashboardTheme(
        key="midnight",
        label="Midnight Pulse",
        description="Dark navy with electric cyan accents for low-light monitoring.",
        mode="dark",
        background="#06111f",
        surface="#0f1c2f",
        surface_alt="#15263d",
        surface_highlight="#1c3150",
        sidebar_background="#081629",
        text="#e2ecff",
        muted_text="#9db0cc",
        accent="#38bdf8",
        accent_soft="#0ea5e9",
        accent_text="#031525",
        border="#234166",
        shadow="0 16px 40px rgba(3, 10, 24, 0.30)",
        chart_colors=("#38bdf8", "#f97316", "#22c55e", "#a855f7", "#facc15"),
    ),
    "sage": DashboardTheme(
        key="sage",
        label="Sage Signal",
        description="Clean light surfaces with green highlights for everyday analysis.",
        mode="light",
        background="#f4f8f1",
        surface="#ffffff",
        surface_alt="#eef6e7",
        surface_highlight="#dcefd1",
        sidebar_background="#edf6e9",
        text="#1c2a1f",
        muted_text="#5d715f",
        accent="#2f855a",
        accent_soft="#68d391",
        accent_text="#f5fff8",
        border="#c6dcc7",
        shadow="0 14px 35px rgba(39, 65, 45, 0.10)",
        chart_colors=("#2f855a", "#2b6cb0", "#dd6b20", "#805ad5", "#d53f8c"),
    ),
    "sunrise": DashboardTheme(
        key="sunrise",
        label="Sunrise Ops",
        description="Warm sand tones with coral accents for a brighter control room feel.",
        mode="light",
        background="#fff8f1",
        surface="#ffffff",
        surface_alt="#fff1df",
        surface_highlight="#ffe0bc",
        sidebar_background="#fff3e4",
        text="#41251c",
        muted_text="#7a5a4e",
        accent="#dd6b20",
        accent_soft="#f6ad55",
        accent_text="#fff7ef",
        border="#f3cfb0",
        shadow="0 16px 35px rgba(131, 71, 23, 0.12)",
        chart_colors=("#dd6b20", "#3182ce", "#38a169", "#d53f8c", "#805ad5"),
    ),
    "st_light": DashboardTheme(
        key="st_light",
        label="Streamlit Default (Light)",
        description="The standard Streamlit look and feel.",
        mode="light",
        background="transparent", # Logic below will handle this
        surface="#ffffff",
        surface_alt="#f0f2f6",
        surface_highlight="#e0e2e6",
        sidebar_background="#f0f2f6",
        text="#31333F",
        muted_text="#555e6d",
        accent="#ff4b4b",
        accent_soft="#ff4b4b",
        accent_text="#ffffff",
        border="#d3d6db",
        shadow="none",
        chart_colors=("#ff4b4b", "#1c83e1", "#00c0f2", "#fffd80", "#7defa1"),
    ),
    "st_dark": DashboardTheme(
        key="st_dark",
        label="Streamlit Default (Dark)",
        description="The standard Streamlit dark mode.",
        mode="dark",
        background="transparent",
        surface="#0e1117",
        surface_alt="#262730",
        surface_highlight="#31333F",
        sidebar_background="#262730",
        text="#fafafa",
        muted_text="#bfbfbf",
        accent="#ff4b4b",
        accent_soft="#ff4b4b",
        accent_text="#ffffff",
        border="#31333F",
        shadow="none",
        chart_colors=("#ff4b4b", "#1c83e1", "#00c0f2", "#fffd80", "#7defa1"),
    ),
}

def initialize_theme_state():
    if THEME_SESSION_KEY not in st.session_state:
        st.session_state[THEME_SESSION_KEY] = DEFAULT_THEME_KEY

def get_active_theme() -> DashboardTheme:
    initialize_theme_state()
    return THEMES.get(st.session_state[THEME_SESSION_KEY], THEMES[DEFAULT_THEME_KEY])

def apply_theme():
    theme = get_active_theme()
    
    # Check if it's a Streamlit default
    is_st_default = theme.key.startswith("st_")

    # Use Streamlit's internal variables for defaults, or custom hex codes for our themes
    bg_color = "transparent" if is_st_default else theme.background
    sidebar_bg = "transparent" if is_st_default else theme.sidebar_background
    text_color = "inherit" if is_st_default else theme.text

    st.markdown(f"""
        <style>
        /* 1. Root Variables */
        :root {{
            --dashboard-bg: {theme.background};
            --dashboard-surface: {theme.surface};
            --dashboard-text: {theme.text};
            --dashboard-accent: {theme.accent};
            --dashboard-border: {theme.border};
        }}

        /* 2. Main Container Fix */
        [data-testid="stAppViewContainer"] {{
            background-color: {bg_color} !important;
        }}

        /* 3. DISABLE DEPLOY BAR & HEADER COMPLETELY */
        [data-testid="stHeader"] {{
            display: none !important;
        }}
        
        /* Remove the top gap caused by the hidden header */
        .block-container {{
            padding-top: 2rem !important;
        }}

        /* 4. Sidebar Consistency */
        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
            border-right: 1px solid {theme.border if not is_st_default else "rgba(255,255,255,0.1)"};
        }}

        /* 5. Inputs and Selectboxes */
        div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="base-input"] {{
            background-color: {theme.surface} !important;
            border: 1px solid {theme.border} !important;
        }}

        /* 6. Text visibility */
        h1, h2, h3, h4, h5, h6, p, label {{
            color: {text_color} !important;
        }}

        /* 7. Hide Status Widgets & Menus */
        [data-testid="stStatusWidget"], #MainMenu, footer {{
            visibility: hidden !important;
            display: none !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    return theme

def apply_theme_v4():
    theme = get_active_theme()
    
    # Check if it's a Streamlit default
    is_st_default = theme.key.startswith("st_")

    # Use Streamlit's internal variables for defaults, or custom hex codes for our themes
    bg_color = "transparent" if is_st_default else theme.background
    sidebar_bg = "transparent" if is_st_default else theme.sidebar_background
    text_color = "inherit" if is_st_default else theme.text

    st.markdown(f"""
        <style>
        /* 1. Root Variables */
        :root {{
            --dashboard-bg: {theme.background};
            --dashboard-surface: {theme.surface};
            --dashboard-text: {theme.text};
            --dashboard-accent: {theme.accent};
            --dashboard-border: {theme.border};
        }}

        /* 2. Main Container Fix - Ensures background matches theme mode */
        [data-testid="stAppViewContainer"] {{
            background-color: {bg_color} !important;
        }}

        /* 3. Header and Toolbar - Makes them disappear into the background */
        [data-testid="stHeader"] {{
            background-color: rgba(0,0,0,0) !important;
            border-bottom: none !important;
        }}

        /* 4. Sidebar Consistency */
        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
            border-right: 1px solid {theme.border if not is_st_default else "rgba(255,255,255,0.1)"};
        }}

        /* 5. Inputs and Selectboxes - Fixed for Dark Mode visibility */
        div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="base-input"] {{
            background-color: {theme.surface} !important;
            border: 1px solid {theme.border} !important;
        }}

        /* 6. Fix for invisible text in results */
        h1, h2, h3, h4, h5, h6, p, label {{
            color: {text_color} !important;
        }}

        /* 7. Hide the 'Deploy' button for a cleaner look */
        [data-testid="stStatusWidget"] {{
            display: none;
        }}
        </style>
    """, unsafe_allow_html=True)
    return theme

def apply_theme_v4():
    theme = get_active_theme()
    
    # Check if it's a Streamlit default or custom
    is_custom = not theme.key.startswith("st_")

    css = f"""
        <style>
        :root {{
            --dashboard-bg: {theme.background};
            --dashboard-surface: {theme.surface};
            --dashboard-text: {theme.text};
            --dashboard-accent: {theme.accent};
            --dashboard-border: {theme.border};
        }}

        /* 1. TOP BAR & DEPLOY BUTTON FIX */
        [data-testid="stHeader"] {{
            background-color: {theme.background if is_custom else "transparent"} !important;
            border-bottom: 1px solid {theme.border if is_custom else "transparent"};
        }}

        /* Targets the 'Deploy' button and 'Three dots' menu */
        [data-testid="stToolbar"] {{
            background-color: transparent !important;
        }}

        /* 2. SIDEBAR CONSISTENCY */
        [data-testid="stSidebar"] {{
            background-color: {theme.sidebar_background} !important;
            border-right: 1px solid {theme.border};
        }}

        /* 3. MAIN CONTAINER FIX */
        [data-testid="stAppViewContainer"] {{
            background-color: {theme.background} !important;
            color: {theme.text};
        }}

        /* 4. BUTTONS & INPUTS MATCHING THEME */
        .stButton > button {{
            background: linear-gradient(135deg, {theme.accent}, {theme.accent_soft}) !important;
            color: {theme.accent_text} !important;
            border: none !important;
            border-radius: 8px !important;
        }}
        
        /* Ensures inputs don't have that default white background in Dark mode */
        div[data-baseweb="input"], div[data-baseweb="select"] {{
            background-color: {theme.surface} !important;
        }}

        /* 5. METRICS & CARDS */
        [data-testid="stMetric"], [data-testid="stExpander"] {{
            background-color: {theme.surface};
            border: 1px solid {theme.border};
            border-radius: 12px;
        }}
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    return theme

def apply_theme_v3():
    theme = get_active_theme()
    
    # If a Streamlit default is selected, we inject minimal CSS
    # or skip the major background overrides to let Streamlit handle it
    if theme.key.startswith("st_"):
        st.markdown(f"""
            <style>
            /* Minimal overrides for standard themes */
            [data-testid="stMetric"] {{
                background: {theme.surface};
                border: 1px solid {theme.border};
                border-radius: 10px;
            }}
            </style>
        """, unsafe_allow_html=True)
    else:
        # Full Custom CSS Injection for your project-specific themes
        st.markdown(f"""
            <style>
            :root {{
                --dashboard-bg: {theme.background};
                --dashboard-surface: {theme.surface};
                --dashboard-text: {theme.text};
                --dashboard-accent: {theme.accent};
                --dashboard-border: {theme.border};
            }}
            [data-testid="stAppViewContainer"] {{
                background-color: {theme.background};
            }}
            /* ... (rest of your custom CSS from the previous message) ... */
            </style>
        """, unsafe_allow_html=True)
    
    return theme

def apply_theme_v2():
    theme = get_active_theme()
    st.markdown(f"""
        <style>
        :root {{
            --dashboard-bg: {theme.background};
            --dashboard-surface: {theme.surface};
            --dashboard-text: {theme.text};
            --dashboard-accent: {theme.accent};
            --dashboard-border: {theme.border};
        }}
        [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background-color: {theme.background};
        }}
        [data-testid="stSidebar"] {{
            background-color: {theme.sidebar_background};
            border-right: 1px solid {theme.border};
        }}
        /* Style standard buttons and inputs to match theme */
        .stButton > button {{
            background: linear-gradient(135deg, {theme.accent}, {theme.accent_soft}) !important;
            color: {theme.accent_text} !important;
            border-radius: 20px !important;
        }}
        /* Style text areas and inputs */
        div[data-baseweb="input"] > div {{
            background-color: {theme.surface} !important;
            color: {theme.text} !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    return theme

def style_plotly_figure_v1(fig: go.Figure) -> go.Figure:
    theme = get_active_theme()
    template = "plotly_dark" if theme.mode == "dark" else "plotly_white"
    fig.update_layout(
        template=template,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={"color": theme.text},
        colorway=list(theme.chart_colors),
    )
    return fig

def style_plotly_figure(fig: go.Figure) -> go.Figure:
    theme = get_active_theme()
    
    # Determine the base template
    template = "plotly_dark" if theme.mode == "dark" else "plotly_white"
    
    fig.update_layout(
        template=template,
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent lets the theme shine through
        plot_bgcolor='rgba(0,0,0,0)',
        font={"color": theme.text},
        colorway=list(theme.chart_colors),
        margin={"l": 10, "r": 10, "t": 40, "b": 10}
    )
    
    # Update grid lines to be subtle based on the theme's border color
    fig.update_xaxes(gridcolor=theme.border, zeroline=False)
    fig.update_yaxes(gridcolor=theme.border, zeroline=False)
    
    return fig
