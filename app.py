# -*- coding: utf-8 -*-
"""
HOOPS AI - Basketball Coaching Staff
Main Application File (Optimized)
"""

import streamlit as st

from config import (
    APP_TITLE, APP_ICON, LOGO_URL,
    AGE_GROUPS, LEVELS, ALLOWED_FILE_TYPES, ANALYSIS_TYPES,
    Agent, AGENT_INFO
)
from styles import CUSTOM_CSS
from utils import (
    get_supabase_client, get_openai_client,
    get_coach_by_email, create_coach,
    get_coach_conversations, create_conversation,
    save_message, get_conversation_messages,
    route_question, get_agent_response,
    format_response, get_agent_from_value,
    read_uploaded_file, build_analysis_prompt
)
from logistics import render_logistics_page

# Page config must be first
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)


def render_login_page(supabase):
    """Render login/registration page"""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown('''
    <div class="scoreboard">
        <div class="hero-title">HOOPS AI</div>
        <div class="hero-subtitle">Your Personal Assistant Coach</div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 REGISTER"])
        
        with tab1:
            email = st.text_input("Email", key="login_email", placeholder="Enter your email")
            if st.button("LOGIN", use_container_width=True, key="login_btn"):
                if email:
                    coach = get_coach_by_email(supabase, email)
                    if coach:
                        st.session_state.logged_in = True
                        st.session_state.coach = coach
                        st.rerun()
                    else:
                        st.error("Coach not found. Please register first.")
                else:
                    st.warning("Please enter your email")
        
        with tab2:
            name = st.text_input("Full Name", key="reg_name", placeholder="Your name")
            email_reg = st.text_input("Email", key="reg_email", placeholder="Your email")
            team_name = st.text_input("Team Name", key="reg_team", placeholder="Your team")
            age_group = st.selectbox("Age Group", AGE_GROUPS, key="reg_age")
            level = st.selectbox("Level", LEVELS, key="reg_level")
            
            if st.button("REGISTER", use_container_width=True, key="register_btn"):
                if name and email_reg and team_name:
                    existing = get_coach_by_email(supabase, email_reg)
                    if existing:
                        st.error("Email already registered. Please login.")
                    else:
                        coach = create_coach(supabase, name, email_reg, team_name, age_group, level)
                        if coach:
                            st.session_state.logged_in = True
                            st.session_state.coach = coach
                            st.rerun()
                        else:
                            st.error("Registration failed. Please try again.")
                else:
                    st.warning("Please fill all fields")
        st.markdown('</div>', unsafe_allow_html=True)


def render_sidebar(supabase):
    """Render sidebar with logo, profile, and navigation"""
    coach = st.session_state.get('coach', {})
    
    with st.sidebar:
        # Logo
        st.markdown(f'<div style="text-align:center; padding:1rem 0;"><img src="{LOGO_URL}" style="width:150px; border-radius:10px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
        # Profile
        st.markdown('<div style="font-family:\'Orbitron\',monospace; color:#FF6B35; font-size:0.9rem; margin-bottom:0.5rem; letter-spacing:2px;">👤 COACH PROFILE</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="profile-card"><div style="font-weight:700; color:#FFFFFF; font-size:1.1rem;">{coach.get("name", "Coach")}</div><div style="color:#B0B0B0; font-size:0.9rem;">{coach.get("team_name", "")} | {coach.get("age_group", "")} | {coach.get("level", "")}</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
        # Navigation
        st.markdown('<div style="font-family:\'Orbitron\',monospace; color:#FF6B35; font-size:0.9rem; margin-bottom:0.5rem; letter-spacing:2px;">🧭 NAVIGATION</div>', unsafe_allow_html=True)
        
        # Initialize current page
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'chat'
        
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("💬 CHAT", use_container_width=True, key="nav_chat",
                        type="primary" if st.session_state.current_page == 'chat' else "secondary"):
                st.session_state.current_page = 'chat'
                st.rerun()
        with col_nav2:
            if st.button("📋 MANAGE", use_container_width=True, key="nav_logistics",
                        type="primary" if st.session_state.current_page == 'logistics' else "secondary"):
                st.session_state.current_page = 'logistics'
                st.rerun()
        
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
        # Only show chat-related items when on chat page
        if st.session_state.current_page == 'chat':
            # New Chat
            if st.button("➕ NEW CHAT", use_container_width=True, key="new_chat_btn"):
                st.session_state.current_conversation = None
                st.session_state.messages = []
                st.rerun()
            
            st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
            
            # Chat History
            st.markdown('<div style="font-family:\'Orbitron\',monospace; color:#FF6B35; font-size:0.9rem; margin-bottom:1rem; letter-spacing:2px;">📜 CHAT HISTORY</div>', unsafe_allow_html=True)
            
            conversations = get_coach_conversations(supabase, coach.get('id'))
        if conversations:
            for conv in conversations[:10]:
                title = conv.get('title', 'New Chat')[:30]
                if len(conv.get('title', '')) > 30:
                    title += "..."
                if st.button(f"💬 {title}", key=f"conv_{conv['id']}", use_container_width=True):
                    st.session_state.current_conversation = conv
                    msgs = get_conversation_messages(supabase, conv['id'])
                    st.session_state.messages = [
                        {
                            "role": m['role'],
                            "content": m['content'],
                            "raw_content": m['content'].split('\n\n', 1)[-1] if '\n\n' in m['content'] else m['content'],
                            "agent": m.get('agent')
                        }
                        for m in msgs
                    ]
                    st.rerun()
            else:
                st.markdown('<div style="color:#666; font-size:0.85rem;">No conversations yet</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
            
            # Coaching Staff - Using HTML cards instead of expanders
            st.markdown('<div style="font-family:\'Orbitron\',monospace; color:#FF6B35; font-size:0.9rem; margin-bottom:1rem; letter-spacing:2px;">👥 COACHING STAFF</div>', unsafe_allow_html=True)
            
            for agent in Agent:
                info = AGENT_INFO[agent]
                st.markdown(f'''
                <div class="agent-card" style="
                    background: linear-gradient(135deg, rgba(30,30,30,0.8), rgba(40,40,40,0.6));
                    border: 1px solid {info["color"]}40;
                    border-left: 4px solid {info["color"]};
                    border-radius: 10px;
                    padding: 0.8rem 1rem;
                    margin-bottom: 0.5rem;
                    transition: all 0.3s ease;
                    cursor: default;
                ">
                    <div style="display:flex; align-items:center; gap:0.5rem;">
                        <span style="font-size:1.3rem;">{info["icon"]}</span>
                        <div>
                            <div style="font-family:'Rajdhani',sans-serif; font-weight:700; color:#FFFFFF; font-size:0.9rem;">{info["name"]}</div>
                            <div style="color:{info["color"]}; font-size:0.75rem;">{info["specialty"]}</div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
        # Logout
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.coach = None
            st.session_state.messages = []
            st.session_state.current_conversation = None
            st.rerun()
        
        st.markdown('<div class="sidebar-divider"></div><div style="text-align:center; padding:1rem;"><div style="font-family:\'Rajdhani\',sans-serif; color:#666; font-size:0.8rem;">Powered by<br><span style="color:#FF6B35; font-family:\'Orbitron\',monospace;">OpenAI GPT</span></div></div>', unsafe_allow_html=True)


def render_header():
    """Render main header"""
    st.markdown('<div class="scoreboard"><div class="hero-title">HOOPS AI</div><div class="hero-subtitle">Your Personal Assistant Coach</div></div>', unsafe_allow_html=True)


def render_welcome():
    """Render welcome banner and quick plays"""
    if not st.session_state.messages:
        coach = st.session_state.get('coach', {})
        name = coach.get('name', '').split()[0] if coach.get('name') else ''
        
        st.markdown(f'''
        <div class="welcome-banner">
            <div class="welcome-title">👋 Hey Coach {name}!</div>
            <div class="welcome-text">Your AI coaching staff is ready. Ask anything about basketball strategy, player development, or team management.</div>
            <div class="welcome-text" style="margin-top:0.5rem;">Tailored for: <strong style="color:#FF6B35;">{coach.get("team_name", "")} | {coach.get("age_group", "")} | {coach.get("level", "")}</strong></div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div style="font-family:\'Orbitron\',monospace; color:#FF6B35; font-size:0.9rem; margin:1.5rem 0 1rem; letter-spacing:2px;">⚡ QUICK PLAYS</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, _ = st.columns(2)
        
        quick_plays = [
            (col1, "🎯 PRACTICE PLAN\n\nBuild a 90-min practice", "Build me a 90-minute practice plan for my team, considering our age group and level."),
            (col2, "📋 BEAT ZONE\n\nAttack 2-3 zone defense", "How should we attack a 2-3 zone defense? Give me specific actions and player movements."),
            (col3, "💪 SHOOTING FORM\n\nTeach correct mechanics", "How do I teach correct shooting mechanics to my players? Break it down step by step."),
            (col4, "👶 FUN DRILLS\n\nGames for kids 6-10", "Give me fun and engaging basketball games and drills for kids ages 6-10."),
            (col5, "📊 GAME ANALYSIS\n\nAnalyze team stats", "I want to analyze my team's performance. What statistics should I provide you?"),
        ]
        
        for col, label, prompt in quick_plays:
            with col:
                if st.button(label, use_container_width=True):
                    st.session_state.pending_prompt = prompt


def render_file_upload():
    """Render file upload section"""
    if not st.session_state.get('show_file_upload', False):
        return
    
    st.markdown('''
    <div style="background: rgba(30,30,30,0.95); border: 2px solid #FF6B35; border-radius: 15px; padding: 1.5rem; margin: 1rem 0;">
        <div style="font-family:'Orbitron',monospace; color:#FF6B35; font-size:1.1rem; margin-bottom:0.5rem;">📁 UPLOAD FILE FOR ANALYSIS</div>
        <div style="color:#FFFFFF; font-size:0.9rem;">Supported formats: <span style="color:#FF6B35;">CSV, Excel, TXT, or Image (Screenshot)</span></div>
    </div>
    ''', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Drop your file here or click to browse", type=ALLOWED_FILE_TYPES, key="stats_file_chat", label_visibility="visible")
    analysis_type = st.selectbox("What do you want to analyze?", ANALYSIS_TYPES, key="analysis_type_chat")
    
    col_analyze, col_cancel = st.columns(2)
    
    if uploaded_file is not None:
        st.success(f"✅ File loaded: {uploaded_file.name}")
        with col_analyze:
            if st.button("🔍 ANALYZE NOW", key="analyze_btn_chat", use_container_width=True):
                try:
                    file_result = read_uploaded_file(uploaded_file)
                    if file_result["type"] == "image":
                        st.session_state.pending_image = {"data": file_result["data"], "mime_type": file_result["mime_type"]}
                    st.session_state.pending_prompt = build_analysis_prompt(file_result, analysis_type)
                    st.session_state.show_file_upload = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error reading file: {e}")
    
    with col_cancel:
        if st.button("❌ Cancel", key="cancel_upload_chat", use_container_width=True):
            st.session_state.show_file_upload = False
            st.rerun()


def render_chat(client, supabase):
    """Render chat interface"""
    coach = st.session_state.get('coach', {})
    
    # File upload section
    render_file_upload()
    
    # Upload button
    if not st.session_state.get('show_file_upload', False):
        if st.button("📁 Upload Stats File for Analysis", key="upload_stats_btn"):
            st.session_state.show_file_upload = True
            st.rerun()
    
    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])
        else:
            agent = get_agent_from_value(msg.get("agent", Agent.ASSISTANT_COACH))
            with st.chat_message("assistant", avatar=AGENT_INFO[agent]["icon"]):
                st.markdown(msg["content"], unsafe_allow_html=True)
    
    # Handle input
    prompt = st.session_state.pop("pending_prompt", None)
    if not prompt:
        prompt = st.chat_input("Ask your coaching question... | שאל את שאלתך...")
    
    if prompt:
        # Create conversation if needed
        if not st.session_state.get('current_conversation'):
            conv = create_conversation(supabase, coach.get('id'), prompt[:50])
            st.session_state.current_conversation = conv
        
        # Show user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Save user message
        if st.session_state.current_conversation:
            save_message(supabase, st.session_state.current_conversation['id'], "user", prompt)
        
        # Route question
        with st.spinner("🏀 Analyzing..."):
            agent = route_question(prompt, client, st.session_state.messages[:-1])
        
        # Check for pending image
        image_data = st.session_state.pop("pending_image", None)
        
        # Get response
        info = AGENT_INFO[agent]
        with st.chat_message("assistant", avatar=info["icon"]):
            with st.spinner(f"Consulting {info['name']}..."):
                raw_response = get_agent_response(
                    prompt, agent, st.session_state.messages[:-1],
                    client, coach, supabase, image_data
                )
                formatted = format_response(raw_response, agent)
            st.markdown(formatted, unsafe_allow_html=True)
        
        # Save response
        if st.session_state.current_conversation:
            save_message(supabase, st.session_state.current_conversation['id'], "assistant", formatted, agent.value)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": formatted,
            "raw_content": raw_response,
            "agent": agent.value
        })
        st.rerun()


def render_mobile_nav(supabase):
    """Render mobile navigation buttons"""
    coach = st.session_state.get('coach', {})
    
    st.markdown('<style>@media (min-width: 768px) { .mobile-nav-section { display: none !important; } }</style><div class="mobile-nav-section">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ NEW", key="mobile_new_btn", use_container_width=True):
            st.session_state.current_conversation = None
            st.session_state.messages = []
            st.session_state.show_mobile_history = False
            st.rerun()
    
    with col2:
        if st.button("📜 HISTORY", key="mobile_history_btn", use_container_width=True):
            st.session_state.show_mobile_history = not st.session_state.get('show_mobile_history', False)
            st.rerun()
    
    with col3:
        if st.button("🚪 LOGOUT", key="mobile_logout_btn", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.coach = None
            st.session_state.messages = []
            st.session_state.current_conversation = None
            st.session_state.show_mobile_history = False
            st.rerun()
    
    # Mobile history panel
    if st.session_state.get('show_mobile_history', False):
        st.markdown('<div style="background: rgba(20,20,20,0.95); border: 2px solid #FF6B35; border-radius: 15px; padding: 1rem; margin: 0.5rem 0;"><div style="font-family:\'Orbitron\',monospace; color:#FF6B35; font-size:1rem; margin-bottom:0.5rem; text-align:center;">📜 CHAT HISTORY</div></div>', unsafe_allow_html=True)
        
        conversations = get_coach_conversations(supabase, coach.get('id'))
        
        if not conversations:
            st.markdown('<div style="text-align:center; color:#888; padding:0.5rem;">No previous conversations</div>', unsafe_allow_html=True)
        else:
            for conv in conversations[:10]:
                title = conv.get('title', 'Untitled')[:35]
                if len(conv.get('title', '')) > 35:
                    title += "..."
                if st.button(f"💬 {title}", key=f"mob_conv_{conv['id']}", use_container_width=True):
                    st.session_state.current_conversation = conv
                    messages = get_conversation_messages(supabase, conv['id'])
                    st.session_state.messages = [
                        {
                            "role": msg['role'],
                            "content": msg['content'],
                            "raw_content": msg['content'],
                            "agent": msg.get('agent', 'assistant_coach')
                        }
                        for msg in messages
                    ]
                    st.session_state.show_mobile_history = False
                    st.rerun()
        
        if st.button("❌ CLOSE", key="close_mob_history", use_container_width=True):
            st.session_state.show_mobile_history = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def main():
    """Main application entry point"""
    # Initialize session state
    defaults = {
        "logged_in": False,
        "messages": [],
        "current_conversation": None,
        "show_mobile_history": False,
        "show_file_upload": False,
        "current_page": "chat"
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Initialize clients
    supabase = get_supabase_client()
    openai_client = get_openai_client()
    
    if not supabase:
        st.error("⚠️ Database connection failed. Check SUPABASE_URL and SUPABASE_KEY in secrets.")
        st.stop()
    
    if not openai_client:
        st.error("⚠️ OpenAI connection failed. Check OPENAI_API_KEY in secrets.")
        st.stop()
    
    # Render app
    if not st.session_state.logged_in:
        render_login_page(supabase)
    else:
        st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
        render_sidebar(supabase)
        render_mobile_nav(supabase)
        render_header()
        
        # Page routing
        if st.session_state.current_page == 'logistics':
            coach = st.session_state.get('coach', {})
            render_logistics_page(supabase, coach.get('id'))
        else:
            render_welcome()
            render_chat(openai_client, supabase)


if __name__ == "__main__":
    main()
