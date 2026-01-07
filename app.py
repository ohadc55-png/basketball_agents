# -*- coding: utf-8 -*-
"""
HOOPS AI - Basketball Coaching Staff
Virtual Locker Room with Multi-Agent System
Powered by OpenAI GPT
"""

import streamlit as st
from openai import OpenAI
from enum import Enum

# ============================================================================
# PAGE CONFIG - Must be first Streamlit command
# ============================================================================
st.set_page_config(
    page_title="HOOPS AI - Your Personal Assistant Coach",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CONSTANTS
# ============================================================================
LOGO_URL = "https://i.postimg.cc/DfYpGxMy/Fashion-Bran-Logo.png"
BACKGROUND_URL = "https://i.postimg.cc/nr6WXxHh/wlm-kdwrsl.jpg"

class Agent(Enum):
    HEAD_COACH = "head_coach"
    TACTICIAN = "tactician"
    SKILLS_COACH = "skills_coach"

AGENT_INFO = {
    Agent.HEAD_COACH: {
        "name": "HEAD COACH",
        "icon": "🎯",
        "title": "General Manager",
        "specialty": "Team Leadership & Strategy",
        "color": "#FF6B35"
    },
    Agent.TACTICIAN: {
        "name": "THE TACTICIAN",
        "icon": "📋",
        "title": "Strategic Mastermind",
        "specialty": "X's & O's Expert",
        "color": "#00D4FF"
    },
    Agent.SKILLS_COACH: {
        "name": "SKILLS COACH",
        "icon": "💪",
        "title": "Player Development",
        "specialty": "Training & Drills",
        "color": "#00FF87"
    }
}

SYSTEM_PROMPTS = {
    Agent.HEAD_COACH: """You are the Head Coach of a professional basketball coaching staff.
Handle general basketball inquiries, team management, and coordination.
Be professional, supportive, and helpful.
IMPORTANT: Detect the user's language and respond in the SAME language (Hebrew or English).""",

    Agent.TACTICIAN: """You are an elite basketball strategist (Euroleague-level).
Expertise: Spacing, defensive schemes (Switch, Hedge, Drop, ICE), ATOs, SLOBs/BLOBs,
zone offense/defense, Pick & Roll coverage, rotations.
Be concise and tactical. Use proper basketball terminology.
IMPORTANT: Detect the user's language and respond in the SAME language (Hebrew or English).""",

    Agent.SKILLS_COACH: """You are a top Player Development Coach.
Expertise: Shooting mechanics, ball handling, footwork, finishing at rim.
Age-appropriate training: Mini-basket (U10), Youth (U12-U14), Juniors (U16-U18), Pros.
Be encouraging but demanding.
IMPORTANT: Detect the user's language and respond in the SAME language (Hebrew or English)."""
}

ROUTER_PROMPT = """Determine which coach should answer this basketball question.
Rules:
- TACTICIAN: plays, schemes, X's & O's, game strategy, zones, ATOs
- SKILLS_COACH: drills, shooting, dribbling, footwork, player development, training
- HEAD_COACH: general questions, team management, motivation, other

Question: {question}

Answer with ONE word only: TACTICIAN, SKILLS_COACH, or HEAD_COACH"""

# ============================================================================
# CSS STYLING - Background at 50% opacity (more visible)
# ============================================================================
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('BACKGROUND_URL_PLACEHOLDER');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(13,13,13,0.95) 0%, rgba(26,26,26,0.95) 50%, rgba(13,13,13,0.95) 100%);
        border-right: 1px solid rgba(255, 107, 53, 0.3);
    }
    
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
    
    .scoreboard {
        background: linear-gradient(135deg, rgba(20,20,20,0.9), rgba(30,30,30,0.85));
        border: 2px solid rgba(255, 107, 53, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 0 30px rgba(255, 107, 53, 0.2);
        backdrop-filter: blur(10px);
    }
    
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
    
    [data-testid="stChatInput"] {
        background: linear-gradient(135deg, #FF6B35, #FF8C42) !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 0.8rem 1rem !important;
    }
    
    [data-testid="stChatInput"] textarea {
        color: #000000 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important;
        background: #FFFFFF !important;
        border-radius: 20px !important;
        padding: 0.5rem 1rem !important;
    }
    
    [data-testid="stChatInput"] textarea::placeholder {
        color: #666666 !important;
    }
    
    [data-testid="stChatInput"] button {
        background: #000000 !important;
        border-radius: 50% !important;
        color: #FF6B35 !important;
    }
    
    [data-testid="stChatInput"] button:hover {
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.6) !important;
    }
    
    [data-testid="stBottom"] {
        background: linear-gradient(135deg, #FF6B35, #FF8C42) !important;
        padding: 1rem !important;
        border-top: 2px solid rgba(255, 107, 53, 0.8) !important;
    }
    
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
    
    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,107,53,0.5), transparent);
        margin: 1.5rem 0;
    }
    
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
    
    ::-webkit-scrollbar {width: 8px;}
    ::-webkit-scrollbar-track {background: #0D0D0D;}
    ::-webkit-scrollbar-thumb {background: linear-gradient(#FF6B35, #FF8C42); border-radius: 4px;}
</style>
""".replace('BACKGROUND_URL_PLACEHOLDER', BACKGROUND_URL)

# ============================================================================
# OPENAI SETUP
# ============================================================================
@st.cache_resource
def get_openai_client():
    """Initialize OpenAI client"""
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            return None
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize OpenAI: {e}")
        return None

# ============================================================================
# AGENT LOGIC
# ============================================================================
def route_question(question, client):
    """Route question to appropriate agent"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": ROUTER_PROMPT.format(question=question)}],
            max_tokens=20,
            temperature=0
        )
        result = response.choices[0].message.content.strip().upper()
        
        if "TACTICIAN" in result:
            return Agent.TACTICIAN
        elif "SKILLS" in result:
            return Agent.SKILLS_COACH
        return Agent.HEAD_COACH
    except Exception:
        return Agent.HEAD_COACH

def get_agent_response(question, agent, chat_history, client):
    """Get response from specific agent"""
    try:
        # Build messages list
        messages = [{"role": "system", "content": SYSTEM_PROMPTS[agent]}]
        
        # Add recent history
        if chat_history:
            for msg in chat_history[-4:]:
                role = "user" if msg["role"] == "user" else "assistant"
                content = msg.get("raw_content", msg["content"])
                messages.append({"role": role, "content": content})
        
        # Add current question
        messages.append({"role": "user", "content": question})
        
        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def format_response(response, agent):
    """Format response with agent badge"""
    info = AGENT_INFO[agent]
    badge = f'<div class="response-badge"><span>{info["icon"]}</span><span>{info["name"]}</span></div>'
    return badge + "\n\n" + response

def get_agent_from_value(value):
    """Convert string value to Agent enum"""
    if isinstance(value, Agent):
        return value
    for agent in Agent:
        if agent.value == value:
            return agent
    return Agent.HEAD_COACH

# ============================================================================
# UI COMPONENTS
# ============================================================================
def render_sidebar():
    with st.sidebar:
        st.markdown(f'''
        <div style="text-align:center; padding:1rem;">
            <img src="{LOGO_URL}" style="width:180px;">
        </div>
        <div class="sidebar-divider"></div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div style="font-family:'Orbitron',monospace; color:#FF6B35; font-size:0.9rem; margin-bottom:1rem; letter-spacing:2px;">
            👥 COACHING STAFF
        </div>
        ''', unsafe_allow_html=True)
        
        for agent in Agent:
            info = AGENT_INFO[agent]
            with st.expander(f"{info['icon']} {info['name']}", expanded=False):
                st.markdown(f'''
                <div style="font-family:'Rajdhani',sans-serif;">
                    <div style="color:{info['color']}; font-weight:600;">{info['title']}</div>
                    <div style="color:#888; font-size:0.85rem;">{info['specialty']}</div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
        if st.button("🗑️ CLEAR COURT", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown('''
        <div class="sidebar-divider"></div>
        <div style="text-align:center; padding:1rem;">
            <div style="font-family:'Rajdhani',sans-serif; color:#666; font-size:0.8rem;">
                Powered by<br>
                <span style="color:#FF6B35; font-family:'Orbitron',monospace;">OpenAI GPT</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)

def render_header():
    st.markdown('''
    <div class="scoreboard">
        <div class="hero-title">HOOPS AI</div>
        <div class="hero-subtitle">Your Personal Assistant Coach</div>
    </div>
    ''', unsafe_allow_html=True)

def render_welcome():
    if not st.session_state.messages:
        st.markdown('''
        <div class="welcome-banner">
            <div class="welcome-title">👋 WELCOME, COACH!</div>
            <div class="welcome-text">Your AI coaching staff is ready. Ask anything about basketball strategy, player development, or team management.</div>
            <div class="welcome-text" style="margin-top:0.5rem; direction:rtl;">ברוכים הבאים! אפשר לשאול בעברית או באנגלית 🇮🇱</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div style="font-family:'Orbitron',monospace; color:#FF6B35; font-size:0.9rem; margin:1.5rem 0 1rem; letter-spacing:2px;">
            ⚡ QUICK PLAYS
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📋 ZONE OFFENSE", use_container_width=True):
                st.session_state.pending_prompt = "What are the best strategies to beat a 2-3 zone defense?"
        with col2:
            if st.button("💪 SHOOTING DRILLS", use_container_width=True):
                st.session_state.pending_prompt = "What are good shooting drills for U14 players?"
        with col3:
            if st.button("🎯 תרגילי כדרור", use_container_width=True):
                st.session_state.pending_prompt = "תן לי תרגילי כדרור מתקדמים לשחקני נוער"

def render_chat(client):
    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])
        else:
            agent = get_agent_from_value(msg.get("agent", Agent.HEAD_COACH))
            with st.chat_message("assistant", avatar=AGENT_INFO[agent]["icon"]):
                st.markdown(msg["content"], unsafe_allow_html=True)
    
    # Handle pending prompt from quick buttons
    prompt = st.session_state.pop("pending_prompt", None)
    
    # Or get new input
    if not prompt:
        prompt = st.chat_input("Ask your coaching question... | שאל את שאלתך...")
    
    if prompt:
        # Show user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Route and respond
        with st.spinner("🏀 Analyzing..."):
            agent = route_question(prompt, client)
        
        info = AGENT_INFO[agent]
        with st.chat_message("assistant", avatar=info["icon"]):
            with st.spinner(f"Consulting {info['name']}..."):
                raw_response = get_agent_response(prompt, agent, st.session_state.messages[:-1], client)
                formatted = format_response(raw_response, agent)
            st.markdown(formatted, unsafe_allow_html=True)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": formatted,
            "raw_content": raw_response,
            "agent": agent.value
        })
        st.rerun()

# ============================================================================
# MAIN
# ============================================================================
def main():
    # Apply CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize OpenAI
    client = get_openai_client()
    if not client:
        st.error("⚠️ Please configure OPENAI_API_KEY in your Streamlit secrets")
        st.info("Go to Settings > Secrets and add: OPENAI_API_KEY = \"sk-your-key-here\"")
        st.stop()
    
    # Render UI
    render_sidebar()
    render_header()
    render_welcome()
    render_chat(client)

if __name__ == "__main__":
    main()