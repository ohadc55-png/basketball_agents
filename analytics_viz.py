# -*- coding: utf-8 -*-
"""
HOOPS AI - Analytics Visualization Module
Charts and graphs for THE ANALYST
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import re
import json

# ============================================================================
# COLOR SCHEME (matches app theme)
# ============================================================================
COLORS = {
    'primary': '#FF6B35',
    'secondary': '#00D4FF',
    'success': '#00FF87',
    'warning': '#FFD700',
    'danger': '#FF4444',
    'background': '#1a1a1a',
    'text': '#FFFFFF',
    'grid': 'rgba(255, 107, 53, 0.1)'
}

CHART_TEMPLATE = {
    'layout': {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': COLORS['text'], 'family': 'Inter, sans-serif'},
        'title': {'font': {'size': 18, 'color': COLORS['primary']}},
        'xaxis': {'gridcolor': COLORS['grid'], 'linecolor': COLORS['grid']},
        'yaxis': {'gridcolor': COLORS['grid'], 'linecolor': COLORS['grid']},
        'legend': {'bgcolor': 'rgba(0,0,0,0.5)', 'bordercolor': COLORS['primary']}
    }
}


# ============================================================================
# DATA EXTRACTION FROM TEXT
# ============================================================================
def extract_stats_from_text(text):
    """Extract statistical data from user's text input"""
    stats = {}
    
    # Don't lowercase - Hebrew doesn't have case, and we want to preserve it
    text_search = text
    
    # Common patterns for basketball stats - improved for Hebrew and English
    patterns = {
        'points': r'(\d+)\s*(?:נקודות|נקודה|points?|pts?|נק)',
        'rebounds': r'(\d+)\s*(?:ריבאונדים|ריבאונד|rebounds?|rebs?|ריב)',
        'assists': r'(\d+)\s*(?:אסיסטים|אסיסט|assists?|ast)',
        'steals': r'(\d+)\s*(?:חטיפות|חטיפה|steals?|stl)',
        'blocks': r'(\d+)\s*(?:בלוקים|בלוק|blocks?|blk)',
        'turnovers': r'(\d+)\s*(?:טעויות|טעות|איבודים|איבוד|turnovers?|tov)',
        'minutes': r'(\d+)\s*(?:דקות|דקה|minutes?|mins?|דק)',
    }
    
    # Shooting patterns - X/Y format
    shooting_patterns = {
        'fg_made': r'(\d+)\s*[/\-]\s*(\d+)\s*(?:מהשדה|fg|field goals?|קליעות|מהמגרש|שדה)',
        'three_made': r'(\d+)\s*[/\-]\s*(\d+)\s*(?:משלש|משלושה|לשלש|3pt?|three|תלת)',
        'ft_made': r'(\d+)\s*[/\-]\s*(\d+)\s*(?:עונשין|חופשיות|ft|free throws?|זריקות)',
    }
    
    # Extract simple stats
    for stat_name, pattern in patterns.items():
        matches = re.findall(pattern, text_search, re.IGNORECASE | re.UNICODE)
        if matches:
            stats[stat_name] = int(matches[0])
    
    # Extract shooting stats (made/attempted)
    for stat_name, pattern in shooting_patterns.items():
        matches = re.findall(pattern, text_search, re.IGNORECASE | re.UNICODE)
        if matches:
            stats[stat_name] = {'made': int(matches[0][0]), 'attempted': int(matches[0][1])}
    
    # Fallback: if no specific patterns matched, look for any numbers with context
    if not stats:
        # Look for "X points" or "scored X" patterns
        points_match = re.search(r'(?:scored?|קלע|הבקיע)\s*(\d+)', text_search, re.IGNORECASE | re.UNICODE)
        if points_match:
            stats['points'] = int(points_match.group(1))
        
        # Look for standalone numbers if text mentions basketball stats
        basketball_keywords = ['game', 'משחק', 'stats', 'סטטיסטיקה', 'performance', 'ביצועים', 'שחקן', 'player']
        if any(word in text_search.lower() for word in basketball_keywords):
            numbers = re.findall(r'\b(\d+)\b', text_search)
            if len(numbers) >= 3:
                # Assume first few numbers are pts, reb, ast
                stats['points'] = int(numbers[0])
                if len(numbers) > 1:
                    stats['rebounds'] = int(numbers[1])
                if len(numbers) > 2:
                    stats['assists'] = int(numbers[2])
    
    return stats


def extract_player_comparison(text):
    """Extract data for player comparison from text"""
    # Look for patterns like "Player A: 20 pts, Player B: 15 pts"
    players = {}
    
    # Split by common delimiters
    parts = re.split(r'[,;]|\bvs\.?\b|\bנגד\b', text, flags=re.IGNORECASE)
    
    current_player = None
    for part in parts:
        # Check if this part contains a player name (usually followed by colon or stats)
        name_match = re.match(r'([א-ת\w\s]+?)[\s:]+(\d+)', part.strip())
        if name_match:
            player_name = name_match.group(1).strip()
            if player_name:
                current_player = player_name
                players[current_player] = extract_stats_from_text(part)
    
    return players


def extract_time_series(text):
    """Extract time series data (e.g., stats over multiple games)"""
    games = []
    
    # Look for game-by-game patterns
    game_patterns = re.findall(
        r'(?:משחק|game)\s*(\d+)[:\s]+(\d+)\s*(?:נקודות|pts?|points?)',
        text, re.IGNORECASE
    )
    
    for game_num, points in game_patterns:
        games.append({'game': int(game_num), 'points': int(points)})
    
    # Alternative: comma-separated values
    if not games:
        numbers = re.findall(r'\b(\d+)\b', text)
        if len(numbers) >= 3:
            games = [{'game': i+1, 'value': int(n)} for i, n in enumerate(numbers[:10])]
    
    return games


# ============================================================================
# CHART GENERATORS
# ============================================================================
def create_player_stats_bar(stats, player_name="Player"):
    """Create bar chart for single player stats"""
    
    # Prepare data
    categories = []
    values = []
    
    stat_labels = {
        'points': 'Points',
        'rebounds': 'Rebounds', 
        'assists': 'Assists',
        'steals': 'Steals',
        'blocks': 'Blocks',
        'turnovers': 'Turnovers',
        'minutes': 'Minutes'
    }
    
    for stat, label in stat_labels.items():
        if stat in stats and not isinstance(stats[stat], dict):
            categories.append(label)
            values.append(stats[stat])
    
    if not categories:
        return None
    
    # Create chart
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=COLORS['primary'],
            marker_line_color=COLORS['secondary'],
            marker_line_width=2,
            text=values,
            textposition='outside',
            textfont=dict(color=COLORS['text'], size=14, family='Inter')
        )
    ])
    
    fig.update_layout(
        title=f"📊 {player_name} - Game Stats",
        xaxis_title="",
        yaxis_title="",
        **CHART_TEMPLATE['layout'],
        height=400,
        showlegend=False
    )
    
    return fig


def create_shooting_chart(stats, player_name="Player"):
    """Create shooting percentages donut charts"""
    
    shooting_stats = []
    
    # Field Goals
    if 'fg_made' in stats:
        fg = stats['fg_made']
        shooting_stats.append({
            'name': 'Field Goals',
            'made': fg['made'],
            'missed': fg['attempted'] - fg['made'],
            'pct': round(fg['made'] / fg['attempted'] * 100, 1) if fg['attempted'] > 0 else 0
        })
    
    # Three Pointers
    if 'three_made' in stats:
        three = stats['three_made']
        shooting_stats.append({
            'name': '3-Pointers',
            'made': three['made'],
            'missed': three['attempted'] - three['made'],
            'pct': round(three['made'] / three['attempted'] * 100, 1) if three['attempted'] > 0 else 0
        })
    
    # Free Throws
    if 'ft_made' in stats:
        ft = stats['ft_made']
        shooting_stats.append({
            'name': 'Free Throws',
            'made': ft['made'],
            'missed': ft['attempted'] - ft['made'],
            'pct': round(ft['made'] / ft['attempted'] * 100, 1) if ft['attempted'] > 0 else 0
        })
    
    if not shooting_stats:
        return None
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=len(shooting_stats),
        specs=[[{'type': 'domain'}] * len(shooting_stats)],
        subplot_titles=[f"{s['name']}<br>{s['pct']}%" for s in shooting_stats]
    )
    
    for i, stat in enumerate(shooting_stats):
        fig.add_trace(
            go.Pie(
                values=[stat['made'], stat['missed']],
                labels=['Made', 'Missed'],
                marker_colors=[COLORS['success'], COLORS['danger']],
                hole=0.6,
                textinfo='value',
                textfont=dict(color=COLORS['text'], size=14),
                showlegend=(i == 0)
            ),
            row=1, col=i+1
        )
    
    fig.update_layout(
        title=f"🎯 {player_name} - Shooting Breakdown",
        **CHART_TEMPLATE['layout'],
        height=350,
        annotations=[dict(font_size=12, font_color=COLORS['text']) for _ in shooting_stats]
    )
    
    return fig


def create_player_comparison(players_data):
    """Create radar chart comparing multiple players"""
    
    if len(players_data) < 2:
        return None
    
    categories = ['Points', 'Rebounds', 'Assists', 'Steals', 'Blocks']
    stat_keys = ['points', 'rebounds', 'assists', 'steals', 'blocks']
    
    fig = go.Figure()
    
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['warning']]
    
    for i, (player_name, stats) in enumerate(players_data.items()):
        values = []
        for key in stat_keys:
            val = stats.get(key, 0)
            if isinstance(val, dict):
                val = val.get('made', 0)
            values.append(val)
        
        # Close the radar chart
        values.append(values[0])
        cats = categories + [categories[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=cats,
            fill='toself',
            fillcolor=f"rgba{tuple(int(colors[i % len(colors)].lstrip('#')[j:j+2], 16) for j in (0, 2, 4)) + (0.3,)}",
            line=dict(color=colors[i % len(colors)], width=2),
            name=player_name
        ))
    
    fig.update_layout(
        title="⚔️ Player Comparison",
        polar=dict(
            radialaxis=dict(
                visible=True,
                gridcolor=COLORS['grid'],
                linecolor=COLORS['grid']
            ),
            angularaxis=dict(
                gridcolor=COLORS['grid'],
                linecolor=COLORS['grid']
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        **CHART_TEMPLATE['layout'],
        height=450,
        showlegend=True
    )
    
    return fig


def create_trend_chart(games_data, metric_name="Points"):
    """Create line chart showing performance over time"""
    
    if not games_data or len(games_data) < 2:
        return None
    
    try:
        df = pd.DataFrame(games_data)
        
        if df.empty or len(df.columns) == 0:
            return None
        
        # Determine x and y columns
        if 'game' in df.columns:
            x_col = 'game'
        else:
            x_col = df.columns[0]
        
        # Find y column (first numeric column that's not x_col)
        y_col = None
        for col in df.columns:
            if col != x_col:
                y_col = col
                break
        
        if y_col is None:
            y_col = x_col  # Fallback
        
        # Ensure numeric values
        df[y_col] = pd.to_numeric(df[y_col], errors='coerce')
        df = df.dropna(subset=[y_col])
        
        if df.empty:
            return None
        
        # Calculate average
        avg = df[y_col].mean()
        
        fig = go.Figure()
        
        # Main line
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines+markers',
            name=metric_name,
            line=dict(color=COLORS['primary'], width=3),
            marker=dict(size=10, color=COLORS['primary'], line=dict(color=COLORS['text'], width=2))
        ))
        
        # Average line
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=[avg] * len(df),
            mode='lines',
            name=f'Average ({avg:.1f})',
            line=dict(color=COLORS['secondary'], width=2, dash='dash')
        ))
        
        fig.update_layout(
            title=f"📈 Performance Trend - {metric_name}",
            xaxis_title="Game",
            yaxis_title=metric_name,
            **CHART_TEMPLATE['layout'],
            height=400
        )
        
        return fig
    except Exception as e:
        print(f"Error creating trend chart: {e}")
        return None


def create_efficiency_gauge(value, title="Efficiency", min_val=0, max_val=100):
    """Create gauge chart for efficiency metrics"""
    
    # Determine color based on value
    if value >= 60:
        color = COLORS['success']
    elif value >= 45:
        color = COLORS['warning']
    else:
        color = COLORS['danger']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'color': COLORS['text'], 'size': 16}},
        number={'font': {'color': COLORS['text'], 'size': 36}, 'suffix': '%'},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickcolor': COLORS['text']},
            'bar': {'color': color},
            'bgcolor': COLORS['background'],
            'borderwidth': 2,
            'bordercolor': COLORS['primary'],
            'steps': [
                {'range': [0, 40], 'color': 'rgba(255,68,68,0.3)'},
                {'range': [40, 55], 'color': 'rgba(255,215,0,0.3)'},
                {'range': [55, 100], 'color': 'rgba(0,255,135,0.3)'}
            ],
            'threshold': {
                'line': {'color': COLORS['text'], 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        **CHART_TEMPLATE['layout'],
        height=300
    )
    
    return fig


def create_shot_distribution_pie(stats):
    """Create pie chart showing shot distribution"""
    
    # Calculate shot types
    shot_types = []
    
    if 'fg_made' in stats and 'three_made' in stats:
        fg = stats['fg_made']
        three = stats['three_made']
        
        two_pt_attempts = fg['attempted'] - three['attempted']
        three_pt_attempts = three['attempted']
        
        if 'ft_made' in stats:
            ft_attempts = stats['ft_made']['attempted']
            shot_types = [
                {'type': '2-Pointers', 'value': two_pt_attempts, 'color': COLORS['primary']},
                {'type': '3-Pointers', 'value': three_pt_attempts, 'color': COLORS['secondary']},
                {'type': 'Free Throws', 'value': ft_attempts, 'color': COLORS['success']}
            ]
        else:
            shot_types = [
                {'type': '2-Pointers', 'value': two_pt_attempts, 'color': COLORS['primary']},
                {'type': '3-Pointers', 'value': three_pt_attempts, 'color': COLORS['secondary']}
            ]
    
    if not shot_types:
        return None
    
    fig = go.Figure(data=[go.Pie(
        labels=[s['type'] for s in shot_types],
        values=[s['value'] for s in shot_types],
        marker_colors=[s['color'] for s in shot_types],
        textinfo='label+percent',
        textfont=dict(color=COLORS['text'], size=12),
        hole=0.4
    )])
    
    fig.update_layout(
        title="🏀 Shot Distribution",
        **CHART_TEMPLATE['layout'],
        height=350
    )
    
    return fig


# ============================================================================
# MAIN ANALYSIS FUNCTION
# ============================================================================
def analyze_and_visualize(text, context=""):
    """
    Main function to analyze text and generate appropriate visualizations
    Returns: (charts_list, analysis_text)
    """
    charts = []
    insights = []
    
    try:
        # Extract stats from text
        stats = extract_stats_from_text(text)
        
        # Check for player comparison
        players_data = extract_player_comparison(text)
        
        # Check for time series data
        time_data = extract_time_series(text)
        
        # Generate appropriate charts
        
        # 1. Single player stats
        if stats and not players_data:
            try:
                bar_chart = create_player_stats_bar(stats)
                if bar_chart:
                    charts.append(('stats_bar', bar_chart))
                    insights.append(generate_stats_insight(stats))
            except Exception as e:
                pass  # Skip this chart if error
            
            try:
                shooting_chart = create_shooting_chart(stats)
                if shooting_chart:
                    charts.append(('shooting', shooting_chart))
                    insights.append(generate_shooting_insight(stats))
            except Exception as e:
                pass  # Skip this chart if error
        
        # 2. Player comparison
        if players_data and len(players_data) >= 2:
            try:
                comparison_chart = create_player_comparison(players_data)
                if comparison_chart:
                    charts.append(('comparison', comparison_chart))
                    insights.append(generate_comparison_insight(players_data))
            except Exception as e:
                pass  # Skip this chart if error
        
        # 3. Trend analysis - SKIP for now to avoid errors
        # if time_data and len(time_data) >= 3:
        #     try:
        #         trend_chart = create_trend_chart(time_data)
        #         if trend_chart:
        #             charts.append(('trend', trend_chart))
        #             insights.append(generate_trend_insight(time_data))
        #     except Exception as e:
        #         pass
        
        # 4. Efficiency metrics
        if stats:
            try:
                # Calculate True Shooting % if possible
                if 'points' in stats and 'fg_made' in stats:
                    fg = stats['fg_made']
                    fta = stats.get('ft_made', {}).get('attempted', 0)
                    if fg.get('attempted', 0) > 0:
                        ts_pct = (stats['points'] / (2 * (fg['attempted'] + 0.44 * fta))) * 100
                        
                        if ts_pct > 0:
                            gauge = create_efficiency_gauge(ts_pct, "True Shooting %")
                            charts.append(('efficiency', gauge))
                            insights.append(f"**True Shooting: {ts_pct:.1f}%** - " + 
                                          ("Elite efficiency! 🔥" if ts_pct >= 60 else 
                                           "Good efficiency 👍" if ts_pct >= 55 else 
                                           "Below average - work on shot selection 📊"))
            except Exception as e:
                pass  # Skip this chart if error
    
    except Exception as e:
        print(f"Error in analyze_and_visualize: {e}")
    
    return charts, insights


def generate_stats_insight(stats):
    """Generate textual insight from stats"""
    insights = []
    
    if 'points' in stats:
        pts = stats['points']
        if pts >= 30:
            insights.append(f"🔥 **{pts} points** - Outstanding scoring performance!")
        elif pts >= 20:
            insights.append(f"👍 **{pts} points** - Solid scoring output")
        else:
            insights.append(f"📊 **{pts} points** scored")
    
    if 'assists' in stats and 'turnovers' in stats:
        ast = stats['assists']
        tov = stats['turnovers']
        ratio = ast / tov if tov > 0 else ast
        if ratio >= 3:
            insights.append(f"✨ Excellent ball security - {ast}:{tov} AST/TO ratio")
        elif ratio >= 2:
            insights.append(f"👍 Good decision making - {ast}:{tov} AST/TO ratio")
        else:
            insights.append(f"⚠️ Need to reduce turnovers - {ast}:{tov} AST/TO ratio")
    
    return " | ".join(insights) if insights else "Stats recorded"


def generate_shooting_insight(stats):
    """Generate shooting analysis insight"""
    insights = []
    
    if 'fg_made' in stats:
        fg = stats['fg_made']
        pct = (fg['made'] / fg['attempted'] * 100) if fg['attempted'] > 0 else 0
        insights.append(f"FG: {fg['made']}/{fg['attempted']} ({pct:.1f}%)")
    
    if 'three_made' in stats:
        three = stats['three_made']
        pct = (three['made'] / three['attempted'] * 100) if three['attempted'] > 0 else 0
        if pct >= 40:
            insights.append(f"🎯 Hot from 3! {three['made']}/{three['attempted']} ({pct:.1f}%)")
        else:
            insights.append(f"3PT: {three['made']}/{three['attempted']} ({pct:.1f}%)")
    
    return " | ".join(insights) if insights else ""


def generate_comparison_insight(players_data):
    """Generate comparison insight between players"""
    if len(players_data) < 2:
        return ""
    
    players = list(players_data.items())
    insights = []
    
    # Compare key stats
    for stat in ['points', 'rebounds', 'assists']:
        values = []
        for name, stats in players:
            val = stats.get(stat, 0)
            if isinstance(val, dict):
                val = val.get('made', 0)
            values.append((name, val))
        
        if all(v[1] > 0 for v in values):
            best = max(values, key=lambda x: x[1])
            insights.append(f"**{stat.title()}**: {best[0]} leads with {best[1]}")
    
    return " | ".join(insights) if insights else "Comparison generated"


def generate_trend_insight(time_data):
    """Generate trend analysis insight"""
    if len(time_data) < 2:
        return ""
    
    values = [g.get('points', g.get('value', 0)) for g in time_data]
    
    # Calculate trend
    first_half = sum(values[:len(values)//2]) / (len(values)//2)
    second_half = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
    
    if second_half > first_half * 1.1:
        return "📈 **Trending UP** - Performance improving over time!"
    elif second_half < first_half * 0.9:
        return "📉 **Trending DOWN** - Performance declining, may need rest or adjustment"
    else:
        return "➡️ **Consistent** - Stable performance level"


# ============================================================================
# STREAMLIT DISPLAY FUNCTION
# ============================================================================
def display_analytics(text, context=""):
    """Display analytics charts in Streamlit"""
    
    try:
        charts, insights = analyze_and_visualize(text, context)
        
        if not charts:
            return False
        
        for chart_type, chart in charts:
            try:
                st.plotly_chart(chart, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display {chart_type} chart")
        
        if insights:
            st.markdown("#### 💡 Key Insights")
            for insight in insights:
                if insight:
                    st.markdown(f"• {insight}")
        
        return True
    except Exception as e:
        st.error(f"Error displaying analytics: {str(e)}")
        return False