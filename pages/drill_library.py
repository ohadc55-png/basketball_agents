# -*- coding: utf-8 -*-
"""
HOOPS AI - Drill Library Page
Browse, create, and manage basketball drills
"""

import streamlit as st
from config import DRILL_CATEGORIES, DRILL_DIFFICULTIES, Agent, AGENT_INFO
from utils import (
    get_drills, create_drill, update_drill, delete_drill,
    get_agent_response
)
from components.drill_card import render_drill_card

def render_drill_library_page(supabase, coach, openai_client):
    """Render the Drill Library page"""

    # Page header with new design
    st.markdown('''
    <div class="page-header">
        <div class="page-title">📚 Drill Library</div>
        <div class="page-subtitle">Browse and manage your basketball drills</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Action bar
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search = st.text_input("🔍 Search drills...", placeholder="Search by name or description", label_visibility="collapsed")
    
    with col2:
        if st.button("➕ Create Drill", use_container_width=True, type="primary"):
            st.session_state.show_drill_form = True
            st.session_state.editing_drill = None
    
    with col3:
        if st.button("🤖 Generate with AI", use_container_width=True):
            st.session_state.show_ai_generator = True
    
    st.markdown("---")
    
    # Filters
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        category_options = [("all", "All Categories")] + DRILL_CATEGORIES
        selected_cat = st.selectbox(
            "Category",
            options=[c[0] for c in category_options],
            format_func=lambda x: dict(category_options)[x],
            label_visibility="collapsed"
        )
    
    with col_f2:
        diff_options = [("all", "All Levels")] + DRILL_DIFFICULTIES
        selected_diff = st.selectbox(
            "Difficulty",
            options=[d[0] for d in diff_options],
            format_func=lambda x: dict(diff_options)[x],
            label_visibility="collapsed"
        )
    
    # Get drills
    category_filter = selected_cat if selected_cat != "all" else None
    difficulty_filter = selected_diff if selected_diff != "all" else None
    
    drills = get_drills(supabase, coach['id'], category_filter, difficulty_filter, search)
    
    # Stats row
    total_drills = len(drills)
    ai_drills = len([d for d in drills if d.get('is_ai_generated')])
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-value">{total_drills}</div>
            <div class="stat-label">Total Drills</div>
        </div>
        ''', unsafe_allow_html=True)
    with stat_col2:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-value">{ai_drills}</div>
            <div class="stat-label">AI Generated</div>
        </div>
        ''', unsafe_allow_html=True)
    with stat_col3:
        categories_used = len(set(d.get('category') for d in drills if d.get('category')))
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-value">{categories_used}</div>
            <div class="stat-label">Categories</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display drills in grid
    if drills:
        # Create 3-column grid
        cols = st.columns(3)
        for i, drill in enumerate(drills):
            with cols[i % 3]:
                render_drill_card(
                    drill,
                    on_edit=lambda d: edit_drill(d),
                    on_delete=lambda d: confirm_delete_drill(d, supabase),
                    show_actions=True
                )
    else:
        st.markdown('''
        <div class="empty-state">
            <div class="empty-state-icon">📚</div>
            <div class="empty-state-text">No drills found</div>
            <div style="color: #888;">Create your first drill or generate one with AI!</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Drill form modal
    if st.session_state.get('show_drill_form', False):
        render_drill_form(supabase, coach)
    
    # AI Generator modal
    if st.session_state.get('show_ai_generator', False):
        render_ai_generator(supabase, coach, openai_client)


def render_drill_form(supabase, coach):
    """Render the drill creation/edit form"""
    
    editing = st.session_state.get('editing_drill')
    title = "✏️ Edit Drill" if editing else "➕ Create New Drill"
    
    with st.expander(title, expanded=True):
        with st.form("drill_form"):
            drill_title = st.text_input("Drill Name *", value=editing.get('title', '') if editing else '')
            
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox(
                    "Category *",
                    options=[c[0] for c in DRILL_CATEGORIES],
                    format_func=lambda x: dict(DRILL_CATEGORIES).get(x, x),
                    index=0 if not editing else [c[0] for c in DRILL_CATEGORIES].index(editing.get('category', 'offense'))
                )
            with col2:
                difficulty = st.selectbox(
                    "Difficulty *",
                    options=[d[0] for d in DRILL_DIFFICULTIES],
                    format_func=lambda x: dict(DRILL_DIFFICULTIES).get(x, x),
                    index=0 if not editing else [d[0] for d in DRILL_DIFFICULTIES].index(editing.get('difficulty', 'beginner'))
                )
            
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=60, value=editing.get('duration_minutes', 10) if editing else 10)
            
            description = st.text_area("Description", value=editing.get('description', '') if editing else '', height=100)
            
            instructions = st.text_area("Instructions", value=editing.get('instructions', '') if editing else '', height=150,
                                        help="Step by step instructions for running the drill")
            
            tags_input = st.text_input("Tags (comma separated)", value=', '.join(editing.get('tags', [])) if editing else '')
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submitted = st.form_submit_button("💾 Save Drill", use_container_width=True, type="primary")
            with col_btn2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.show_drill_form = False
                    st.session_state.editing_drill = None
                    st.rerun()
            
            if submitted and drill_title:
                tags = [t.strip() for t in tags_input.split(',') if t.strip()]
                
                if editing:
                    # Update existing drill
                    update_drill(supabase, editing['id'], {
                        'title': drill_title,
                        'category': category,
                        'difficulty': difficulty,
                        'duration_minutes': duration,
                        'description': description,
                        'instructions': instructions,
                        'tags': tags
                    })
                    st.success("✅ Drill updated!")
                else:
                    # Create new drill
                    create_drill(
                        supabase, coach['id'], drill_title, description, category,
                        duration, difficulty, instructions, [], tags, False
                    )
                    st.success("✅ Drill created!")
                
                st.session_state.show_drill_form = False
                st.session_state.editing_drill = None
                st.rerun()


def render_ai_generator(supabase, coach, openai_client):
    """Render AI drill generator"""
    
    with st.expander("🤖 AI Drill Generator", expanded=True):
        st.markdown("Describe what kind of drill you need and AI will create it for you!")
        
        with st.form("ai_generator"):
            prompt = st.text_area(
                "Describe the drill you want",
                placeholder="e.g., A shooting drill for beginners that focuses on form and can be done with 4-6 players...",
                height=100
            )
            
            col1, col2 = st.columns(2)
            with col1:
                ai_category = st.selectbox(
                    "Category",
                    options=[c[0] for c in DRILL_CATEGORIES],
                    format_func=lambda x: dict(DRILL_CATEGORIES).get(x, x)
                )
            with col2:
                ai_difficulty = st.selectbox(
                    "Difficulty",
                    options=[d[0] for d in DRILL_DIFFICULTIES],
                    format_func=lambda x: dict(DRILL_DIFFICULTIES).get(x, x)
                )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                generate = st.form_submit_button("🤖 Generate Drill", use_container_width=True, type="primary")
            with col_btn2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.show_ai_generator = False
                    st.rerun()
            
            if generate and prompt:
                with st.spinner("🤖 AI is creating your drill..."):
                    # Build the AI prompt
                    full_prompt = f"""Create a basketball drill with these requirements:
                    
{prompt}

Category: {ai_category}
Difficulty: {ai_difficulty}
Age group: {coach.get('age_group', 'Senior')}

Please provide:
1. A creative drill name
2. Brief description (2-3 sentences)
3. Duration in minutes
4. Step-by-step instructions
5. Key coaching points (3-5 bullets)

Format your response as:
NAME: [drill name]
DURATION: [minutes]
DESCRIPTION: [description]
INSTRUCTIONS: [step by step]
COACHING POINTS:
- [point 1]
- [point 2]
- [point 3]"""

                    # Use existing agent system
                    response = get_agent_response(
                        full_prompt,
                        Agent.SKILLS_COACH,
                        [],
                        openai_client,
                        coach,
                        supabase
                    )
                    
                    # Parse and save the drill
                    drill_data = parse_ai_drill_response(response, ai_category, ai_difficulty)
                    
                    if drill_data:
                        created = create_drill(
                            supabase, coach['id'],
                            drill_data['title'],
                            drill_data['description'],
                            ai_category,
                            drill_data['duration'],
                            ai_difficulty,
                            drill_data['instructions'],
                            drill_data['coaching_points'],
                            [],
                            True  # is_ai_generated
                        )
                        
                        if created:
                            st.success(f"✅ Created: {drill_data['title']}")
                            st.session_state.show_ai_generator = False
                            st.rerun()
                        else:
                            st.error("Failed to save drill")
                    else:
                        st.warning("Could not parse AI response. Here's what was generated:")
                        st.markdown(response)


def parse_ai_drill_response(response, category, difficulty):
    """Parse AI response into drill data"""
    try:
        lines = response.split('\n')
        
        drill_data = {
            'title': 'AI Generated Drill',
            'description': '',
            'duration': 10,
            'instructions': '',
            'coaching_points': []
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.upper().startswith('NAME:'):
                drill_data['title'] = line.split(':', 1)[1].strip()
            elif line.upper().startswith('DURATION:'):
                try:
                    duration_str = line.split(':', 1)[1].strip()
                    drill_data['duration'] = int(''.join(filter(str.isdigit, duration_str)) or '10')
                except:
                    pass
            elif line.upper().startswith('DESCRIPTION:'):
                drill_data['description'] = line.split(':', 1)[1].strip()
                current_section = 'description'
            elif line.upper().startswith('INSTRUCTIONS:'):
                drill_data['instructions'] = line.split(':', 1)[1].strip()
                current_section = 'instructions'
            elif line.upper().startswith('COACHING POINTS'):
                current_section = 'coaching_points'
            elif line.startswith('-') and current_section == 'coaching_points':
                drill_data['coaching_points'].append(line[1:].strip())
            elif current_section == 'instructions' and not line.upper().startswith(('NAME', 'DURATION', 'DESCRIPTION', 'COACHING')):
                drill_data['instructions'] += '\n' + line
            elif current_section == 'description' and not line.upper().startswith(('NAME', 'DURATION', 'INSTRUCTIONS', 'COACHING')):
                drill_data['description'] += ' ' + line
        
        return drill_data
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        return None


def edit_drill(drill):
    """Set up drill for editing"""
    st.session_state.editing_drill = drill
    st.session_state.show_drill_form = True
    st.rerun()


def confirm_delete_drill(drill, supabase):
    """Delete a drill"""
    if delete_drill(supabase, drill['id']):
        st.success(f"Deleted: {drill['title']}")
        st.rerun()
