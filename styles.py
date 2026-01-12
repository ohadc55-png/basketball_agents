# -*- coding: utf-8 -*-
"""
HOOPS AI - Styles
All CSS styling for the application
"""

from config import BACKGROUND_URL

# ============================================================================
# CSS TEMPLATE
# ============================================================================
CSS_TEMPLATE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');
    
    /* ===== MAIN APP BACKGROUND ===== */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('BACKGROUND_URL_PLACEHOLDER');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* ===== GLOBAL TEXT COLOR ===== */
    .stApp p, .stApp span, .stApp li, .stApp label, .stApp div {
        color: #FFFFFF;
    }
    
    /* ===== MAIN CONTAINER ===== */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(13,13,13,0.95) 0%, rgba(26,26,26,0.95) 50%, rgba(13,13,13,0.95) 100%);
        border-right: 1px solid rgba(255, 107, 53, 0.3);
    }
    
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background: rgba(30, 30, 30, 0.8) !important;
        border: 1px solid rgba(255, 107, 53, 0.3) !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
        color: #FF6B35 !important;
    }
    
    /* ===== HERO SECTION ===== */
    .hero-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #FF6B35, #FF8C42, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        text-align: center;
        color: #B0B0B0;
        letter-spacing: 6px;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }
    
    /* ===== SCOREBOARD HEADER ===== */
    .scoreboard {
        background: linear-gradient(135deg, rgba(20,20,20,0.9), rgba(30,30,30,0.85));
        border: 2px solid rgba(255, 107, 53, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 0 30px rgba(255, 107, 53, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* ===== CHAT MESSAGES ===== */
    [data-testid="stChatMessage"] {
        background: linear-gradient(135deg, rgba(25,25,25,0.85), rgba(35,35,35,0.8));
        border: 1px solid rgba(255, 107, 53, 0.2);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.8rem 0;
        backdrop-filter: blur(5px);
    }
    
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div {
        color: #FFFFFF !important;
    }
    
    [data-testid="stChatMessage"] strong {
        color: #FF6B35 !important;
    }
    
    /* ===== CHAT INPUT ===== */
    [data-testid="stChatInput"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    [data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important;
        background: rgba(25, 25, 25, 0.95) !important;
        border: 2px solid rgba(255, 107, 53, 0.5) !important;
        border-radius: 25px !important;
        padding: 0.8rem 1rem !important;
    }
    
    [data-testid="stChatInput"] textarea:focus {
        border-color: #FF6B35 !important;
        box-shadow: 0 0 15px rgba(255, 107, 53, 0.4) !important;
    }
    
    [data-testid="stChatInput"] textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    [data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #FF6B35, #FF8C42) !important;
        border-radius: 50% !important;
        color: #000 !important;
    }
    
    [data-testid="stChatInput"] button:hover {
        box-shadow: 0 0 20px rgba(255, 107, 53, 0.6) !important;
    }
    
    /* ===== BOTTOM AREA ===== */
    [data-testid="stBottom"] {
        background: rgba(13, 13, 13, 0.98) !important;
        border-top: 1px solid rgba(255, 107, 53, 0.3) !important;
    }
    
    [data-testid="stBottom"] > div {
        background: transparent !important;
    }
    
    [data-testid="stBottom"] * {
        background-color: transparent !important;
    }
    
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] > div > div {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* ===== FILE UPLOADER ===== */
    [data-testid="stFileUploader"] {
        background: rgba(30, 30, 30, 0.95) !important;
        border: 2px solid rgba(255, 107, 53, 0.5) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #FFFFFF !important;
    }
    
    [data-testid="stFileUploader"] section {
        background: rgba(50, 50, 50, 0.9) !important;
        border: 2px dashed rgba(255, 107, 53, 0.5) !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stFileUploader"] section > div {
        color: #FFFFFF !important;
    }
    
    [data-testid="stFileUploader"] small {
        color: #FF6B35 !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #FF6B35, #FF8C42) !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* ===== SELECTBOX ===== */
    [data-testid="stSelectbox"] label {
        color: #FFFFFF !important;
    }
    
    [data-testid="stSelectbox"] > div > div {
        background: rgba(40, 40, 40, 0.95) !important;
        border: 1px solid rgba(255, 107, 53, 0.5) !important;
        color: #FFFFFF !important;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        font-family: 'Orbitron', monospace;
        font-weight: 600;
        background: rgba(255, 107, 53, 0.2);
        color: #FF6B35;
        border: 2px solid #FF6B35;
        border-radius: 25px;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FF6B35, #FF8C42);
        color: #000;
        box-shadow: 0 0 30px rgba(255, 107, 53, 0.5);
    }
    
    /* ===== WELCOME BANNER ===== */
    .welcome-banner {
        background: linear-gradient(135deg, rgba(255,107,53,0.2), rgba(255,140,66,0.15), rgba(0,212,255,0.1));
        border: 2px solid rgba(255, 107, 53, 0.4);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .welcome-title {
        font-family: 'Orbitron', monospace;
        font-size: 1.6rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0.5rem;
    }
    
    .welcome-text {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        color: #B0B0B0;
    }
    
    /* ===== SIDEBAR DIVIDER ===== */
    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,107,53,0.5), transparent);
        margin: 1.5rem 0;
    }
    
    /* ===== RESPONSE BADGE ===== */
    .response-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 107, 53, 0.2);
        border: 1px solid rgba(255, 107, 53, 0.5);
        border-radius: 20px;
        padding: 0.4rem 1rem;
        margin-bottom: 1rem;
        font-family: 'Orbitron', monospace;
        font-size: 0.85rem;
        font-weight: 600;
        color: #FF6B35;
    }
    
    /* ===== LOGIN CONTAINER ===== */
    .login-container {
        background: linear-gradient(135deg, rgba(20,20,20,0.95), rgba(30,30,30,0.9));
        border: 2px solid rgba(255, 107, 53, 0.5);
        border-radius: 20px;
        padding: 2rem;
        max-width: 500px;
        margin: 2rem auto;
        backdrop-filter: blur(10px);
    }
    
    /* ===== PROFILE CARD ===== */
    .profile-card {
        background: rgba(255, 107, 53, 0.1);
        border: 1px solid rgba(255, 107, 53, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* ===== HISTORY ITEM ===== */
    .history-item {
        background: rgba(30, 30, 30, 0.8);
        border: 1px solid rgba(255, 107, 53, 0.2);
        border-radius: 10px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .history-item:hover {
        border-color: #FF6B35;
        background: rgba(255, 107, 53, 0.1);
    }
    
    /* ===== FORM STYLING ===== */
    .stTextInput input, .stSelectbox select {
        background: rgba(30, 30, 30, 0.9) !important;
        border: 1px solid rgba(255, 107, 53, 0.3) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: #FF6B35 !important;
        box-shadow: 0 0 10px rgba(255, 107, 53, 0.3) !important;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {width: 8px;}
    ::-webkit-scrollbar-track {background: #0D0D0D;}
    ::-webkit-scrollbar-thumb {background: linear-gradient(#FF6B35, #FF8C42); border-radius: 4px;}
    
    /* ===== DESKTOP STYLES ===== */
    @media (min-width: 768px) {
        section[data-testid="stSidebar"] {
            display: flex !important;
            width: 300px !important;
            min-width: 300px !important;
            transform: none !important;
            position: relative !important;
        }
        
        button[data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"],
        button[kind="headerNoPadding"] {
            display: none !important;
        }
        
        .main .block-container {
            max-width: 100% !important;
        }
        
        .mobile-only-buttons {
            display: none !important;
        }
    }
    
    /* ===== MOBILE STYLES ===== */
    @media (max-width: 767px) {
        .mobile-only-buttons {
            display: flex !important;
            gap: 0.5rem;
            margin-bottom: 1rem;
            padding: 0.5rem;
        }
        
        .mobile-only-buttons button {
            flex: 1;
            padding: 0.5rem !important;
            font-size: 0.85rem !important;
        }
    }
</style>
"""

# ============================================================================
# GENERATE CSS
# ============================================================================
def get_custom_css():
    """Generate the custom CSS with background URL"""
    return CSS_TEMPLATE.replace('BACKGROUND_URL_PLACEHOLDER', BACKGROUND_URL)

CUSTOM_CSS = get_custom_css()
