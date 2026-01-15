# -*- coding: utf-8 -*-
"""
HOOPS AI - Styles (Premium Edition)
Advanced CSS with animations, glassmorphism, and modern UI
"""

from config import BACKGROUND_URL

# ============================================================================
# CSS TEMPLATE - PREMIUM DESIGN
# ============================================================================
CSS_TEMPLATE = """
<style>
    /* ===== FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* ===== CSS VARIABLES ===== */
    :root {
        --primary: #FF6B35;
        --primary-light: #FF8C42;
        --primary-dark: #E55A2B;
        --secondary: #00D4FF;
        --accent: #FFD700;
        --success: #00FF87;
        --bg-dark: #0D0D0D;
        --bg-card: rgba(20, 20, 20, 0.85);
        --bg-glass: rgba(255, 255, 255, 0.05);
        --text-primary: #FFFFFF;
        --text-secondary: #B0B0B0;
        --text-muted: #666666;
        --border-glow: rgba(255, 107, 53, 0.5);
        --shadow-glow: rgba(255, 107, 53, 0.3);
        --radius-sm: 10px;
        --radius-md: 15px;
        --radius-lg: 20px;
        --radius-xl: 25px;
        --transition-fast: 0.2s ease;
        --transition-normal: 0.3s ease;
        --transition-slow: 0.5s ease;
    }
    
    /* ===== KEYFRAME ANIMATIONS ===== */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 20px var(--shadow-glow); }
        50% { box-shadow: 0 0 40px var(--shadow-glow), 0 0 60px rgba(255, 107, 53, 0.2); }
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes bounce-ball {
        0%, 100% { transform: translateY(0) scale(1); }
        25% { transform: translateY(-20px) scale(0.95); }
        50% { transform: translateY(0) scale(1.05); }
        75% { transform: translateY(-10px) scale(0.98); }
    }
    
    @keyframes spin-slow {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* ===== MAIN APP BACKGROUND ===== */
    .stApp {
        background: 
            linear-gradient(135deg, rgba(13,13,13,0.92) 0%, rgba(20,20,20,0.88) 50%, rgba(13,13,13,0.92) 100%),
            url('BACKGROUND_URL_PLACEHOLDER');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* ===== AGENT CARDS HOVER ===== */
    .agent-card:hover {
        transform: translateX(5px) !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3) !important;
        border-left-width: 6px !important;
    }
    
    /* ===== GLOBAL TEXT ===== */
    .stApp p, .stApp span, .stApp li, .stApp label, .stApp div {
        color: var(--text-primary);
        font-family: 'Inter', 'Rajdhani', sans-serif;
    }
    
    /* ===== MAIN CONTAINER ===== */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        animation: fadeIn 0.5s ease;
    }
    
    /* ===== GLASSMORPHISM SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg, 
            rgba(13, 13, 13, 0.95) 0%, 
            rgba(20, 20, 20, 0.92) 30%,
            rgba(25, 25, 25, 0.90) 70%,
            rgba(13, 13, 13, 0.95) 100%
        );
        border-right: 1px solid var(--border-glow);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--secondary), var(--primary));
        background-size: 200% 100%;
        animation: gradient-shift 3s ease infinite;
    }
    
    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }
    
    /* Sidebar Expanders - Agent Cards */
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.8), rgba(40, 40, 40, 0.6)) !important;
        border: 1px solid rgba(255, 107, 53, 0.2) !important;
        border-radius: var(--radius-md) !important;
        margin-bottom: 0.5rem !important;
        transition: all var(--transition-normal) !important;
        overflow: hidden;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"]:hover {
        border-color: var(--primary) !important;
        box-shadow: 0 5px 20px rgba(255, 107, 53, 0.2) !important;
        transform: translateX(5px);
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-family: 'Rajdhani', sans-serif !important;
        transition: all var(--transition-fast) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
        color: var(--primary) !important;
    }
    
    /* ===== PREMIUM HERO SECTION ===== */
    .hero-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.8rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, var(--primary), var(--primary-light), #FFFFFF, var(--primary-light), var(--primary));
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-bottom: 0.5rem;
        animation: gradient-shift 4s ease infinite;
        text-shadow: 0 0 40px rgba(255, 107, 53, 0.5);
    }
    
    .hero-subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        text-align: center;
        color: var(--text-secondary);
        letter-spacing: 8px;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
        opacity: 0.9;
    }
    
    /* ===== GLASSMORPHISM SCOREBOARD ===== */
    .scoreboard {
        background: linear-gradient(135deg, var(--bg-card), rgba(30, 30, 30, 0.8));
        border: 1px solid var(--border-glow);
        border-radius: var(--radius-lg);
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            0 0 40px var(--shadow-glow),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .scoreboard::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 107, 53, 0.1),
            transparent
        );
        animation: shimmer 3s ease infinite;
    }
    
    /* ===== PREMIUM WELCOME BANNER ===== */
    .welcome-banner {
        background: linear-gradient(
            135deg, 
            rgba(255, 107, 53, 0.15) 0%, 
            rgba(255, 140, 66, 0.1) 25%,
            rgba(0, 212, 255, 0.08) 50%,
            rgba(255, 107, 53, 0.12) 100%
        );
        border: 1px solid rgba(255, 107, 53, 0.3);
        border-radius: var(--radius-lg);
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
        animation: fadeIn 0.6s ease;
    }
    
    .welcome-banner::before {
        content: '🏀';
        position: absolute;
        top: 15px;
        right: 20px;
        font-size: 3rem;
        opacity: 0.15;
        animation: bounce-ball 2s ease infinite;
    }
    
    .welcome-title {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.8rem;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .welcome-text {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.15rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* ===== MODERN CHAT MESSAGES ===== */
    [data-testid="stChatMessage"] {
        background: linear-gradient(135deg, rgba(25, 25, 25, 0.9), rgba(35, 35, 35, 0.85));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: var(--radius-lg);
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        animation: fadeIn 0.4s ease;
        transition: all var(--transition-normal);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    [data-testid="stChatMessage"]:hover {
        border-color: rgba(255, 107, 53, 0.2);
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
    }
    
    /* User messages - right aligned style */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(255, 140, 66, 0.1));
        border-color: rgba(255, 107, 53, 0.3);
        animation: slideInRight 0.4s ease;
    }
    
    /* Assistant messages */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        animation: slideInLeft 0.4s ease;
    }
    
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div {
        color: var(--text-primary) !important;
    }
    
    [data-testid="stChatMessage"] strong {
        color: var(--primary) !important;
        font-weight: 700;
    }
    
    [data-testid="stChatMessage"] code {
        background: rgba(255, 107, 53, 0.2) !important;
        color: var(--primary-light) !important;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
    }
    
    /* ===== PREMIUM CHAT INPUT ===== */
    [data-testid="stChatInput"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    [data-testid="stChatInput"] textarea {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        background: linear-gradient(135deg, rgba(25, 25, 25, 0.95), rgba(30, 30, 30, 0.9)) !important;
        border: 2px solid rgba(255, 107, 53, 0.4) !important;
        border-radius: var(--radius-xl) !important;
        padding: 1rem 1.5rem !important;
        transition: all var(--transition-normal) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }
    
    [data-testid="stChatInput"] textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 
            0 0 20px var(--shadow-glow),
            0 4px 20px rgba(0, 0, 0, 0.3) !important;
        outline: none !important;
    }
    
    [data-testid="stChatInput"] textarea::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
        font-style: italic;
    }
    
    [data-testid="stChatInput"] button {
        background: linear-gradient(135deg, var(--primary), var(--primary-light)) !important;
        border-radius: 50% !important;
        color: #000 !important;
        transition: all var(--transition-normal) !important;
        box-shadow: 0 4px 15px var(--shadow-glow) !important;
    }
    
    [data-testid="stChatInput"] button:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 6px 25px var(--shadow-glow) !important;
    }
    
    /* ===== BOTTOM AREA ===== */
    [data-testid="stBottom"] {
        background: linear-gradient(180deg, transparent, rgba(13, 13, 13, 0.98)) !important;
        border-top: 1px solid rgba(255, 107, 53, 0.2) !important;
        padding-top: 1rem !important;
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
        font-size: 0.75rem !important;
        padding: 0.5rem 0.3rem !important;
        letter-spacing: 0.5px !important;
        min-height: 45px !important;
        white-space: nowrap !important;
    }
    
    /* ===== PREMIUM BUTTONS ===== */
    .stButton > button {
        font-family: 'Orbitron', monospace !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.2), rgba(255, 107, 53, 0.1)) !important;
        color: var(--primary) !important;
        border: 2px solid var(--primary) !important;
        border-radius: var(--radius-xl) !important;
        padding: 0.6rem 1.5rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        transition: all var(--transition-normal) !important;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.1) !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary), var(--primary-light)) !important;
        color: #000 !important;
        transform: translateY(-3px) !important;
        box-shadow: 
            0 8px 25px var(--shadow-glow),
            0 0 40px rgba(255, 107, 53, 0.3) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* ===== PREMIUM RESPONSE BADGE ===== */
    .response-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.25), rgba(255, 140, 66, 0.15));
        border: 1px solid var(--primary);
        border-radius: var(--radius-xl);
        padding: 0.5rem 1.2rem;
        margin-bottom: 1rem;
        font-family: 'Orbitron', monospace;
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--primary);
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.2);
        animation: fadeIn 0.3s ease;
    }
    
    .response-badge span:first-child {
        font-size: 1.2rem;
        animation: bounce-ball 2s ease infinite;
    }
    
    /* ===== PREMIUM FILE UPLOADER ===== */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.95), rgba(40, 40, 40, 0.9)) !important;
        border: 2px dashed var(--primary) !important;
        border-radius: var(--radius-lg) !important;
        padding: 1.5rem !important;
        transition: all var(--transition-normal) !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-style: solid !important;
        box-shadow: 0 8px 30px var(--shadow-glow) !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: var(--text-primary) !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stFileUploader"] section {
        background: rgba(50, 50, 50, 0.5) !important;
        border: 2px dashed rgba(255, 107, 53, 0.3) !important;
        border-radius: var(--radius-md) !important;
        transition: all var(--transition-normal) !important;
    }
    
    [data-testid="stFileUploader"] section:hover {
        border-color: var(--primary) !important;
        background: rgba(255, 107, 53, 0.1) !important;
    }
    
    [data-testid="stFileUploader"] section > div {
        color: var(--text-primary) !important;
    }
    
    [data-testid="stFileUploader"] small {
        color: var(--primary) !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, var(--primary), var(--primary-light)) !important;
        color: #000 !important;
        font-weight: 700 !important;
        border-radius: var(--radius-md) !important;
        transition: all var(--transition-normal) !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 5px 20px var(--shadow-glow) !important;
    }
    
    /* ===== PREMIUM SELECTBOX ===== */
    [data-testid="stSelectbox"] label {
        color: var(--text-primary) !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSelectbox"] > div > div {
        background: linear-gradient(135deg, rgba(40, 40, 40, 0.95), rgba(50, 50, 50, 0.9)) !important;
        border: 1px solid rgba(255, 107, 53, 0.4) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        transition: all var(--transition-normal) !important;
    }
    
    [data-testid="stSelectbox"] > div > div:hover {
        border-color: var(--primary) !important;
    }
    
    /* ===== SIDEBAR DIVIDER ===== */
    .sidebar-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--primary), var(--secondary), var(--primary), transparent);
        margin: 1.5rem 0;
        border-radius: 1px;
        opacity: 0.6;
    }
    
    /* ===== PREMIUM LOGIN CONTAINER ===== */
    .login-container {
        background: linear-gradient(135deg, rgba(20, 20, 20, 0.95), rgba(30, 30, 30, 0.9));
        border: 1px solid var(--border-glow);
        border-radius: var(--radius-lg);
        padding: 2.5rem;
        max-width: 500px;
        margin: 2rem auto;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.5),
            0 0 40px var(--shadow-glow);
        animation: fadeIn 0.6s ease;
    }
    
    /* ===== PROFILE CARD ===== */
    .profile-card {
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(255, 107, 53, 0.05));
        border: 1px solid rgba(255, 107, 53, 0.3);
        border-radius: var(--radius-md);
        padding: 1.2rem;
        margin: 0.5rem 0;
        transition: all var(--transition-normal);
    }
    
    .profile-card:hover {
        border-color: var(--primary);
        box-shadow: 0 5px 20px rgba(255, 107, 53, 0.2);
    }
    
    /* ===== FORM INPUTS ===== */
    .stTextInput input {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.9), rgba(40, 40, 40, 0.85)) !important;
        border: 1px solid rgba(255, 107, 53, 0.3) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        padding: 0.8rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all var(--transition-normal) !important;
    }
    
    .stTextInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 15px var(--shadow-glow) !important;
    }
    
    .stTextInput input::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 107, 53, 0.1) !important;
        border: 1px solid rgba(255, 107, 53, 0.3) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 600 !important;
        padding: 0.8rem 1.5rem !important;
        transition: all var(--transition-normal) !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 107, 53, 0.2) !important;
        border-color: var(--primary) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary), var(--primary-light)) !important;
        color: #000 !important;
        border-color: var(--primary) !important;
    }
    
    /* ===== PREMIUM SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--primary), var(--primary-light));
        border-radius: 5px;
        border: 2px solid var(--bg-dark);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, var(--primary-light), var(--primary));
    }
    
    /* ===== SUCCESS/ERROR MESSAGES ===== */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 255, 135, 0.15), rgba(0, 255, 135, 0.05)) !important;
        border: 1px solid rgba(0, 255, 135, 0.5) !important;
        border-radius: var(--radius-md) !important;
        animation: fadeIn 0.3s ease;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(255, 50, 50, 0.15), rgba(255, 50, 50, 0.05)) !important;
        border: 1px solid rgba(255, 50, 50, 0.5) !important;
        border-radius: var(--radius-md) !important;
        animation: fadeIn 0.3s ease;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(255, 215, 0, 0.05)) !important;
        border: 1px solid rgba(255, 215, 0, 0.5) !important;
        border-radius: var(--radius-md) !important;
        animation: fadeIn 0.3s ease;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(0, 212, 255, 0.05)) !important;
        border: 1px solid rgba(0, 212, 255, 0.5) !important;
        border-radius: var(--radius-md) !important;
        animation: fadeIn 0.3s ease;
    }
    
    /* ===== SPINNER OVERRIDE ===== */
    .stSpinner > div {
        border-color: var(--primary) transparent transparent transparent !important;
    }
    
    /* ===== DESKTOP STYLES ===== */
    @media (min-width: 768px) {
        section[data-testid="stSidebar"] {
            display: flex !important;
            width: 320px !important;
            min-width: 320px !important;
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
            font-size: 1.8rem;
            letter-spacing: 2px;
        }
        
        .hero-subtitle {
            font-size: 0.9rem;
            letter-spacing: 4px;
        }
        
        .welcome-banner {
            padding: 1.5rem;
        }
        
        .welcome-title {
            font-size: 1.4rem;
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
            padding: 1.5rem;
        }
    }
    
    /* ===== QUICK PLAY CARDS ===== */
    .stButton > button[kind="secondary"] {
        min-height: 80px !important;
        white-space: pre-wrap !important;
        line-height: 1.4 !important;
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