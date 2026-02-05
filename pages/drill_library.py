# -*- coding: utf-8 -*-
"""
HOOPS AI - Play Creator Page
Visual basketball play designer with drag-and-drop court editor
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import os
from utils import get_plays, create_play, delete_play


def render_play_creator_page(supabase, coach):
    """Render the Play Creator page"""

    # Page header
    st.markdown('''
    <div class="page-header">
        <div class="page-title">🏀 Play Creator</div>
        <div class="page-subtitle">Design and animate basketball plays with visual editor</div>
    </div>
    ''', unsafe_allow_html=True)

    # Get saved plays from database
    saved_plays = get_plays(supabase, coach['id'])

    # Convert plays to format expected by the component
    plays_for_component = []
    for play in saved_plays:
        play_data = play.get('play_data', {})
        if play_data:
            plays_for_component.append({
                'id': play['id'],
                'name': play.get('title', 'Untitled'),
                'o': play_data.get('o', '5-out'),
                'd': play_data.get('d', 'none'),
                'i': play_data.get('i', []),
                'a': play_data.get('a', []),
                'b': play_data.get('b')
            })

    # Load the HTML file
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'play_creator.html')

    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Render the component
        components.html(html_content, height=900, scrolling=True)

    except FileNotFoundError:
        st.error("Play Creator component not found. Please ensure static/play_creator.html exists.")
        return

    st.markdown("---")

    # Saved plays management section
    st.markdown("### 💾 Saved Plays")

    if not saved_plays:
        st.info("No saved plays yet. Create a play using the editor above and click Save!")
    else:
        # Display saved plays in a grid
        cols = st.columns(3)
        for i, play in enumerate(saved_plays):
            with cols[i % 3]:
                play_data = play.get('play_data', {})
                offense_tpl = play_data.get('o', 'custom')
                defense_tpl = play_data.get('d', 'none')
                actions_count = len(play_data.get('a', []))

                st.markdown(f'''
                <div style="
                    background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
                    border-radius: 12px;
                    padding: 1rem;
                    margin-bottom: 1rem;
                    border: 1px solid #3d5a7f;
                ">
                    <div style="font-weight: bold; font-size: 1rem; margin-bottom: 0.5rem; color: #fff;">
                        🏀 {play.get('title', 'Untitled')}
                    </div>
                    <div style="font-size: 0.8rem; color: #aaa; margin-bottom: 0.5rem;">
                        Offense: {offense_tpl} | Defense: {defense_tpl}
                    </div>
                    <div style="font-size: 0.75rem; color: #888;">
                        {actions_count} actions
                    </div>
                </div>
                ''', unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("▶️ Load", key=f"load_{play['id']}", use_container_width=True):
                        st.session_state.load_play = play
                        st.rerun()
                with col2:
                    if st.button("🗑️", key=f"delete_{play['id']}", use_container_width=True):
                        if delete_play(supabase, play['id']):
                            st.success("Play deleted!")
                            st.rerun()

    # Save to Database Section
    st.markdown("### 💾 Save Play to Database")
    st.markdown("""
    <div style="background: #2d3748; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #f48c25;">
        <strong>How to save:</strong><br>
        1. Create your play in the editor above<br>
        2. Click <strong>Save</strong> button and enter a name<br>
        3. The play data will be copied to your clipboard<br>
        4. Paste it in the field below and click Save
    </div>
    """, unsafe_allow_html=True)

    with st.form("save_play_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            play_name = st.text_input("Play Name", placeholder="e.g., Horns Flare")
        with col2:
            play_data_json = st.text_area("Paste Play Data (JSON)", height=80, placeholder='Paste the copied JSON here...')

        submitted = st.form_submit_button("💾 Save to Database", use_container_width=True, type="primary")

        if submitted:
            if not play_data_json:
                st.error("Please paste the play data JSON from the editor above.")
            else:
                try:
                    play_data = json.loads(play_data_json)
                    # Use name from JSON if not provided
                    final_name = play_name.strip() if play_name.strip() else play_data.get('name', 'Untitled Play')
                    result = create_play(supabase, coach['id'], final_name, play_data)
                    if result:
                        st.success(f"✅ Play '{final_name}' saved successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to save play. Please check your database connection.")
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON format. Please copy the data again from the editor.")

    # Instructions
    with st.expander("📖 How to Use Play Creator"):
        st.markdown("""
        ### Getting Started
        1. **Select Template** - Choose an offensive formation (5-Out, Horns, Box, etc.) and optional defense
        2. **Position Players** - If using "Empty" template, drag players to starting positions
        3. **Pick Ball Carrier** - Select which player starts with the ball

        ### Drawing Actions
        - **Pass** ⤳ - Click player, drag to target location
        - **Dribble** 〰 - Player moves with the ball
        - **Cut** → - Player moves without ball
        - **Screen** ⊥ - Set a screen
        - **Handoff** ⇌ - Hand the ball to nearby player
        - **Shot** ◎ - Attempt a shot at the basket

        ### Advanced Features
        - **Parallel Mode** ⇉ - Make multiple players move simultaneously
        - **Curve Paths** 🎯 - Click on action lines and drag control point to curve
        - **Timeline** - Edit or delete specific steps

        ### Controls
        - **Undo** - Remove last action
        - **Clear** - Reset to initial positions
        - **Play** ▶️ - Watch the animation
        - **Save** 💾 - Save to your library
        - **Share** - Get a link to share the play
        """)


# Keep backward compatibility - alias for the old function name
def render_drill_library_page(supabase, coach, openai_client=None):
    """Backward compatible wrapper"""
    render_play_creator_page(supabase, coach)
