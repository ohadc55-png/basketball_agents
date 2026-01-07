# -*- coding: utf-8 -*-
"""
Basketball Coaching Staff - Virtual Locker Room
A multi-agent AI application for basketball coaches
Built with Streamlit and Google Gemini API
"""

import streamlit as st
import google.generativeai as genai
from enum import Enum

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

LOGO_URL = "https://i.postimg.cc/DfYpGxMy/Fashion-Bran-Logo.png"
BACKGROUND_URL = "https://i.postimg.cc/nr6WXxHh/wlm-kdwrsl.jpg"

class Agent(Enum):
    HEAD_ASSISTANT = "head_assistant"
    TACTICIAN = "tactician"
    SKILLS_COACH = "skills_coach"

AGENT_INFO = {
    Agent.HEAD_ASSISTANT: {
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

# System instructions for each agent
SYSTEM_INSTRUCTIONS = {
    Agent.HEAD_ASSISTANT: """You are the Head Assistant Coach of a professional basketball coaching staff. 
Your role is to handle general basketball inquiries, team management questions, and coordinate the coaching staff.
You are knowledgeable about all aspects of basketball but defer to specialists when appropriate.
Be professional, supportive, and helpful.

IMPORTANT: You MUST detect the language of the user's input and respond in the SAME language.
If the user writes in Hebrew, respond in Hebrew. If in English, respond in English.
This is crucial for effective communication with coaches from different backgrounds.""",

    Agent.TACTICIAN: """You are an elite basketball strategist with Euroleague-level expertise.
Your specializations include:
- Spacing and floor geometry
- Modern defensive schemes: Switch-all, Hedge & Recover, Drop Coverage, ICE, Blue/Nail
- ATOs (After Time Out plays) and SLOBs/BLOBs
- Breaking zone defenses (1-3-1, 2-3, Match-up)
- Transition offense and early offense concepts
- Pick and Roll coverage variations
- Help-side rotations and closeout principles

Be concise, professional, and tactical. Use basketball terminology appropriately.
When explaining plays, describe them clearly and suggest when they're most effective.

IMPORTANT: You MUST detect the language of the user's input and respond in the SAME language.
If the user writes in Hebrew, respond in Hebrew. If in English, respond in English.
Use standard basketball terms even in Hebrew responses when there's no good translation.""",

    Agent.SKILLS_COACH: """You are a top-tier Player Development Coach with expertise in:
- Shooting mechanics and biomechanics
- Ball handling progressions (stationary to game-speed)
- Footwork patterns (pivots, euro-steps, step-backs, jab series)
- Finishing at the rim (floaters, layup packages)
- Age-appropriate training:
  * Mini-basket (U10): Fun, coordination, basic skills
  * Youth (U12-U14): Fundamentals, movement patterns
  * Juniors (U16-U18): Position-specific development
  * Pros: Advanced moves, efficiency, maintenance

Be encouraging but demanding. Push for excellence while respecting developmental stages.
Provide specific drills and progressions when asked.

IMPORTANT: You MUST detect the language of the user's input and respond in the SAME language.
If the user writes in Hebrew, respond in Hebrew. If in English, respond in English."""
}

# Fixed model - no selection needed
MODEL_NAME = "gemini-1.5-flash"

ROUTER_PROMPT = """Analyze the following basketball coaching question and determine which specialist should handle it.

ROUTING RULES:
1. TACTICIAN - Route here if the question is about:
   - Plays, sets, or offensive/defensive schemes
   - X's and O's, game strategy
   - Game management, timeouts, adjustments
   - Zone offense/defense, press breaks
   - Spacing, rotations, coverages
   - ATOs, SLOBs, BLOBs
   
2. SKILLS_COACH - Route here if the question is about:
   - Individual skill development (shooting, dribbling, passing)
   - Workouts, drills, training programs
   - Youth development, age-appropriate training
   - Biomechanics, footwork, technique
   - Player evaluation and improvement areas
   
3. HEAD_ASSISTANT - Handle yourself if:
   - General basketball questions
   - Team management, leadership
   - Motivation, communication
   - Questions that don't fit the above categories

Respond with ONLY ONE of these exact words: TACTICIAN, SKILLS_COACH, or HEAD_ASSISTANT

User's question: {question}

Your routing decision:"""


# ============================================================================
# CUSTOM CSS - NBA FUTURISTIC DESIGN
# ============================================================================

def get_custom_css():
    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    :root {{
        --primary-orange: #FF6B35;
        --bright-orange: #FF8C42;
        --dark-bg: #0D0D0D;
        --card-bg: rgba(20, 20, 20, 0.95);
        --neon-blue: #00D4FF;
        --neon-green: #00FF87;
        --text-primary: #FFFFFF;
        --text-secondary: #B0B0B0;
    }}
    
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.9)), url("{BACKGROUND_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D0D0D 0%, #1A1A1A 50%, #0D0D0D 100%);
        border-right: 1px solid rgba(255, 107, 53, 0.3);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdown"] {
        color: #FFFFFF;
    }
    
    .hero-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 50%, #FFFFFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 0.5rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 20px rgba(255, 107, 53, 0.5)); }
        to { filter: drop-shadow(0 0 30px rgba(255, 107, 53, 0.8)); }
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
        background: linear-gradient(135deg, rgba(20, 20, 20, 0.95) 0%, rgba(30, 30, 30, 0.9) 100%);
        border: 2px solid rgba(255, 107, 53, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 0 30px rgba(255, 107, 53, 0.2);
        position: relative;
    }
    
    .scoreboard::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, #FF6B35, transparent);
    }
    
    [data-testid="stChatMessage"] {
        background: linear-gradient(135deg, rgba(25, 25, 25, 0.9) 0%, rgba(35, 35, 35, 0.85) 100%);
        border: 1px solid rgba(255, 107, 53, 0.2);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.8rem 0;
    }
    
    [data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        background: rgba(20, 20, 20, 0.9) !important;
    }
    
    .stButton > button {
        font-family: 'Orbitron', monospace;
        font-weight: 600;
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.2) 0%, rgba(255, 107, 53, 0.1) 100%);
        color: #FF6B35;
        border: 2px solid #FF6B35;
        border-radius: 25px;
        padding: 0.6rem 1.5rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
        color: #000000;
        box-shadow: 0 0 30px rgba(255, 107, 53, 0.5);
        transform: translateY(-2px);
    }
    
    .welcome-banner {
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.15) 0%, rgba(255, 140, 66, 0.1) 50%, rgba(0, 212, 255, 0.05) 100%);
        border: 2px solid rgba(255, 107, 53, 0.4);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .welcome-banner::before {
        content: '🏀';
        position: absolute;
        top: -20px;
        right: -20px;
        font-size: 120px;
        opacity: 0.1;
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
        background: linear-gradient(90deg, transparent, rgba(255, 107, 53, 0.5), transparent);
        margin: 1.5rem 0;
    }
    
    [data-testid="stExpander"] {
        background: rgba(20, 20, 20, 0.8);
        border: 1px solid rgba(255, 107, 53, 0.3);
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .response-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.2) 0%, rgba(255, 107, 53, 0.1) 100%);
        border: 1px solid rgba(255, 107, 53, 0.5);
        border-radius: 20px;
        padding: 0.4rem 1rem;
        margin-bottom: 1rem;
        font-family: 'Orbitron', monospace;
        font-size: 0.85rem;
        font-weight: 600;
        color: #FF6B35;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0D0D0D;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #FF6B35, #FF8C42);
        border-radius: 4px;
    }
</style>
"""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_agent_from_value(agent_value):
    if isinstance(agent_value, Agent):
        return agent_value
    if isinstance(agent_value, str):
        for agent in Agent:
            if agent.value == agent_value or agent.name == agent_value:
                return agent
    return Agent.HEAD_ASSISTANT


def init_gemini():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        return True
    except KeyError:
        st.markdown("""
        <div style="background: rgba(255, 59, 48, 0.2); border: 1px solid #FF3B30; border-radius: 10px; padding: 1.5rem; margin: 1rem 0;">
            <h3 style="color: #FF3B30; font-family: 'Orbitron', monospace; margin: 0 0 1rem 0;">⚠️ API KEY REQUIRED</h3>
            <p style="color: #FFFFFF; font-family: 'Rajdhani', sans-serif;">Configure GEMINI_API_KEY in your secrets to start coaching!</p>
        </div>
        """, unsafe_allow_html=True)
        return False


def route_question(question):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = ROUTER_PROMPT.format(question=question)
        response = model.generate_content(prompt)
        result = response.text.strip().upper()
        
        if "TACTICIAN" in result:
            return Agent.TACTICIAN
        elif "SKILLS" in result or "COACH" in result:
            return Agent.SKILLS_COACH
        else:
            return Agent.HEAD_ASSISTANT
    except Exception as e:
        return Agent.HEAD_ASSISTANT


def get_agent_response(question, agent, chat_history):
    try:
        model = genai.GenerativeModel(
            MODEL_NAME,
            system_instruction=SYSTEM_INSTRUCTIONS[agent]
        )
        
        history_context = ""
        if chat_history:
            recent_history = chat_history[-6:]
            for msg in recent_history:
                role = "Coach" if msg["role"] == "user" else "Assistant"
                history_context += f"{role}: {msg['content']}\n"
        
        if history_context:
            full_prompt = f"""Previous conversation:
{history_context}

Current question from the coach: {question}

Provide a helpful, professional response:"""
        else:
            full_prompt = question
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def format_agent_response(response, agent):
    info = AGENT_INFO[agent]
    badge_html = f"""<div class="response-badge">
        <span>{info['icon']}</span>
        <span>{info['name']}</span>
    </div>"""
    return f"{badge_html}\n\n{response}"


# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_sidebar():
    with st.sidebar:
        # Logo
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <img src="{LOGO_URL}" style="width: 180px; margin-bottom: 0.5rem;">
        </div>
        <div class="sidebar-divider"></div>
        """, unsafe_allow_html=True)
        
        # Coaching Staff
        st.markdown("""
        <div style="font-family: 'Orbitron', monospace; color: #FF6B35; font-size: 0.9rem; margin-bottom: 1rem; letter-spacing: 2px;">
            👥 COACHING STAFF
        </div>
        """, unsafe_allow_html=True)
        
        for agent in Agent:
            info = AGENT_INFO[agent]
            with st.expander(f"{info['icon']} {info['name']}", expanded=False):
                st.markdown(f"""
                <div style="font-family: 'Rajdhani', sans-serif;">
                    <div style="color: {info['color']}; font-weight: 600;">{info['title']}</div>
                    <div style="color: #888; font-size: 0.85rem;">{info['specialty']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
        if st.button("🗑️ CLEAR COURT", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("""
        <div class="sidebar-divider"></div>
        <div style="text-align: center; padding: 1rem;">
            <div style="font-family: 'Rajdhani', sans-serif; color: #666; font-size: 0.8rem;">
                Powered by<br>
                <span style="color: #FF6B35; font-family: 'Orbitron', monospace;">GOOGLE GEMINI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_header():
    st.markdown(f"""
    <div class="scoreboard">
        <div style="text-align: center;">
            <img src="{LOGO_URL}" style="width: 150px; margin-bottom: 1rem;">
        </div>
        <div class="hero-title">BASKETBALL AI</div>
        <div class="hero-subtitle">Virtual Locker Room</div>
    </div>
    """, unsafe_allow_html=True)


def render_welcome_banner():
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="welcome-banner">
            <div class="welcome-title">👋 WELCOME, COACH!</div>
            <div class="welcome-text">Your AI coaching staff is ready for action. Ask anything about basketball strategy, player development, or team management.</div>
            <div class="welcome-text" style="margin-top: 0.5rem; direction: rtl;">ברוכים הבאים! אפשר לשאול בעברית או באנגלית 🇮🇱</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="font-family: 'Orbitron', monospace; color: #FF6B35; font-size: 0.9rem; margin: 1.5rem 0 1rem 0; letter-spacing: 2px;">
            ⚡ QUICK PLAYS
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 ZONE OFFENSE", use_container_width=True, key="btn1"):
                st.session_state.starter_prompt = "What are the best strategies to beat a 2-3 zone defense?"
                st.rerun()
        
        with col2:
            if st.button("💪 SHOOTING DRILLS", use_container_width=True, key="btn2"):
                st.session_state.starter_prompt = "What are good shooting drills for U14 players?"
                st.rerun()
        
        with col3:
            if st.button("🎯 תרגילי כדרור", use_container_width=True, key="btn3"):
                st.session_state.starter_prompt = "תן לי תרגילי כדרור מתקדמים לשחקני נוער"
                st.rerun()
        
        if "starter_prompt" in st.session_state:
            prompt = st.session_state.starter_prompt
            del st.session_state.starter_prompt
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            agent = route_question(prompt)
            response = get_agent_response(prompt, agent, [])
            formatted_response = format_agent_response(response, agent)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": formatted_response,
                "agent": agent.value
            })
            st.rerun()


def render_chat_interface():
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(message["content"])
        else:
            agent = get_agent_from_value(message.get("agent", Agent.HEAD_ASSISTANT))
            info = AGENT_INFO[agent]
            with st.chat_message("assistant", avatar=info["icon"]):
                st.markdown(message["content"], unsafe_allow_html=True)
    
    if prompt := st.chat_input("Ask your coaching question... | שאל את שאלתך..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        with st.spinner("🏀 Analyzing play..."):
            agent = route_question(prompt)
        
        info = AGENT_INFO[agent]
        with st.chat_message("assistant", avatar=info["icon"]):
            with st.spinner(f"Consulting {info['name']}..."):
                response = get_agent_response(
                    prompt, 
                    agent, 
                    st.session_state.messages[:-1]
                )
                formatted_response = format_agent_response(response, agent)
            
            st.markdown(formatted_response, unsafe_allow_html=True)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": formatted_response,
            "agent": agent.value
        })


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    st.set_page_config(
        page_title="HOOPS AI - Basketball Coaching Staff",
        page_icon="🏀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if not init_gemini():
        st.stop()
    
    render_sidebar()
    render_header()
    render_welcome_banner()
    render_chat_interface()


if __name__ == "__main__":
    main()