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
    """Render clean sidebar"""
    coach = st.session_state.get('coach', {})
    
    with st.sidebar:
        # ========== LOGO ==========
        st.image("https://i.postimg.cc/g2QPCwqj/עיצוב_ללא_שם.png", width=180)
        
        # ========== PROFILE ==========
        st.caption(f"**{coach.get('name', 'Coach')}**")
        st.caption(f"{coach.get('team_name', '')} | {coach.get('age_group', '')} | {coach.get('level', '')}")
        
        st.divider()
        
        # ========== NAVIGATION ==========
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💬 CHAT", use_container_width=True, key="nav_chat",
                        type="primary" if st.session_state.current_page == 'chat' else "secondary"):
                st.session_state.current_page = 'chat'
                st.rerun()
        with col2:
            if st.button("📋 MGR", use_container_width=True, key="nav_logistics",
                        type="primary" if st.session_state.current_page == 'logistics' else "secondary"):
                st.session_state.current_page = 'logistics'
                st.rerun()
        
        # ========== CHAT PAGE CONTENT ==========
        if st.session_state.current_page == 'chat':
            
            # New Chat
            if st.button("➕ NEW CHAT", use_container_width=True, key="new_chat_btn"):
                st.session_state.current_conversation = None
                st.session_state.messages = []
                st.rerun()
            
            st.divider()
            
            # ========== QUICK IDEAS ==========
            qi_options = {
                "💡 Quick Ideas...": [],
                "🏀 Offense": [
                    ("Motion offense", "Explain motion offense basics and give me 3 simple actions."),
                    ("Pick & Roll", "Show me different pick and roll variations."),
                    ("Beat zone", "How to attack a 2-3 zone defense?"),
                ],
                "🛡️ Defense": [
                    ("Man-to-man", "Key principles of man-to-man defense."),
                    ("Zone setup", "How to set up a 2-3 zone defense?"),
                    ("Press break", "How to break full-court press?"),
                ],
                "💪 Fitness": [
                    ("Warmup routine", "Create a 15-minute pre-game warmup."),
                    ("Strength program", "Weekly strength program for players."),
                ],
                "🧠 Mental": [
                    ("Team talk", "Help me structure a pre-game team talk."),
                    ("Build confidence", "How to build player confidence?"),
                ],
                "📊 Analytics": [
                    ("Player stats", "What statistics should I track?"),
                    ("Team review", "Help with team performance review."),
                ],
                "👶 Youth": [
                    ("Fun drills", "Fun drills for kids ages 6-10."),
                    ("Fundamentals", "Teaching fundamentals to young kids."),
                ],
                "🍎 Nutrition": [
                    ("Meal plan", "Create a nutrition plan for my player."),
                    ("Game day food", "What to eat before/after games?"),
                ],
            }
            
            selected = st.selectbox("Quick Ideas", list(qi_options.keys()), 
                                   key="qi_select", label_visibility="collapsed")
            
            if selected != "💡 Quick Ideas...":
                for label, prompt in qi_options[selected]:
                    if st.button(f"▸ {label}", key=f"qi_{label}", use_container_width=True):
                        st.session_state.pending_prompt = prompt
                        st.rerun()
            
            st.divider()
            
            # ========== CHAT HISTORY (3 only) ==========
            st.caption("📜 Recent Chats")
            conversations = get_coach_conversations(supabase, coach.get('id'))
            if conversations:
                for conv in conversations[:3]:
                    title = conv.get('title', 'Chat')[:22] + "..." if len(conv.get('title', '')) > 22 else conv.get('title', 'Chat')
                    if st.button(f"💬 {title}", key=f"conv_{conv['id']}", use_container_width=True):
                        st.session_state.current_conversation = conv
                        msgs = get_conversation_messages(supabase, conv['id'])
                        st.session_state.messages = [
                            {"role": m['role'], "content": m['content'],
                             "raw_content": m['content'].split('\n\n', 1)[-1] if '\n\n' in m['content'] else m['content'],
                             "agent": m.get('agent')}
                            for m in msgs
                        ]
                        st.rerun()
            else:
                st.caption("No chats yet")
            
            st.divider()
            
            # ========== COACHING STAFF ==========
            st.caption("👥 Coaching Staff")
            
            staff_data = [
                ("🎯", "Assistant Coach", "Strategy", "#FF6B35"),
                ("📋", "Team Manager", "Logistics", "#9B59B6"),
                ("📋", "Tactician", "X's & O's", "#00D4FF"),
                ("💪", "Skills Coach", "Drills", "#00FF87"),
                ("🥗", "Nutritionist", "Diet", "#FFD700"),
                ("🏋️", "Strength Coach", "Fitness", "#FF4500"),
                ("📊", "Analyst", "Stats", "#9370DB"),
                ("👶", "Youth Coach", "Kids", "#FF69B4"),
            ]
            
            for icon, name, spec, color in staff_data:
                st.markdown(f'''<div style="display:flex; align-items:center; padding:4px 0; border-left:3px solid {color}; padding-left:8px; margin:2px 0;">
                    <span style="font-size:14px;">{icon}</span>
                    <span style="font-size:12px; color:#fff; margin-left:6px;">{name}</span>
                    <span style="font-size:10px; color:#888; margin-left:4px;">• {spec}</span>
                </div>''', unsafe_allow_html=True)
        
        st.divider()
        
        # ========== LOGOUT ==========
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.coach = None
            st.session_state.messages = []
            st.session_state.current_conversation = None
            st.rerun()
        
        st.caption("Powered by OpenAI")


def render_header():
    """Render compact header - only shown when no messages"""
    # Only show the big header when there are no messages (welcome state)
    if not st.session_state.messages:
        st.markdown('''
        <div class="scoreboard" style="padding: 1rem 0; margin-bottom: 0.5rem;">
            <div class="hero-title" style="font-size: 2rem;">HOOPS AI</div>
            <div class="hero-subtitle" style="font-size: 0.9rem;">Your Personal Assistant Coach</div>
        </div>
        ''', unsafe_allow_html=True)


def render_welcome():
    """Render welcome banner - only when no messages"""
    if not st.session_state.messages:
        coach = st.session_state.get('coach', {})
        name = coach.get('name', '').split()[0] if coach.get('name') else ''
        
        st.markdown(f'''
        <div class="welcome-banner" style="padding: 1rem 1.5rem; margin-bottom: 1rem;">
            <div class="welcome-title" style="font-size: 1.3rem;">👋 Hey Coach {name}!</div>
            <div class="welcome-text" style="font-size: 0.9rem;">Your AI coaching staff is ready. Ask anything about basketball strategy, player development, or team management.</div>
            <div class="welcome-text" style="margin-top:0.5rem; font-size: 0.85rem;">Tailored for: <strong style="color:#FF6B35;">{coach.get("team_name", "")} | {coach.get("age_group", "")} | {coach.get("level", "")}</strong></div>
            <div class="welcome-text" style="margin-top:0.8rem; font-size:0.8rem; color:#888;">💡 <em>Check out Quick Ideas in the sidebar for instant prompts!</em></div>
        </div>
        ''', unsafe_allow_html=True)


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


def render_mobile_nav(supabase):
    """Mobile navigation - disabled since all buttons exist in sidebar"""
    # All navigation buttons (NEW, HISTORY, LOGOUT) are already in the sidebar
    # This function is kept empty to avoid duplicate buttons
    pass


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
            # Show compact title for logistics page
            st.markdown('<div style="text-align:center; padding:0.5rem;"><span style="font-family:Orbitron,monospace; color:#FF6B35; font-size:1.2rem;">📋 TEAM MANAGER</span></div>', unsafe_allow_html=True)
            coach = st.session_state.get('coach', {})
            render_logistics_page(supabase, coach.get('id'))
        else:
            # Chat page - header and welcome only when no messages
            render_header()  # Will only show if no messages
            render_welcome()  # Will only show if no messages
            render_mobile_nav(supabase)  # Mobile only
            render_chat(openai_client, supabase)


if __name__ == "__main__":
    main()