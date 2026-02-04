# -*- coding: utf-8 -*-
"""
HOOPS AI - Styles (Modern Edition)
Clean, warm dark theme with Space Grotesk font
"""

from config import BACKGROUND_URL

# ============================================================================
# CSS TEMPLATE - MODERN WARM DESIGN
# ============================================================================
CSS_TEMPLATE = """
<style>
    /* ===== FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ===== CSS VARIABLES - WARM DARK THEME ===== */
    :root {
        --primary: #f48c25;
        --primary-light: #ffa94d;
        --primary-dark: #e07b1a;
        --secondary: #00D4FF;
        --accent: #FFD700;
        --success: #00FF87;
        --bg-dark: #181411;
        --bg-darker: #120e0c;
        --bg-card: #221910;
        --bg-surface: #221910;
        --bg-glass: rgba(34, 25, 16, 0.9);
        --border-dark: #393028;
        --border-light: #4a3f33;
        --text-primary: #FFFFFF;
        --text-secondary: #baab9c;
        --text-muted: #7a6f63;
        --border-glow: rgba(244, 140, 37, 0.4);
        --shadow-glow: rgba(244, 140, 37, 0.25);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --radius-full: 9999px;
        --transition-fast: 0.15s ease;
        --transition-normal: 0.25s ease;
        --transition-slow: 0.4s ease;
    }
    
    /* ===== KEYFRAME ANIMATIONS ===== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-15px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(15px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes pulse-subtle {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    /* ===== MAIN APP BACKGROUND ===== */
    .stApp {
        background: var(--bg-darker);
        font-family: 'Space Grotesk', 'Inter', sans-serif;
    }
    
    /* ===== GLOBAL TYPOGRAPHY & LAYOUT ===== */

    /* Base font */
    html, body, .stApp {
        font-size: 14px !important;
        font-family: 'Space Grotesk', 'Inter', sans-serif !important;
    }

    /* Main content area */
    .main .block-container {
        max-width: 100% !important;
        padding: 1.5rem 2rem 1.5rem 1.5rem !important;
        margin-left: 0 !important;
        background: var(--bg-darker);
    }

    /* Make main area use full width */
    .main {
        margin-left: 0 !important;
        padding-left: 0 !important;
        background: var(--bg-darker);
    }

    [data-testid="stAppViewContainer"] {
        margin-left: 0 !important;
        background: var(--bg-darker);
    }

    /* Text styling */
    .stApp p, .stApp span, .stApp div, .stApp label, .stApp li {
        font-size: 0.9rem !important;
        line-height: 1.5 !important;
        font-family: 'Space Grotesk', 'Inter', sans-serif !important;
    }

    /* Headers */
    .stApp h1 { font-size: 1.75rem !important; font-weight: 700 !important; }
    .stApp h2 { font-size: 1.5rem !important; font-weight: 600 !important; }
    .stApp h3 { font-size: 1.2rem !important; font-weight: 600 !important; }
    .stApp h4 { font-size: 1rem !important; font-weight: 500 !important; }
    
    /* ===== BUTTONS - MODERN STYLE ===== */
    .stButton > button {
        padding: 0.5rem 1rem !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        min-height: 36px !important;
        line-height: 1.3 !important;
        margin: 0 !important;
        border-radius: var(--radius-md) !important;
        transition: all var(--transition-normal) !important;
    }

    /* Remove gaps between buttons */
    .stButton {
        margin-bottom: 0.25rem !important;
    }

    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        padding: 0.4rem 0.6rem !important;
        font-size: 0.8rem !important;
        min-height: 32px !important;
        max-height: 40px !important;
        overflow: hidden !important;
        margin: 0 !important;
    }

    [data-testid="stSidebar"] .stButton {
        margin-bottom: 0.15rem !important;
    }

    /* Sidebar layout fixes */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.2rem !important;
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
        gap: 0.4rem !important;
        margin-bottom: 0.3rem !important;
    }

    [data-testid="stSidebar"] [data-testid="column"] {
        padding: 0 !important;
    }

    [data-testid="stSidebar"] [data-testid="stElementContainer"] {
        margin-bottom: 0 !important;
    }
    
    /* ===== SIDEBAR - CLEAN DESIGN ===== */
    [data-testid="stSidebar"] {
        width: 260px !important;
        background: var(--bg-dark) !important;
        border-right: 1px solid var(--border-dark) !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        width: 260px !important;
        background: var(--bg-dark) !important;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        padding: 0.75rem !important;
        background: var(--bg-dark) !important;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label {
        font-size: 0.85rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text-primary) !important;
    }

    /* Sidebar selectbox */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] {
        font-size: 0.85rem !important;
        margin-bottom: 0.3rem !important;
    }

    [data-testid="stSidebar"] [data-testid="stSelectbox"] > div {
        margin-bottom: 0 !important;
    }

    [data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
        padding: 0.4rem 0.6rem !important;
        min-height: 32px !important;
        font-size: 0.85rem !important;
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-md) !important;
    }
    
    /* ===== CHAT MESSAGES - MODERN STYLE ===== */
    [data-testid="stChatMessage"] {
        padding: 0.75rem 1rem !important;
        font-size: 0.9rem !important;
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-lg) !important;
        margin: 0.5rem 0 !important;
    }

    [data-testid="stChatMessageContent"] {
        font-size: 0.9rem !important;
    }

    [data-testid="stChatMessageContent"] p {
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
        line-height: 1.6 !important;
    }

    /* Chat input */
    [data-testid="stChatInput"] {
        font-size: 0.9rem !important;
    }

    [data-testid="stChatInput"] textarea {
        font-size: 0.9rem !important;
        padding: 0.75rem 1rem !important;
        min-height: 44px !important;
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-xl) !important;
    }
    
    /* ===== WELCOME BANNER - MODERN ===== */
    .welcome-banner {
        padding: 1.25rem 1.5rem !important;
        margin-bottom: 1rem !important;
        background: linear-gradient(135deg, rgba(244, 140, 37, 0.1), rgba(244, 140, 37, 0.05)) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-lg) !important;
    }

    .welcome-title {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text-primary) !important;
    }

    .welcome-text {
        font-size: 0.9rem !important;
        color: var(--text-secondary) !important;
        line-height: 1.5 !important;
    }

    /* ===== SCOREBOARD/HEADER ===== */
    .scoreboard {
        padding: 1rem 1.5rem !important;
        margin-bottom: 1rem !important;
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-lg) !important;
    }

    .hero-title {
        font-size: 2rem !important;
        font-weight: 700 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--primary) !important;
        letter-spacing: 2px !important;
    }

    .hero-subtitle {
        font-size: 0.9rem !important;
        color: var(--text-secondary) !important;
        letter-spacing: 1px !important;
    }

    /* ===== PROFILE CARD ===== */
    .profile-card {
        padding: 0.75rem 1rem !important;
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-md) !important;
    }

    .profile-card div {
        font-size: 0.85rem !important;
    }

    /* ===== AGENT CARDS ===== */
    .agent-card {
        padding: 0.6rem 0.8rem !important;
        margin-bottom: 0.4rem !important;
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-md) !important;
        transition: all var(--transition-normal) !important;
    }

    .agent-card:hover {
        border-color: var(--primary) !important;
        transform: translateX(3px) !important;
    }

    .agent-card span {
        font-size: 1.1rem !important;
    }

    .agent-card div div {
        font-size: 0.8rem !important;
    }

    /* ===== DIVIDERS ===== */
    .sidebar-divider {
        margin: 0.5rem 0 !important;
        height: 1px !important;
        background: var(--border-dark) !important;
        opacity: 0.5 !important;
    }
    
    /* Mobile nav hide on desktop */
    @media (min-width: 769px) {
        .mobile-only-nav,
        .mobile-nav-wrapper {
            display: none !important;
            height: 0 !important;
            overflow: hidden !important;
        }
    }
    
    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu, footer, header {visibility: hidden;}

    /* ===== GLOBAL TEXT ===== */
    .stApp p, .stApp span, .stApp li, .stApp label, .stApp div {
        color: var(--text-primary);
        font-family: 'Space Grotesk', 'Inter', sans-serif;
    }

    /* ===== MAIN CONTAINER ===== */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
        animation: fadeIn 0.4s ease;
    }

    /* ===== SIDEBAR STYLING ===== */
    [data-testid="stSidebar"] {
        background: var(--bg-dark) !important;
        border-right: 1px solid var(--border-dark) !important;
    }

    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--primary), var(--primary-light));
    }

    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }

    /* Sidebar Expanders */
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-md) !important;
        margin-bottom: 0.5rem !important;
        transition: all var(--transition-normal) !important;
        overflow: hidden;
    }

    [data-testid="stSidebar"] [data-testid="stExpander"]:hover {
        border-color: var(--primary) !important;
    }

    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        transition: all var(--transition-fast) !important;
    }

    [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
        color: var(--primary) !important;
    }
    
    /* ===== HERO SECTION - CLEAN ===== */
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: var(--primary);
        letter-spacing: 3px;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        text-align: center;
        color: var(--text-secondary);
        letter-spacing: 2px;
        margin-bottom: 1.5rem;
    }

    /* ===== SCOREBOARD/HEADER ===== */
    .scoreboard {
        background: var(--bg-surface);
        border: 1px solid var(--border-dark);
        border-radius: var(--radius-lg);
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
    }

    /* ===== WELCOME BANNER ===== */
    .welcome-banner {
        background: linear-gradient(135deg, rgba(244, 140, 37, 0.1), rgba(244, 140, 37, 0.05));
        border: 1px solid var(--border-dark);
        border-radius: var(--radius-lg);
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        animation: fadeIn 0.4s ease;
    }

    .welcome-banner::before {
        content: '🏀';
        position: absolute;
        top: 15px;
        right: 20px;
        font-size: 2.5rem;
        opacity: 0.2;
    }

    .welcome-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
    }

    .welcome-text {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* ===== CHAT MESSAGES - CLEAN STYLE ===== */
    [data-testid="stChatMessage"] {
        background: var(--bg-surface);
        border: 1px solid var(--border-dark);
        border-radius: var(--radius-lg);
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        animation: fadeIn 0.3s ease;
        transition: all var(--transition-normal);
    }

    [data-testid="stChatMessage"]:hover {
        border-color: var(--border-light);
    }

    /* User messages */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(135deg, rgba(244, 140, 37, 0.1), rgba(244, 140, 37, 0.05));
        border-color: rgba(244, 140, 37, 0.3);
        animation: slideInRight 0.3s ease;
    }

    /* Assistant messages */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        animation: slideInLeft 0.3s ease;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div {
        color: var(--text-primary) !important;
    }

    [data-testid="stChatMessage"] strong {
        color: var(--primary) !important;
        font-weight: 600;
    }

    [data-testid="stChatMessage"] code {
        background: rgba(244, 140, 37, 0.15) !important;
        color: var(--primary-light) !important;
        padding: 0.15rem 0.4rem;
        border-radius: 4px;
        font-size: 0.9em;
    }

    /* ===== CHAT INPUT - CLEAN ===== */
    [data-testid="stChatInput"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    [data-testid="stChatInput"] textarea {
        color: var(--text-primary) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.95rem !important;
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-xl) !important;
        padding: 0.875rem 1.25rem !important;
        transition: all var(--transition-normal) !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(244, 140, 37, 0.2) !important;
        outline: none !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--text-muted) !important;
    }

    [data-testid="stChatInput"] button {
        background: var(--primary) !important;
        border-radius: var(--radius-md) !important;
        color: var(--bg-dark) !important;
        transition: all var(--transition-normal) !important;
    }

    [data-testid="stChatInput"] button:hover {
        background: var(--primary-light) !important;
        transform: scale(1.05) !important;
    }

    /* ===== BOTTOM AREA ===== */
    [data-testid="stBottom"] {
        background: linear-gradient(180deg, transparent, var(--bg-darker)) !important;
        border-top: 1px solid var(--border-dark) !important;
        padding-top: 0.75rem !important;
    }

    [data-testid="stBottom"] > div,
    [data-testid="stBottom"] *,
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] > div > div {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* ===== SIDEBAR NAVIGATION BUTTONS ===== */
    [data-testid="stSidebar"] .stButton > button {
        font-size: 0.85rem !important;
        padding: 0.6rem 0.5rem !important;
        letter-spacing: 0.3px !important;
        min-height: 40px !important;
        white-space: nowrap !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* ===== BUTTONS - MODERN STYLE ===== */
    .stButton > button {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        background: var(--bg-surface) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-md) !important;
        padding: 0.6rem 1.25rem !important;
        transition: all var(--transition-normal) !important;
        position: relative;
        overflow: hidden;
    }

    .stButton > button:hover {
        background: var(--primary) !important;
        color: var(--bg-dark) !important;
        border-color: var(--primary) !important;
        transform: translateY(-2px) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* ===== CALENDAR DAY BUTTONS - SECONDARY TYPE ===== */
    .stButton > button[kind="secondary"] {
        background: var(--bg-surface) !important;
        color: var(--text-primary) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-md) !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        min-height: 60px !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: var(--primary) !important;
        color: var(--bg-dark) !important;
        -webkit-text-fill-color: var(--bg-dark) !important;
        border-color: var(--primary) !important;
        transform: translateY(-2px) !important;
    }

    /* Primary buttons (active/today) */
    .stButton > button[kind="primary"] {
        background: var(--primary) !important;
        color: var(--bg-dark) !important;
        -webkit-text-fill-color: var(--bg-dark) !important;
        border: 1px solid var(--primary) !important;
        border-radius: var(--radius-md) !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        min-height: 60px !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: var(--primary-light) !important;
        border-color: var(--primary-light) !important;
        transform: translateY(-2px) !important;
    }

    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        color: var(--text-primary) !important;
        background: var(--bg-surface) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
        min-height: auto !important;
        font-size: 0.85rem !important;
        border: 1px solid var(--border-dark) !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        color: var(--bg-dark) !important;
        background: var(--primary) !important;
        -webkit-text-fill-color: var(--bg-dark) !important;
        border-color: var(--primary) !important;
    }
    
    /* ===== SIDEBAR EXPANDER STYLES (Quick Ideas) ===== */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.6rem 1rem !important;
        transition: all var(--transition-normal) !important;
    }

    [data-testid="stSidebar"] .streamlit-expanderHeader:hover {
        border-color: var(--primary) !important;
    }

    [data-testid="stSidebar"] .streamlit-expanderHeader p {
        color: var(--text-primary) !important;
        font-size: 0.9rem !important;
        margin: 0 !important;
    }

    [data-testid="stSidebar"] .streamlit-expanderContent {
        background: var(--bg-dark) !important;
        border: 1px solid var(--border-dark) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
        padding: 0.5rem !important;
    }

    /* Quick Ideas buttons inside expander */
    [data-testid="stSidebar"] .streamlit-expanderContent .stButton > button {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        color: var(--text-secondary) !important;
        -webkit-text-fill-color: var(--text-secondary) !important;
        font-size: 0.8rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        padding: 0.5rem 0.75rem !important;
        margin: 0.2rem 0 !important;
        text-align: left !important;
        justify-content: flex-start !important;
    }

    [data-testid="stSidebar"] .streamlit-expanderContent .stButton > button:hover {
        background: var(--primary) !important;
        color: var(--bg-dark) !important;
        -webkit-text-fill-color: var(--bg-dark) !important;
        border-color: var(--primary) !important;
    }

    /* Expander arrow icon */
    [data-testid="stSidebar"] .streamlit-expanderHeader svg {
        fill: var(--primary) !important;
        color: var(--primary) !important;
    }

    /* ===== RESPONSE BADGE ===== */
    .response-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(244, 140, 37, 0.15);
        border: 1px solid rgba(244, 140, 37, 0.3);
        border-radius: var(--radius-full);
        padding: 0.4rem 1rem;
        margin-bottom: 0.75rem;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--primary);
        animation: fadeIn 0.3s ease;
    }

    .response-badge span:first-child {
        font-size: 1.1rem;
    }
    
    /* ===== FILE UPLOADER ===== */
    [data-testid="stFileUploader"] {
        background: var(--bg-surface) !important;
        border: 2px dashed var(--border-dark) !important;
        border-radius: var(--radius-lg) !important;
        padding: 1.5rem !important;
        transition: all var(--transition-normal) !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary) !important;
    }

    [data-testid="stFileUploader"] label {
        color: var(--text-primary) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
    }

    [data-testid="stFileUploader"] section {
        background: var(--bg-dark) !important;
        border: 2px dashed var(--border-dark) !important;
        border-radius: var(--radius-md) !important;
        transition: all var(--transition-normal) !important;
    }

    [data-testid="stFileUploader"] section:hover {
        border-color: var(--primary) !important;
    }

    [data-testid="stFileUploader"] section > div {
        color: var(--text-primary) !important;
    }

    [data-testid="stFileUploader"] small {
        color: var(--primary) !important;
    }

    [data-testid="stFileUploader"] button {
        background: var(--primary) !important;
        color: var(--bg-dark) !important;
        font-weight: 600 !important;
        border-radius: var(--radius-md) !important;
        transition: all var(--transition-normal) !important;
    }

    [data-testid="stFileUploader"] button:hover {
        background: var(--primary-light) !important;
    }

    /* ===== SELECTBOX ===== */
    [data-testid="stSelectbox"] label {
        color: var(--text-primary) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
    }

    [data-testid="stSelectbox"] > div > div {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        transition: all var(--transition-normal) !important;
    }

    [data-testid="stSelectbox"] > div > div:hover {
        border-color: var(--primary) !important;
    }
    
    /* ===== SIDEBAR DIVIDER ===== */
    .sidebar-divider {
        height: 1px;
        background: var(--border-dark);
        margin: 1rem 0;
        opacity: 0.5;
    }

    /* ===== LOGIN CONTAINER ===== */
    .login-container {
        background: var(--bg-surface);
        border: 1px solid var(--border-dark);
        border-radius: var(--radius-lg);
        padding: 2rem;
        max-width: 480px;
        margin: 2rem auto;
        animation: fadeIn 0.4s ease;
    }

    /* ===== PROFILE CARD ===== */
    .profile-card {
        background: var(--bg-surface);
        border: 1px solid var(--border-dark);
        border-radius: var(--radius-md);
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all var(--transition-normal);
    }

    .profile-card:hover {
        border-color: var(--primary);
    }
    
    /* ===== FORM INPUTS - DARK THEME ===== */

    /* ALL Input types - base styling */
    .stTextInput input,
    .stNumberInput input,
    .stDateInput input,
    .stTimeInput input,
    .stTextArea textarea,
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea,
    input[type="text"],
    input[type="number"],
    input[type="date"],
    input[type="time"],
    input[type="email"],
    input[type="tel"] {
        background: var(--bg-surface) !important;
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        padding: 0.75rem 1rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        transition: all var(--transition-normal) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
    }

    /* AUTOFILL FIX */
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    input:-webkit-autofill:active,
    .stTextInput input:-webkit-autofill,
    .stTextInput input:-webkit-autofill:hover,
    .stTextInput input:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0 30px var(--bg-surface) inset !important;
        -webkit-text-fill-color: var(--text-primary) !important;
        background-color: var(--bg-surface) !important;
        caret-color: var(--text-primary) !important;
        transition: background-color 5000s ease-in-out 0s !important;
    }

    /* Input containers */
    [data-baseweb="input"],
    [data-baseweb="base-input"] {
        background: var(--bg-surface) !important;
        background-color: var(--bg-surface) !important;
    }

    [data-baseweb="input"] > div,
    [data-baseweb="base-input"] > div {
        background: var(--bg-surface) !important;
        background-color: var(--bg-surface) !important;
    }

    /* Number input wrapper */
    .stNumberInput > div > div {
        background: var(--bg-surface) !important;
        border-radius: var(--radius-md) !important;
    }

    /* Number input buttons */
    .stNumberInput button {
        background: var(--bg-dark) !important;
        color: var(--primary) !important;
        border: 1px solid var(--border-dark) !important;
    }

    .stNumberInput button:hover {
        background: rgba(244, 140, 37, 0.2) !important;
    }

    /* Date and Time input containers */
    .stDateInput > div > div,
    .stTimeInput > div > div,
    [data-testid="stDateInput"] > div > div,
    [data-testid="stTimeInput"] > div > div {
        background: var(--bg-surface) !important;
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-md) !important;
    }

    /* Date/Time input text */
    .stDateInput input,
    .stTimeInput input,
    [data-testid="stDateInput"] input,
    [data-testid="stTimeInput"] input {
        color: var(--text-primary) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
    }

    /* Focus states */
    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stDateInput input:focus,
    .stTimeInput input:focus,
    .stTextArea textarea:focus,
    [data-baseweb="input"]:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(244, 140, 37, 0.2) !important;
        outline: none !important;
    }

    /* Placeholder text */
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder,
    input::placeholder {
        color: var(--text-muted) !important;
        -webkit-text-fill-color: var(--text-muted) !important;
    }

    /* Form Labels */
    .stTextInput label,
    .stNumberInput label,
    .stDateInput label,
    .stTimeInput label,
    .stTextArea label,
    .stSelectbox label,
    .stCheckbox label,
    .stRadio label,
    .stMultiSelect label,
    [data-testid="stWidgetLabel"] {
        color: var(--text-primary) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
    }

    /* Selectbox / Dropdown */
    .stSelectbox > div > div,
    [data-testid="stSelectbox"] > div > div,
    [data-baseweb="select"] > div {
        background: var(--bg-surface) !important;
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
    }

    /* Selected value in selectbox */
    [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] span {
        color: var(--text-primary) !important;
    }

    .stSelectbox > div > div:hover,
    [data-baseweb="select"] > div:hover {
        border-color: var(--primary) !important;
    }

    /* Dropdown menu container */
    [data-baseweb="menu"],
    [data-baseweb="popover"] [data-baseweb="menu"],
    [role="listbox"] {
        background: var(--bg-surface) !important;
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-md) !important;
    }

    /* Dropdown menu items */
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] [role="option"],
    [role="listbox"] [role="option"] {
        color: var(--text-primary) !important;
        background: transparent !important;
    }

    [data-baseweb="menu"] li:hover,
    [data-baseweb="menu"] [role="option"]:hover,
    [role="listbox"] [role="option"]:hover {
        background: rgba(244, 140, 37, 0.15) !important;
    }

    /* Selected option in dropdown */
    [data-baseweb="menu"] [aria-selected="true"],
    [role="option"][aria-selected="true"] {
        background: rgba(244, 140, 37, 0.2) !important;
    }
    
    /* Date picker popup/calendar */
    [data-baseweb="calendar"],
    [data-baseweb="datepicker"],
    [data-baseweb="popover"] > div,
    [data-baseweb="popover"] [data-baseweb="calendar"] {
        background: #1a1a1a !important;
        background-color: #1a1a1a !important;
        border: 1px solid rgba(255, 107, 53, 0.3) !important;
        border-radius: 10px !important;
    }
    
    /* ========== CALENDAR MONTH/YEAR DROPDOWNS - AGGRESSIVE FIX ========== */
    
    /* The popover container that holds the calendar */
    [data-baseweb="popover"] {
        background: transparent !important;
    }
    
    [data-baseweb="popover"] > div > div {
        background: #1a1a1a !important;
    }
    
    /* Month and Year select containers in calendar header */
    [data-baseweb="calendar"] [data-baseweb="select"],
    [data-baseweb="datepicker"] [data-baseweb="select"] {
        background: #1a1a1a !important;
    }
    
    [data-baseweb="calendar"] [data-baseweb="select"] > div,
    [data-baseweb="datepicker"] [data-baseweb="select"] > div {
        background: #1a1a1a !important;
        background-color: #1a1a1a !important;
        border: 1px solid rgba(255, 107, 53, 0.3) !important;
    }
    
    /* The actual text showing month/year */
    [data-baseweb="calendar"] [data-baseweb="select"] [data-baseweb="tag"],
    [data-baseweb="calendar"] [data-baseweb="select"] > div > div,
    [data-baseweb="calendar"] [data-baseweb="select"] > div > div > div,
    [data-baseweb="calendar"] [data-baseweb="select"] span,
    [data-baseweb="datepicker"] [data-baseweb="select"] span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        background: transparent !important;
    }
    
    /* Calendar header row with month/year */
    [data-baseweb="calendar"] > div:first-child,
    [data-baseweb="calendar-header"] {
        background: #1a1a1a !important;
    }
    
    [data-baseweb="calendar"] > div:first-child *,
    [data-baseweb="calendar-header"] * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    
    /* Week day headers (Su, Mo, Tu, etc) */
    [data-baseweb="calendar"] [role="row"]:first-child div,
    [data-baseweb="calendar"] thead th {
        color: #f48c25 !important;
        -webkit-text-fill-color: #f48c25 !important;
    }
    
    /* All day buttons/cells in the calendar */
    [data-baseweb="calendar"] [role="gridcell"],
    [data-baseweb="calendar"] [role="gridcell"] > div,
    [data-baseweb="calendar"] button {
        color: var(--text-primary) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
        background: transparent !important;
    }

    /* Day numbers */
    [data-baseweb="calendar"] [role="gridcell"] div,
    [data-baseweb="calendar"] td div {
        color: var(--text-primary) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
    }

    /* Selected date */
    [data-baseweb="calendar"] [aria-selected="true"],
    [data-baseweb="calendar"] [aria-selected="true"] div,
    [data-baseweb="calendar"] [data-highlighted="true"] {
        background: var(--primary) !important;
        background-color: var(--primary) !important;
        color: var(--bg-dark) !important;
        -webkit-text-fill-color: var(--bg-dark) !important;
    }

    /* Today's date indicator */
    [data-baseweb="calendar"] [data-today="true"] {
        border: 2px solid var(--primary) !important;
    }

    /* Hover state for days */
    [data-baseweb="calendar"] [role="gridcell"]:hover,
    [data-baseweb="calendar"] button:hover {
        background: rgba(244, 140, 37, 0.15) !important;
    }

    /* Navigation arrows */
    [data-baseweb="calendar"] [aria-label*="previous"],
    [data-baseweb="calendar"] [aria-label*="next"],
    [data-baseweb="calendar"] svg {
        color: var(--primary) !important;
        fill: var(--primary) !important;
    }

    /* Month/year dropdown menus */
    [data-baseweb="popover"] [data-baseweb="menu"],
    [data-baseweb="popover"] ul,
    [data-baseweb="calendar"] ~ [data-baseweb="popover"] > div {
        background: var(--bg-surface) !important;
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
    }

    /* Items in month/year dropdown */
    [data-baseweb="popover"] [data-baseweb="menu"] li,
    [data-baseweb="popover"] ul li,
    [data-baseweb="popover"] [role="option"] {
        color: var(--text-primary) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
        background: transparent !important;
    }

    [data-baseweb="popover"] [data-baseweb="menu"] li:hover,
    [data-baseweb="popover"] ul li:hover,
    [data-baseweb="popover"] [role="option"]:hover {
        background: rgba(244, 140, 37, 0.15) !important;
    }

    /* Time picker */
    [data-baseweb="time-picker"],
    [data-baseweb="timepicker"],
    [data-baseweb="combobox"] {
        background: var(--bg-surface) !important;
    }

    [data-baseweb="combobox"] input {
        color: var(--text-primary) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
    }

    /* Time picker menu */
    [data-baseweb="menu"][aria-label*="time"],
    [data-baseweb="select"] [data-baseweb="menu"] {
        background: var(--bg-surface) !important;
    }

    /* Checkbox styling */
    .stCheckbox > label > span,
    .stCheckbox span {
        color: var(--text-primary) !important;
    }

    .stCheckbox [data-testid="stCheckbox"],
    .stCheckbox > div {
        background: transparent !important;
    }

    /* Checkbox box itself */
    [data-baseweb="checkbox"] {
        background: var(--bg-surface) !important;
        border-color: var(--border-dark) !important;
    }

    [data-baseweb="checkbox"]:hover {
        border-color: var(--primary) !important;
    }

    /* Alert boxes */
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        color: var(--text-primary) !important;
    }

    .stAlert p, .stInfo p, .stSuccess p, .stWarning p, .stError p {
        color: var(--text-primary) !important;
    }

    /* Form submit buttons */
    [data-testid="stForm"] button[kind="primaryFormSubmit"],
    [data-testid="stForm"] button[kind="secondaryFormSubmit"] {
        color: var(--primary) !important;
    }

    [data-testid="stForm"] button[kind="primaryFormSubmit"]:hover {
        background: var(--primary) !important;
        color: var(--bg-dark) !important;
    }

    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.25rem !important;
        transition: all var(--transition-normal) !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        border-color: var(--primary) !important;
    }

    .stTabs [aria-selected="true"] {
        background: var(--primary) !important;
        color: var(--bg-dark) !important;
        border-color: var(--primary) !important;
    }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--border-dark);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary);
    }

    /* ===== SUCCESS/ERROR MESSAGES ===== */
    .stSuccess {
        background: rgba(0, 255, 135, 0.1) !important;
        border: 1px solid rgba(0, 255, 135, 0.3) !important;
        border-radius: var(--radius-md) !important;
    }

    .stError {
        background: rgba(255, 50, 50, 0.1) !important;
        border: 1px solid rgba(255, 50, 50, 0.3) !important;
        border-radius: var(--radius-md) !important;
    }

    .stWarning {
        background: rgba(255, 215, 0, 0.1) !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: var(--radius-md) !important;
    }

    .stInfo {
        background: rgba(0, 212, 255, 0.1) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: var(--radius-md) !important;
    }

    /* ===== SPINNER ===== */
    .stSpinner > div {
        border-color: var(--primary) transparent transparent transparent !important;
    }

    /* ===== DESKTOP STYLES ===== */
    @media (min-width: 768px) {
        section[data-testid="stSidebar"] {
            display: flex !important;
            width: 280px !important;
            min-width: 280px !important;
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

        .mobile-only-buttons,
        .mobile-nav-section {
            display: none !important;
        }
    }

    /* ===== MOBILE STYLES ===== */
    @media (max-width: 767px) {
        .hero-title {
            font-size: 1.75rem;
            letter-spacing: 1px;
        }

        .hero-subtitle {
            font-size: 0.85rem;
            letter-spacing: 1px;
        }

        .welcome-banner {
            padding: 1.25rem;
        }

        .welcome-title {
            font-size: 1.25rem;
        }

        .welcome-banner::before {
            display: none;
        }

        .mobile-only-buttons {
            display: flex !important;
            gap: 0.5rem;
            margin-bottom: 1rem;
            padding: 0.5rem;
        }

        .mobile-only-buttons button {
            flex: 1;
            padding: 0.5rem !important;
            font-size: 0.8rem !important;
        }

        .login-container {
            margin: 1rem;
            padding: 1.25rem;
        }
    }

    /* ===== QUICK PLAY CARDS ===== */
    .stButton > button[kind="secondary"] {
        min-height: 60px !important;
        white-space: pre-wrap !important;
        line-height: 1.4 !important;
    }

    /* ===== GLOBAL TEXT COLOR OVERRIDES ===== */

    /* All paragraph and span text */
    .main p, .main span, .main div, .main label {
        color: var(--text-primary) !important;
    }

    /* Buttons on hover */
    .stButton > button:hover,
    .stButton > button:hover span,
    .stButton > button:hover p {
        color: var(--bg-dark) !important;
    }

    /* Form element values */
    input, textarea, select {
        color: var(--text-primary) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
    }

    /* Streamlit value display */
    [data-testid="stMarkdownContainer"] p {
        color: var(--text-primary) !important;
    }

    /* Column content */
    [data-testid="column"] p,
    [data-testid="column"] span,
    [data-testid="column"] div {
        color: var(--text-primary) !important;
    }

    /* Metric values */
    [data-testid="stMetricValue"] {
        color: var(--primary) !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-primary) !important;
    }

    /* Expander content */
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] span {
        color: var(--text-primary) !important;
    }

    /* Data editor / table */
    [data-testid="stDataFrame"] * {
        color: var(--text-primary) !important;
    }

    /* Caption text */
    .stCaption, figcaption {
        color: var(--text-secondary) !important;
    }

    /* Help text */
    .stHelp, [data-testid="stHelp"] {
        color: var(--text-muted) !important;
    }

    /* Tooltip */
    [data-testid="stTooltipContent"] {
        background: var(--bg-surface) !important;
        color: var(--text-primary) !important;
    }

    /* Empty state text */
    .stEmpty, [data-testid="stEmpty"] {
        color: var(--text-muted) !important;
    }

    /* Code blocks */
    code, pre {
        background: var(--bg-surface) !important;
        color: var(--primary) !important;
    }

    /* Markdown content */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: var(--primary) !important;
    }

    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: var(--text-primary) !important;
    }

    .stMarkdown a {
        color: var(--secondary) !important;
    }

    /* Horizontal rule */
    .stMarkdown hr {
        border-color: var(--border-dark) !important;
    }

    /* ===== DRILL CARD - MODERN ===== */
    .drill-card {
        background: var(--bg-surface);
        border: 1px solid var(--border-dark);
        border-radius: var(--radius-lg);
        padding: 1rem;
        margin-bottom: 1rem;
        transition: all var(--transition-normal);
        position: relative;
        overflow: hidden;
    }
    
    .drill-card:hover {
        border-color: var(--primary);
        transform: translateY(-2px);
    }

    .drill-card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .drill-card-desc {
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-bottom: 0.75rem;
        line-height: 1.5;
    }

    .drill-card-meta {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        align-items: center;
    }

    .drill-tag {
        background: rgba(244, 140, 37, 0.15);
        color: var(--primary);
        padding: 0.25rem 0.75rem;
        border-radius: var(--radius-full);
        font-size: 0.75rem;
        font-weight: 500;
    }

    .drill-tag.difficulty-beginner { background: rgba(0, 255, 135, 0.15); color: #00FF87; }
    .drill-tag.difficulty-intermediate { background: rgba(255, 215, 0, 0.15); color: #FFD700; }
    .drill-tag.difficulty-advanced { background: rgba(255, 68, 68, 0.15); color: #FF4444; }

    .drill-duration {
        color: var(--text-muted);
        font-size: 0.8rem;
    }

    .ai-badge {
        position: absolute;
        top: 10px;
        right: 10px;
        background: var(--primary);
        color: var(--bg-dark);
        padding: 0.2rem 0.6rem;
        border-radius: var(--radius-sm);
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
    }

    /* ===== TIMELINE ===== */
    .timeline-container {
        background: var(--bg-surface);
        border: 1px solid var(--border-dark);
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        margin: 1rem 0;
    }

    .timeline-segment {
        display: flex;
        align-items: center;
        padding: 0.75rem 1rem;
        margin: 0.4rem 0;
        border-radius: var(--radius-md);
        transition: all var(--transition-normal);
        position: relative;
    }

    .timeline-segment:hover {
        transform: translateX(3px);
    }

    .timeline-segment.warmup { background: rgba(0, 255, 135, 0.1); border-left: 3px solid #00FF87; }
    .timeline-segment.drill { background: rgba(244, 140, 37, 0.1); border-left: 3px solid var(--primary); }
    .timeline-segment.scrimmage { background: rgba(0, 212, 255, 0.1); border-left: 3px solid #00D4FF; }
    .timeline-segment.cooldown { background: rgba(155, 89, 182, 0.1); border-left: 3px solid #9B59B6; }
    .timeline-segment.break { background: rgba(255, 215, 0, 0.1); border-left: 3px solid #FFD700; }
    .timeline-segment.film { background: rgba(147, 112, 219, 0.1); border-left: 3px solid #9370DB; }

    .segment-time {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--primary);
        min-width: 50px;
    }

    .segment-title {
        flex: 1;
        font-weight: 600;
        color: var(--text-primary);
        margin-left: 1rem;
    }

    .segment-duration {
        color: var(--text-muted);
        font-size: 0.8rem;
        margin-left: auto;
    }

    /* ===== PAGE HEADER ===== */
    .page-header {
        background: linear-gradient(135deg, rgba(244, 140, 37, 0.08), rgba(244, 140, 37, 0.03));
        border: 1px solid var(--border-dark);
        border-radius: var(--radius-lg);
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
    }

    .page-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.25rem;
    }

    .page-subtitle {
        color: var(--text-secondary);
        font-size: 0.95rem;
    }

    /* ===== FILTER CHIPS ===== */
    .filter-section {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-bottom: 1rem;
    }

    .filter-chip {
        background: var(--bg-surface);
        border: 1px solid var(--border-dark);
        color: var(--text-primary);
        padding: 0.4rem 1rem;
        border-radius: var(--radius-full);
        font-size: 0.85rem;
        cursor: pointer;
        transition: all var(--transition-fast);
    }

    .filter-chip:hover {
        border-color: var(--primary);
        color: var(--primary);
    }

    .filter-chip.active {
        background: var(--primary);
        border-color: var(--primary);
        color: var(--bg-dark);
    }

    /* ===== STATS CARDS ===== */
    .stat-card {
        background: var(--bg-surface);
        border: 1px solid var(--border-dark);
        border-radius: var(--radius-lg);
        padding: 1rem;
        text-align: center;
    }

    .stat-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--primary);
    }

    .stat-label {
        color: var(--text-muted);
        font-size: 0.8rem;
        margin-top: 0.25rem;
    }

    /* ===== EMPTY STATE ===== */
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: var(--text-muted);
    }

    .empty-state-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        opacity: 0.4;
    }

    .empty-state-text {
        font-size: 1rem;
        margin-bottom: 0.75rem;
        color: var(--text-secondary);
    }

    /* ===== ACTION BUTTONS ROW ===== */
    .action-row {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.75rem;
    }

    /* ===== AI RECOMMENDED CHIP ===== */
    .ai-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(244, 140, 37, 0.15);
        border: 1px solid rgba(244, 140, 37, 0.3);
        color: var(--primary);
        padding: 0.4rem 0.875rem;
        border-radius: var(--radius-full);
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* ===== NAV LINK ACTIVE ===== */
    .nav-link-active {
        background: rgba(244, 140, 37, 0.1) !important;
        color: var(--primary) !important;
        border-left: 3px solid var(--primary) !important;
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