# -*- coding: utf-8 -*-
"""
HOOPS AI - Styles (Professional SaaS Edition)
Clean, modern UI inspired by Linear, Vercel, Notion
"""

from config import BACKGROUND_URL

# ============================================================================
# CSS TEMPLATE - PROFESSIONAL SAAS DESIGN
# ============================================================================
CSS_TEMPLATE = """
<style>
    /* ===== FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@500;700&display=swap');
    
    /* ===== CSS VARIABLES - PROFESSIONAL PALETTE ===== */
    :root {
        /* Backgrounds */
        --bg-primary: #0F172A;
        --bg-secondary: #1E293B;
        --bg-tertiary: #334155;
        --bg-card: #1E293B;
        --bg-hover: #2D3B4F;
        
        /* Text */
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        
        /* Accents */
        --accent-primary: #3B82F6;
        --accent-primary-hover: #2563EB;
        --accent-secondary: #F59E0B;
        --accent-success: #10B981;
        --accent-error: #EF4444;
        
        /* Borders */
        --border-color: #334155;
        --border-light: #475569;
        
        /* Shadows */
        --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.3);
        --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.3);
        
        /* Radius */
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;
        
        /* Transitions */
        --transition: 0.15s ease;
    }
    
    /* ===== RESET & BASE ===== */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    html, body, .stApp {
        font-size: 14px !important;
        color: var(--text-primary) !important;
    }
    
    /* ===== MAIN APP BACKGROUND ===== */
    .stApp {
        background: var(--bg-primary) !important;
    }
    
    .main .block-container {
        max-width: 1400px !important;
        padding: 1rem 1.5rem !important;
    }
    
    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu, footer, header { visibility: hidden; }
    
    /* ===== SIDEBAR - CLEAN NAVIGATION ===== */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: var(--bg-secondary) !important;
        padding: 0.75rem !important;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label {
        color: var(--text-secondary) !important;
        font-size: 0.8rem !important;
    }
    
    /* Sidebar section titles */
    .sidebar-section-title {
        font-size: 0.65rem !important;
        font-weight: 600 !important;
        color: var(--text-muted) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        margin: 0.5rem 0 0.3rem 0 !important;
    }
    
    /* Sidebar divider */
    .sidebar-divider {
        height: 1px !important;
        background: var(--border-color) !important;
        margin: 0.4rem 0 !important;
        border: none !important;
    }
    
    /* ===== BUTTONS - CLEAN STYLE ===== */
    .stButton > button {
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        padding: 0.4rem 0.8rem !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        transition: all var(--transition) !important;
        min-height: 32px !important;
    }
    
    .stButton > button:hover {
        background: var(--bg-hover) !important;
        border-color: var(--border-light) !important;
    }
    
    /* Primary buttons */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background: var(--accent-primary) !important;
        border-color: var(--accent-primary) !important;
        color: white !important;
    }
    
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background: var(--accent-primary-hover) !important;
        border-color: var(--accent-primary-hover) !important;
    }
    
    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: 1px solid transparent !important;
        color: var(--text-secondary) !important;
        padding: 0.35rem 0.6rem !important;
        font-size: 0.7rem !important;
        min-height: 28px !important;
        justify-content: flex-start !important;
        text-align: left !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: var(--bg-hover) !important;
        color: var(--text-primary) !important;
    }
    
    /* Sidebar vertical spacing */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.1rem !important;
    }
    
    [data-testid="stSidebar"] .stButton {
        margin-bottom: 0.05rem !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
        gap: 0.25rem !important;
    }
    
    /* ===== SELECTBOX ===== */
    [data-testid="stSelectbox"] > div > div {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
        background: var(--bg-primary) !important;
        min-height: 28px !important;
        font-size: 0.7rem !important;
    }
    
    /* ===== CHAT MESSAGES - CARD STYLE ===== */
    [data-testid="stChatMessage"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-lg) !important;
        padding: 0.75rem 1rem !important;
        margin-bottom: 0.5rem !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    [data-testid="stChatMessageContent"] {
        color: var(--text-primary) !important;
        font-size: 0.85rem !important;
        line-height: 1.5 !important;
    }
    
    [data-testid="stChatMessageContent"] p {
        color: var(--text-primary) !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* ===== CHAT INPUT ===== */
    [data-testid="stChatInput"] textarea {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-size: 0.85rem !important;
        padding: 0.75rem !important;
    }
    
    [data-testid="stChatInput"] textarea:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* ===== HEADER / LOGO ===== */
    .app-header {
        text-align: center;
        padding: 0.75rem 0;
        margin-bottom: 0.5rem;
    }
    
    .app-logo {
        font-family: 'Orbitron', monospace !important;
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--accent-primary);
        letter-spacing: 2px;
    }
    
    .app-tagline {
        font-size: 0.7rem;
        color: var(--text-muted);
        margin-top: 0.2rem;
    }
    
    /* ===== WELCOME CARD ===== */
    .welcome-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 1rem;
        margin-bottom: 0.75rem;
        box-shadow: var(--shadow-md);
    }
    
    .welcome-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.4rem;
    }
    
    .welcome-text {
        font-size: 0.8rem;
        color: var(--text-secondary);
        line-height: 1.4;
    }
    
    .welcome-highlight {
        color: var(--accent-secondary);
        font-weight: 500;
    }
    
    /* ===== WORKSPACE PANEL (Right Column) ===== */
    .workspace-panel {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 0.75rem;
        min-height: 400px;
    }
    
    .workspace-title {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    /* ===== PROFILE CARD ===== */
    .profile-card {
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 0.5rem 0.6rem;
        margin-bottom: 0.3rem;
    }
    
    .profile-name {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 0.8rem;
    }
    
    .profile-team {
        color: var(--text-muted);
        font-size: 0.65rem;
    }
    
    /* ===== AGENT/COACH CARDS ===== */
    .agent-card {
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-left: 3px solid var(--accent-primary);
        border-radius: var(--radius-md);
        padding: 0.4rem 0.6rem;
        margin-bottom: 0.2rem;
        transition: all var(--transition);
    }
    
    .agent-card:hover {
        background: var(--bg-hover);
        border-left-color: var(--accent-secondary);
    }
    
    /* ===== RESPONSE BADGE ===== */
    .response-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 0.25rem 0.6rem;
        margin-bottom: 0.5rem;
        font-size: 0.7rem;
        color: var(--text-secondary);
    }
    
    /* ===== FILE UPLOADER ===== */
    [data-testid="stFileUploader"] {
        background: var(--bg-tertiary) !important;
        border: 1px dashed var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent-primary) !important;
    }
    
    /* ===== MOBILE NAV HIDE ON DESKTOP ===== */
    @media (min-width: 768px) {
        .mobile-nav-wrapper {
            display: none !important;
        }
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--bg-tertiary);
        border-radius: 3px;
    }
    
    /* ===== COLUMNS GAP ===== */
    [data-testid="stHorizontalBlock"] {
        gap: 0.75rem !important;
    }
    
</style>
"""

# ============================================================================
# FINAL CSS
# ============================================================================
CUSTOM_CSS = CSS_TEMPLATE.replace('BACKGROUND_URL_PLACEHOLDER', BACKGROUND_URL)
