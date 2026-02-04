# -*- coding: utf-8 -*-
"""
HOOPS AI - Practice Planner Page
Create and manage practice sessions with visual timeline
"""

import streamlit as st
from datetime import date, datetime, timedelta
from config import SEGMENT_TYPES, SEGMENT_COLORS, DRILL_CATEGORIES, Agent
from utils import (
    get_practice_sessions, get_session_by_id, create_practice_session,
    update_practice_session, delete_practice_session,
    get_session_segments, create_segment, update_segment, delete_segment,
    get_drills, get_agent_response
)
from components.timeline import render_timeline, render_timeline_summary
from components.drill_card import render_drill_card_mini

def render_practice_planner_page(supabase, coach, openai_client):
    """Render the Practice Planner page"""
    
    # Initialize session state
    if 'selected_session' not in st.session_state:
        st.session_state.selected_session = None
    if 'show_session_form' not in st.session_state:
        st.session_state.show_session_form = False
    
    # Page header
    st.markdown('''
    <div class="page-header">
        <div class="page-title">📋 Practice Planner</div>
        <div class="page-subtitle">Design and organize your practice sessions</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Two column layout: Sessions list | Session editor
    col_list, col_editor = st.columns([1, 2])
    
    with col_list:
        st.markdown("### 📅 Sessions")
        
        if st.button("➕ New Session", use_container_width=True, type="primary"):
            st.session_state.show_session_form = True
            st.session_state.selected_session = None
        
        st.markdown("---")
        
        # Get sessions
        sessions = get_practice_sessions(supabase, coach['id'])
        
        if sessions:
            for session in sessions[:10]:  # Show last 10
                session_date = session.get('date', '')
                if session_date:
                    try:
                        date_obj = datetime.strptime(session_date, '%Y-%m-%d')
                        date_display = date_obj.strftime('%b %d')
                    except:
                        date_display = session_date
                else:
                    date_display = "No date"
                
                is_selected = st.session_state.selected_session and st.session_state.selected_session.get('id') == session.get('id')
                
                btn_type = "primary" if is_selected else "secondary"
                
                if st.button(
                    f"📋 {session.get('title', 'Untitled')[:20]}\n{date_display}",
                    key=f"sess_{session['id']}",
                    use_container_width=True,
                    type=btn_type
                ):
                    st.session_state.selected_session = session
                    st.session_state.show_session_form = False
                    st.rerun()
        else:
            st.markdown('''
            <div style="text-align: center; color: #666; padding: 2rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📋</div>
                <div>No sessions yet</div>
            </div>
            ''', unsafe_allow_html=True)
    
    with col_editor:
        # Show session form if creating new
        if st.session_state.show_session_form:
            render_session_form(supabase, coach)
        
        # Show session editor if session selected
        elif st.session_state.selected_session:
            render_session_editor(supabase, coach, openai_client)
        
        else:
            st.markdown('''
            <div class="empty-state">
                <div class="empty-state-icon">📋</div>
                <div class="empty-state-text">Select a session or create a new one</div>
                <div style="color: #888;">Your practice timeline will appear here</div>
            </div>
            ''', unsafe_allow_html=True)


def render_session_form(supabase, coach):
    """Render form for creating/editing a session"""
    
    st.markdown("### ➕ Create New Session")
    
    with st.form("session_form"):
        title = st.text_input("Session Title *", placeholder="e.g., Tuesday Practice - Defense Focus")
        
        col1, col2 = st.columns(2)
        with col1:
            session_date = st.date_input("Date", value=date.today())
        with col2:
            duration = st.number_input("Planned Duration (min)", min_value=30, max_value=180, value=90)
        
        notes = st.text_area("Notes", placeholder="Any notes about this session...", height=80)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.form_submit_button("💾 Create Session", use_container_width=True, type="primary"):
                if title:
                    session = create_practice_session(supabase, coach['id'], title, session_date, duration, notes)
                    if session:
                        st.session_state.selected_session = session
                        st.session_state.show_session_form = False
                        st.success("✅ Session created!")
                        st.rerun()
                else:
                    st.error("Please enter a title")
        
        with col_btn2:
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                st.session_state.show_session_form = False
                st.rerun()


def render_session_editor(supabase, coach, openai_client):
    """Render the session editor with timeline"""
    
    session = st.session_state.selected_session
    
    # Session header
    col_h1, col_h2, col_h3 = st.columns([4, 1, 1])
    
    with col_h1:
        st.markdown(f"### 📋 {session.get('title', 'Session')}")
        
        session_date = session.get('date', '')
        if session_date:
            st.caption(f"📅 {session_date}")
    
    with col_h2:
        if st.button("🤖 Auto-Fill", use_container_width=True, help="Let AI suggest a practice plan"):
            auto_fill_session(supabase, coach, openai_client, session)
    
    with col_h3:
        if st.button("🗑️ Delete", use_container_width=True):
            if delete_practice_session(supabase, session['id']):
                st.session_state.selected_session = None
                st.rerun()
    
    st.markdown("---")
    
    # Get segments
    segments = get_session_segments(supabase, session['id'])
    
    # Timeline visualization
    st.markdown("#### ⏱️ Practice Timeline")
    
    render_timeline(
        segments,
        on_move_up=lambda s, i: move_segment(supabase, session['id'], segments, i, -1),
        on_move_down=lambda s, i: move_segment(supabase, session['id'], segments, i, 1),
        on_delete=lambda s: delete_and_refresh(supabase, s)
    )
    
    st.markdown("---")
    
    # Add segment section
    st.markdown("#### ➕ Add Activity")
    
    tab_manual, tab_drill = st.tabs(["📝 Manual Entry", "🏀 From Library"])
    
    with tab_manual:
        render_add_segment_form(supabase, session, segments)
    
    with tab_drill:
        render_add_drill_form(supabase, coach, session, segments)


def render_add_segment_form(supabase, session, segments):
    """Render form to add a custom segment"""
    
    with st.form("add_segment"):
        col1, col2 = st.columns(2)
        
        with col1:
            seg_type = st.selectbox(
                "Activity Type",
                options=[s[0] for s in SEGMENT_TYPES],
                format_func=lambda x: dict(SEGMENT_TYPES).get(x, x)
            )
        
        with col2:
            duration = st.number_input("Duration (min)", min_value=1, max_value=60, value=10)
        
        title = st.text_input("Activity Name", placeholder="e.g., Dynamic stretching, 3-man weave...")
        
        notes = st.text_input("Notes (optional)", placeholder="Any specific instructions...")
        
        if st.form_submit_button("➕ Add to Timeline", use_container_width=True, type="primary"):
            if title:
                next_order = len(segments)
                create_segment(supabase, session['id'], next_order, seg_type, title, duration, None, notes)
                st.success(f"✅ Added: {title}")
                st.rerun()
            else:
                st.error("Please enter an activity name")


def render_add_drill_form(supabase, coach, session, segments):
    """Render form to add a drill from library"""
    
    # Get drills from library
    drills = get_drills(supabase, coach['id'])
    
    if not drills:
        st.info("📚 No drills in your library yet. Create some drills first!")
        if st.button("Go to Drill Library"):
            st.session_state.current_page = 'library'
            st.rerun()
        return
    
    # Filter
    category_filter = st.selectbox(
        "Filter by category",
        options=["all"] + [c[0] for c in DRILL_CATEGORIES],
        format_func=lambda x: "All Categories" if x == "all" else dict(DRILL_CATEGORIES).get(x, x)
    )
    
    filtered_drills = drills if category_filter == "all" else [d for d in drills if d.get('category') == category_filter]
    
    st.markdown("##### Available Drills:")
    
    for drill in filtered_drills[:6]:  # Show first 6
        col1, col2 = st.columns([4, 1])
        
        with col1:
            render_drill_card_mini(drill)
        
        with col2:
            if st.button("➕", key=f"add_drill_{drill['id']}", help="Add to session"):
                next_order = len(segments)
                create_segment(
                    supabase, session['id'], next_order, 'drill',
                    drill.get('title', 'Drill'),
                    drill.get('duration_minutes', 10),
                    drill['id'],
                    None
                )
                st.success(f"✅ Added: {drill.get('title')}")
                st.rerun()


def move_segment(supabase, session_id, segments, current_index, direction):
    """Move a segment up or down"""
    new_index = current_index + direction
    
    if 0 <= new_index < len(segments):
        # Swap orders
        seg1 = segments[current_index]
        seg2 = segments[new_index]
        
        update_segment(supabase, seg1['id'], {'segment_order': new_index})
        update_segment(supabase, seg2['id'], {'segment_order': current_index})
        
        st.rerun()


def delete_and_refresh(supabase, segment):
    """Delete segment and refresh"""
    delete_segment(supabase, segment['id'])
    st.rerun()


def auto_fill_session(supabase, coach, openai_client, session):
    """Use AI to suggest a practice plan"""
    
    with st.spinner("🤖 AI is creating your practice plan..."):
        prompt = f"""Create a practice plan for a {session.get('total_duration', 90)} minute basketball practice.

Team info:
- Age group: {coach.get('age_group', 'Senior')}
- Level: {coach.get('level', 'Competitive')}
- Session title: {session.get('title', 'Practice')}

Please suggest a structured practice with:
1. Warmup (5-10 min)
2. Skill work drills (15-20 min)
3. Team drills/plays (20-30 min)
4. Scrimmage/game situations (15-20 min)
5. Cooldown (5 min)

For each segment provide:
- Type (warmup/drill/scrimmage/cooldown)
- Name
- Duration in minutes
- Brief description

Format as a list with each segment on a new line:
TYPE | NAME | DURATION | DESCRIPTION"""

        response = get_agent_response(
            prompt,
            Agent.ASSISTANT_COACH,
            [],
            openai_client,
            coach,
            supabase
        )
        
        # Parse and create segments
        parse_and_create_segments(supabase, session['id'], response)
        st.success("✅ Practice plan created!")
        st.rerun()


def parse_and_create_segments(supabase, session_id, response):
    """Parse AI response and create segments"""
    
    # Clear existing segments first
    existing = get_session_segments(supabase, session_id)
    for seg in existing:
        delete_segment(supabase, seg['id'])
    
    lines = response.split('\n')
    order = 0
    
    type_mapping = {
        'warmup': 'warmup', 'warm-up': 'warmup', 'warm up': 'warmup',
        'drill': 'drill', 'drills': 'drill', 'skill': 'drill',
        'scrimmage': 'scrimmage', 'game': 'scrimmage', 'play': 'scrimmage',
        'cooldown': 'cooldown', 'cool-down': 'cooldown', 'cool down': 'cooldown',
        'break': 'break', 'rest': 'break'
    }
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Try to parse "TYPE | NAME | DURATION | DESC" format
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                seg_type_raw = parts[0].lower()
                seg_type = 'drill'  # default
                for key, val in type_mapping.items():
                    if key in seg_type_raw:
                        seg_type = val
                        break
                
                title = parts[1]
                
                try:
                    duration = int(''.join(filter(str.isdigit, parts[2])) or '10')
                except:
                    duration = 10
                
                notes = parts[3] if len(parts) > 3 else None
                
                create_segment(supabase, session_id, order, seg_type, title, duration, None, notes)
                order += 1
