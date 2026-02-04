# -*- coding: utf-8 -*-
"""
HOOPS AI - Drill Card Component
Modern card design for displaying drills
"""

import streamlit as st

def render_drill_card(drill, on_add_to_session=None, on_edit=None, on_delete=None, show_actions=True):
    """
    Render a drill card with optional actions

    Args:
        drill: Dict with drill data
        on_add_to_session: Callback when "Add to Practice" is clicked
        on_edit: Callback when "Edit" is clicked
        on_delete: Callback when "Delete" is clicked
        show_actions: Whether to show action buttons
    """

    # Get drill data
    title = drill.get('title', 'Untitled Drill')
    description = drill.get('description', '')[:100]
    if len(drill.get('description', '')) > 100:
        description += '...'

    category = drill.get('category', 'general')
    difficulty = drill.get('difficulty', 'beginner')
    duration = drill.get('duration_minutes', 10)
    is_ai = drill.get('is_ai_generated', False)
    tags = drill.get('tags', [])

    # Category icons
    category_icons = {
        'offense': '🏀',
        'defense': '🛡️',
        'shooting': '🎯',
        'ball_handling': '⛹️',
        'passing': '🤝',
        'conditioning': '💪',
        'warmup': '🔥',
        'cooldown': '❄️'
    }
    cat_icon = category_icons.get(category, '🏀')

    # Difficulty labels
    diff_labels = {
        'beginner': 'Beginner',
        'intermediate': 'Intermediate',
        'advanced': 'Advanced'
    }
    diff_label = diff_labels.get(difficulty, difficulty.capitalize())
    diff_class = f"difficulty-{difficulty}"

    # Build the card HTML with modern design
    ai_badge = '<div class="ai-badge">AI</div>' if is_ai else ''

    tags_html = ''
    if tags:
        tags_html = ''.join([f'<span class="drill-tag">{tag}</span>' for tag in tags[:2]])

    card_html = f'''
    <div class="drill-card">
        {ai_badge}
        <div class="drill-card-title">{cat_icon} {title}</div>
        <div class="drill-card-desc">{description}</div>
        <div class="drill-card-meta">
            <span class="drill-tag {diff_class}">{diff_label}</span>
            <span class="drill-duration">⏱ {duration}m</span>
            {tags_html}
        </div>
    </div>
    '''

    st.markdown(card_html, unsafe_allow_html=True)
    
    # Action buttons
    if show_actions:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if on_add_to_session:
                if st.button("➕ Add to Practice", key=f"add_{drill['id']}", use_container_width=True):
                    on_add_to_session(drill)
        
        with col2:
            if on_edit:
                if st.button("✏️", key=f"edit_{drill['id']}", use_container_width=True):
                    on_edit(drill)
        
        with col3:
            if on_delete:
                if st.button("🗑️", key=f"del_{drill['id']}", use_container_width=True):
                    on_delete(drill)


def render_drill_card_mini(drill):
    """Render a compact version of the drill card"""

    title = drill.get('title', 'Untitled')[:28]
    duration = drill.get('duration_minutes', 10)
    category = drill.get('category', 'general')

    category_icons = {
        'offense': '🏀', 'defense': '🛡️', 'shooting': '🎯',
        'ball_handling': '⛹️', 'passing': '🤝', 'conditioning': '💪',
        'warmup': '🔥', 'cooldown': '❄️'
    }
    icon = category_icons.get(category, '🏀')

    st.markdown(f'''
    <div style="background: #221910; border-left: 3px solid #f48c25;
                padding: 0.6rem 0.85rem; border-radius: 8px; margin: 0.35rem 0;
                display: flex; justify-content: space-between; align-items: center;">
        <span style="color: #FFF; font-size: 0.85rem; font-family: 'Space Grotesk', sans-serif;">{icon} {title}</span>
        <span style="color: #7a6f63; font-size: 0.75rem;">⏱ {duration}m</span>
    </div>
    ''', unsafe_allow_html=True)
