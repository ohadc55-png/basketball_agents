# -*- coding: utf-8 -*-
"""
HOOPS AI - Timeline Component
Visual timeline for practice sessions
"""

import streamlit as st
from config import SEGMENT_COLORS

def render_segment(segment, index, total_segments, on_move_up=None, on_move_down=None, on_delete=None):
    """
    Render a single timeline segment
    
    Args:
        segment: Dict with segment data
        index: Position in timeline
        total_segments: Total number of segments
        on_move_up: Callback for moving segment up
        on_move_down: Callback for moving segment down
        on_delete: Callback for deleting segment
    """
    
    seg_type = segment.get('segment_type', 'drill')
    title = segment.get('title', 'Activity')
    duration = segment.get('duration_minutes', 10)
    notes = segment.get('notes', '')
    
    # Get color for segment type
    color = SEGMENT_COLORS.get(seg_type, '#f48c25')
    
    # Type icons
    type_icons = {
        'warmup': '🔥',
        'drill': '🏀',
        'scrimmage': '⚔️',
        'cooldown': '❄️',
        'break': '☕',
        'film': '🎬'
    }
    icon = type_icons.get(seg_type, '📋')
    
    # Calculate time position (approximate)
    # This would need actual start times in a real implementation
    
    col1, col2, col3 = st.columns([6, 1, 1])
    
    with col1:
        st.markdown(f'''
        <div class="timeline-segment {seg_type}">
            <span class="segment-time">{icon}</span>
            <span class="segment-title">{title}</span>
            <span class="segment-duration">{duration} min</span>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        # Move buttons
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if index > 0 and on_move_up:
                if st.button("⬆️", key=f"up_{segment['id']}", help="Move up"):
                    on_move_up(segment, index)
        with btn_col2:
            if index < total_segments - 1 and on_move_down:
                if st.button("⬇️", key=f"down_{segment['id']}", help="Move down"):
                    on_move_down(segment, index)
    
    with col3:
        if on_delete:
            if st.button("🗑️", key=f"del_seg_{segment['id']}", help="Delete"):
                on_delete(segment)


def render_timeline(segments, on_move_up=None, on_move_down=None, on_delete=None):
    """
    Render the full practice timeline
    
    Args:
        segments: List of segment dicts
        on_move_up: Callback for moving segment up
        on_move_down: Callback for moving segment down
        on_delete: Callback for deleting segment
    """
    
    if not segments:
        st.markdown('''
        <div class="empty-state">
            <div class="empty-state-icon">📋</div>
            <div class="empty-state-text">No activities yet</div>
            <div style="color: #888; font-size: 0.9rem;">Add drills or activities to build your practice plan</div>
        </div>
        ''', unsafe_allow_html=True)
        return
    
    # Calculate total time
    total_time = sum(s.get('duration_minutes', 0) for s in segments)
    
    # Header with stats
    st.markdown(f'''
    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem; padding: 0 0.5rem;">
        <span style="color: #f48c25; font-family: 'Space Grotesk', sans-serif;">
            📋 {len(segments)} Activities
        </span>
        <span style="color: #00FF87; font-family: 'Space Grotesk', sans-serif;">
            ⏱️ Total: {total_time} min
        </span>
    </div>
    ''', unsafe_allow_html=True)
    
    # Visual timeline bar
    if segments:
        timeline_bar = '<div style="display: flex; height: 8px; border-radius: 4px; overflow: hidden; margin-bottom: 1rem;">'
        for seg in segments:
            seg_type = seg.get('segment_type', 'drill')
            duration = seg.get('duration_minutes', 10)
            width_percent = (duration / total_time * 100) if total_time > 0 else 0
            color = SEGMENT_COLORS.get(seg_type, '#f48c25')
            timeline_bar += f'<div style="width: {width_percent}%; background: {color};" title="{seg.get("title", "")} - {duration}min"></div>'
        timeline_bar += '</div>'
        st.markdown(timeline_bar, unsafe_allow_html=True)
    
    # Render each segment
    for i, segment in enumerate(segments):
        render_segment(segment, i, len(segments), on_move_up, on_move_down, on_delete)


def render_timeline_summary(segments):
    """Render a compact summary of the timeline"""
    
    if not segments:
        return
    
    total_time = sum(s.get('duration_minutes', 0) for s in segments)
    
    # Count by type
    type_counts = {}
    for seg in segments:
        t = seg.get('segment_type', 'drill')
        type_counts[t] = type_counts.get(t, 0) + 1
    
    summary_parts = []
    type_icons = {'warmup': '🔥', 'drill': '🏀', 'scrimmage': '⚔️', 'cooldown': '❄️', 'break': '☕', 'film': '🎬'}
    
    for t, count in type_counts.items():
        icon = type_icons.get(t, '📋')
        summary_parts.append(f"{icon} {count}")
    
    summary = " | ".join(summary_parts)
    
    st.markdown(f'''
    <div style="background: rgba(20,20,20,0.8); border-radius: 10px; padding: 0.75rem 1rem; margin: 0.5rem 0;">
        <span style="color: #888; font-size: 0.8rem;">{summary}</span>
        <span style="color: #00FF87; font-size: 0.8rem; float: right;">⏱️ {total_time} min</span>
    </div>
    ''', unsafe_allow_html=True)
