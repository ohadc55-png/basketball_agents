# -*- coding: utf-8 -*-
"""
HOOPS AI - Basketball Coaching Staff
Main Application File (Optimized)
"""

import streamlit as st
import re

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
from analytics_viz import display_analytics, extract_stats_from_text

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
        # Hello Coach banner
        st.markdown('''
        <div style="background: linear-gradient(135deg, rgba(255,107,53,0.2), rgba(255,107,53,0.1));
                    border: 2px solid #FF6B35; border-radius: 15px; padding: 1rem; 
                    text-align: center; margin-bottom: 1.5rem;">
            <span style="font-family: 'Orbitron', monospace; font-size: 1.5rem; 
                        color: #FF6B35; letter-spacing: 3px;">
                🏀 HELLO COACH 🏀
            </span>
        </div>
        ''', unsafe_allow_html=True)
        
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
    """Render sidebar with clean professional navigation"""
    coach = st.session_state.get('coach', {})
    
    with st.sidebar:
        # Logo - smaller and cleaner
        st.markdown(f'<div style="text-align:center; padding:0.5rem 0;"><img src="{LOGO_URL}" style="width:160px; border-radius:8px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
        # Profile - clean card style
        st.markdown('<div class="sidebar-section-title">Profile</div>', unsafe_allow_html=True)
        st.markdown(f'''
        <div class="profile-card">
            <div class="profile-name">{coach.get("name", "Coach")}</div>
            <div class="profile-team">{coach.get("team_name", "")} • {coach.get("age_group", "")} • {coach.get("level", "")}</div>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
        # Navigation
        st.markdown('<div class="sidebar-section-title">Navigation</div>', unsafe_allow_html=True)
        
        # Initialize current page
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'chat'
        
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("💬 Chat", use_container_width=True, key="nav_chat",
                        type="primary" if st.session_state.current_page == 'chat' else "secondary"):
                st.session_state.current_page = 'chat'
                st.rerun()
        with col_nav2:
            if st.button("📋 Manager", use_container_width=True, key="nav_logistics",
                        type="primary" if st.session_state.current_page == 'logistics' else "secondary"):
                st.session_state.current_page = 'logistics'
                st.rerun()
        
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
        # Only show chat-related items when on chat page
        if st.session_state.current_page == 'chat':
            # New Chat button
            if st.button("+ New Chat", use_container_width=True, key="new_chat_btn"):
                st.session_state.current_conversation = None
                st.session_state.messages = []
                st.rerun()
            
            # Upload Stats button
            if st.button("📊 Upload Stats", use_container_width=True, key="upload_stats_sidebar"):
                st.session_state.show_file_upload = True
                st.rerun()
            
            st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
            
            # ===== QUICK IDEAS SECTION =====
            st.markdown('<div class="sidebar-section-title">Quick Ideas</div>', unsafe_allow_html=True)
            
            # Category selector
            qi_categories = {
                "Select category...": [],
                "🏀 Offense": [
                    ("Motion offense basics", "Explain motion offense basics and give me 3 simple actions to start with."),
                    ("Pick & Roll variations", "Show me different pick and roll variations and when to use each one."),
                    ("Beat 2-3 zone", "How should we attack a 2-3 zone defense? Give me specific actions and player movements."),
                    ("End of game plays", "Give me 3 effective end-of-game plays for different situations (need 3, need 2, etc).")
                ],
                "🛡️ Defense": [
                    ("Man-to-man principles", "What are the key principles of man-to-man defense I should teach my team?"),
                    ("Zone defense setup", "How do I set up a 2-3 zone defense? Explain rotations and responsibilities."),
                    ("Press break strategies", "How do we break full-court press? Give me formation and movement options."),
                    ("Defending pick & roll", "What are the different ways to defend pick and roll? When should I use each?")
                ],
                "💪 Fitness": [
                    ("Pre-game warmup", "Create a 15-minute pre-game warmup routine for my team."),
                    ("Weekly strength program", "Design a weekly strength and conditioning program for basketball players."),
                    ("Injury prevention", "What exercises should we do to prevent common basketball injuries?"),
                    ("In-season conditioning", "How do I maintain fitness during the season without overtraining?")
                ],
                "🧠 Mental": [
                    ("Pre-game team talk", "Help me structure an effective pre-game team talk."),
                    ("Building confidence", "How do I build confidence in a player who is struggling?"),
                    ("Handling pressure", "How do I teach my players to perform better under pressure?"),
                    ("Team chemistry", "What activities and approaches help build team chemistry?")
                ],
                "📊 Analytics": [
                    ("Analyze player stats", "I want to analyze a player's performance. What statistics should I provide you?"),
                    ("Team performance review", "Help me do a team performance review. What data do you need from me?"),
                    ("Key metrics explained", "Explain the most important basketball analytics metrics I should track.")
                ],
                "👶 Youth (5-12)": [
                    ("Fun drills for kids", "Give me fun and engaging basketball games and drills for kids ages 6-10."),
                    ("Teaching fundamentals", "How do I teach basketball fundamentals to young kids in a fun way?"),
                    ("Age-appropriate plays", "What simple plays work best for youth basketball teams?")
                ],
                "🍎 Nutrition": [
                    ("Build meal plan", "I want to create a nutrition plan for my player. Please ask me the relevant questions to build a personalized meal plan."),
                    ("Game day nutrition", "What should players eat before, during, and after games?"),
                    ("Hydration guide", "Create a hydration guide for basketball players during practice and games.")
                ]
            }
            
            selected_category = st.selectbox(
                "Choose a topic:",
                options=list(qi_categories.keys()),
                key="qi_category_select",
                label_visibility="collapsed"
            )
            
            # Show buttons for selected category
            if selected_category and selected_category != "Select category...":
                prompts = qi_categories[selected_category]
                for i, (label, prompt) in enumerate(prompts):
                    if st.button(f"▸ {label}", key=f"qi_btn_{selected_category}_{i}", use_container_width=True):
                        st.session_state.pending_prompt = prompt
                        st.rerun()
            
            st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
            
            # Chat History
            st.markdown('<div class="sidebar-section-title">Chat History</div>', unsafe_allow_html=True)
            
            conversations = get_coach_conversations(supabase, coach.get('id'))
            if conversations:
                for conv in conversations[:8]:
                    title = conv.get('title', 'New Chat')[:25]
                    if len(conv.get('title', '')) > 25:
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
                st.markdown('<div style="color:var(--text-muted); font-size:0.75rem;">No conversations yet</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
            
            # Coaching Staff - Clean card style
            st.markdown('<div class="sidebar-section-title">Coaching Staff</div>', unsafe_allow_html=True)
            
            for agent in Agent:
                info = AGENT_INFO[agent]
                st.markdown(f'''
                <div class="agent-card">
                    <div style="display:flex; align-items:center; gap:0.4rem;">
                        <span style="font-size:1rem;">{info["icon"]}</span>
                        <div>
                            <div style="font-weight:500; color:var(--text-primary); font-size:0.75rem;">{info["name"]}</div>
                            <div style="color:var(--text-muted); font-size:0.6rem;">{info["specialty"]}</div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
        # Logout
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.coach = None
            st.session_state.messages = []
            st.session_state.current_conversation = None
            st.rerun()
        
        st.markdown('<div style="text-align:center; padding:0.5rem;"><div style="color:var(--text-muted); font-size:0.6rem;">Powered by OpenAI</div></div>', unsafe_allow_html=True)


def render_header():
    """Render clean header - only shown when no messages"""
    if not st.session_state.messages:
        st.markdown('''
        <div class="app-header">
            <div class="app-logo">HOOPS AI</div>
            <div class="app-tagline">Your Personal Assistant Coach</div>
        </div>
        ''', unsafe_allow_html=True)


def render_welcome():
    """Render welcome card - only when no messages"""
    if not st.session_state.messages:
        coach = st.session_state.get('coach', {})
        name = coach.get('name', '').split()[0] if coach.get('name') else ''
        
        st.markdown(f'''
        <div class="welcome-card">
            <div class="welcome-title">👋 Welcome back, {name}!</div>
            <div class="welcome-text">
                Your AI coaching staff is ready to help with strategy, training, and team management.
            </div>
            <div class="welcome-text" style="margin-top:0.5rem;">
                Team: <span class="welcome-highlight">{coach.get("team_name", "")} • {coach.get("age_group", "")} • {coach.get("level", "")}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def render_workspace():
    """Render the right-side workspace panel with tactical info and stats"""
    st.markdown('''
    <div class="workspace-panel">
        <div class="workspace-title">📊 Tactical Workspace</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Quick Stats Section
    st.markdown("**Quick Stats**")
    
    coach = st.session_state.get('coach', {})
    
    # Display some quick info cards
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Team", coach.get('team_name', 'N/A')[:10])
    with col2:
        st.metric("Level", coach.get('level', 'N/A')[:10])
    
    st.markdown("---")
    
    # Tactical Tips
    st.markdown("**💡 Quick Tips**")
    tips = [
        "🏀 Ask about pick & roll variations",
        "🛡️ Get zone defense strategies",
        "💪 Build a practice plan",
        "📊 Analyze player stats"
    ]
    for tip in tips:
        st.markdown(f"<div style='font-size:0.75rem; color:var(--text-secondary); padding:0.25rem 0;'>{tip}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent Activity (placeholder)
    st.markdown("**📜 Recent Topics**")
    if st.session_state.messages:
        # Show last 3 user messages
        user_msgs = [m for m in st.session_state.messages if m['role'] == 'user'][-3:]
        for msg in user_msgs:
            short_msg = msg['content'][:40] + "..." if len(msg['content']) > 40 else msg['content']
            st.markdown(f"<div style='font-size:0.7rem; color:var(--text-muted); padding:0.2rem 0; border-left:2px solid var(--accent-primary); padding-left:0.5rem;'>{short_msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size:0.75rem; color:var(--text-muted);'>Start a conversation to see topics here</div>", unsafe_allow_html=True)


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
    """Render clean chat interface - focused on conversation"""
    coach = st.session_state.get('coach', {})
    
    # File upload section (only if triggered from sidebar)
    render_file_upload()
    
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
        prompt = st.chat_input("Ask your coaching question...")
    
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
        
        # If ANALYST and user provided stats, show visualizations OUTSIDE chat message
        if agent == Agent.ANALYST:
            stats = extract_stats_from_text(prompt)
            # Check if there are numbers that look like stats
            numbers_in_prompt = re.findall(r'\b(\d+)\b', prompt)
            
            if stats:
                st.markdown("---")
                st.markdown("### 📊 Visual Analysis")
                display_analytics(prompt)
            elif len(numbers_in_prompt) >= 2:
                # Try to display even with fewer detected stats
                st.markdown("---")
                st.markdown("### 📊 Visual Analysis")
                display_analytics(prompt)
        
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
        
        # Page routing
        if st.session_state.current_page == 'logistics':
            st.markdown('<div style="text-align:center; padding:0.5rem;"><span style="color:var(--accent-primary); font-size:1rem; font-weight:600;">📋 Team Manager</span></div>', unsafe_allow_html=True)
            coach = st.session_state.get('coach', {})
            render_logistics_page(supabase, coach.get('id'))
        else:
            # Chat page - SPLIT SCREEN LAYOUT
            render_header()
            render_welcome()
            
            # Create two columns: Chat (60%) | Workspace (40%)
            chat_col, workspace_col = st.columns([3, 2])
            
            with chat_col:
                render_chat(openai_client, supabase)
            
            with workspace_col:
                render_workspace()


if __name__ == "__main__":
    main()