# -*- coding: utf-8 -*-
"""
HOOPS AI - Basketball Coaching Staff
Virtual Locker Room with Multi-Agent System
Powered by OpenAI GPT + Supabase
"""

import streamlit as st
from openai import OpenAI
from supabase import create_client
from enum import Enum
from datetime import datetime

# ============================================================================
# PAGE CONFIG - Must be first Streamlit command
# ============================================================================
st.set_page_config(
    page_title="HOOPS AI - Your Personal Assistant Coach",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CONSTANTS
# ============================================================================
LOGO_URL = "https://i.postimg.cc/DfYpGxMy/Fashion-Bran-Logo.png"
BACKGROUND_URL = "https://i.postimg.cc/nr6WXxHh/wlm-kdwrsl.jpg"

AGE_GROUPS = ["U10", "U12", "U14", "U16", "U18", "Senior"]
LEVELS = ["Beginner", "League", "Competitive", "Professional"]

class Agent(Enum):
    ASSISTANT_COACH = "assistant_coach"
    TACTICIAN = "tactician"
    SKILLS_COACH = "skills_coach"
    NUTRITIONIST = "nutritionist"
    STRENGTH_COACH = "strength_coach"
    ANALYST = "analyst"
    YOUTH_COACH = "youth_coach"

AGENT_INFO = {
    Agent.ASSISTANT_COACH: {
        "name": "ASSISTANT COACH",
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
    },
    Agent.NUTRITIONIST: {
        "name": "SPORTS NUTRITIONIST",
        "icon": "🥗",
        "title": "Nutrition Expert",
        "specialty": "Personalized Diet Plans",
        "color": "#FFD700"
    },
    Agent.STRENGTH_COACH: {
        "name": "STRENGTH & CONDITIONING",
        "icon": "🏋️",
        "title": "Physical Development",
        "specialty": "Athletic Performance",
        "color": "#FF4500"
    },
    Agent.ANALYST: {
        "name": "THE ANALYST",
        "icon": "📊",
        "title": "Data & Statistics Expert",
        "specialty": "Performance Analytics",
        "color": "#9370DB"
    },
    Agent.YOUTH_COACH: {
        "name": "YOUTH COACH",
        "icon": "👶",
        "title": "Kids Development Expert",
        "specialty": "Ages 5-12 Specialist",
        "color": "#FF69B4"
    }
}

def get_system_prompt(agent, coach_profile=None):
    """Generate system prompt with coach profile context"""
    
    base_prompts = {
        Agent.ASSISTANT_COACH: """You are an elite Head Assistant Coach, acting as a strategic advisor and manager of team culture. You balance high-performance efficiency with educational pedagogy.

CORE PRINCIPLES:
- Prioritize role modeling and the "Spirit of Sport" (health, fair play, honesty)
- Define success by skill improvement and "process" rather than just the scoreboard
- Maintain strict integrity regarding anti-doping and safe environments

PEDAGOGY & LEARNING:
- Utilize the four educator roles: Facilitator, Expert, Evaluator, and Coach
- Apply the 4 stages of motor learning: Coordination, Control, Skill, and Automaticity
- Use "Implicit Learning" and analogies for resilience under stress
- Understand that learning is non-linear - expect plateaus and breakthroughs

ELITE MANAGEMENT:
- Oversee support staff and manage administrative and parental relationships
- Analyze team efficiency using PAWS (Player Adjusted Wins Score) and possession-based metrics
- Manage high-performance logistics, including sleep and recovery for international travel
- Handle team culture, communication protocols, and conflict resolution
- Plan and structure practices, seasons, and development programs

CRITICAL APPROACH:
- Balance winning with player development based on age group
- Create positive learning environments where mistakes are growth opportunities
- Manage relationships with players, parents, staff, and administration professionally
- Use data to support decisions but never lose sight of the human element""",

        Agent.TACTICIAN: """You are a Master Tactician responsible for offensive and defensive systems, transition protocols, and in-game strategic adjustments.

DEFENSIVE STRATEGY:
- Implement Man-to-Man as the mandatory base, focusing on the "Split Line" and "Help and Recover"
- Apply advanced screen defenses: Lock and Trail, Ice (Push), and Weak
- Manage elite Match-up Zone systems and 2-2-1 full-court trapping protocols
- Teach closeout techniques: "High Hands", contest without fouling
- Rotations and help-side principles for team defense

OFFENSIVE STRATEGY:
- Deploy 5-Out and 4-Out 1-In Motion offenses based on "Read & React" principles
- Manage structured Secondary Breaks and End-of-Game (EBO) set plays
- Dismantle zone defenses using skip passes, gap penetration, and "Short Corner" positioning
- Design ATOs (After Time Out), SLOBs (Sideline Out of Bounds), BLOBs (Baseline Out of Bounds)
- Spacing principles: maintain 12-15 feet between players, create driving lanes

TRANSITION GAME:
- Primary break: push the ball, fill lanes, attack before defense sets
- Secondary break: structured actions off the primary
- Transition defense: sprint back, protect the paint, match up

ANALYTICS & SCOUTING:
- Provide "cures, not diagnoses" in scouting reports
- Adjust tempo and player rotations based on points per possession and efficiency data
- Identify opponent tendencies and create game-specific strategies
- Use video and statistics to prepare for opponents

CRITICAL APPROACH:
- Keep systems simple enough for players to execute under pressure
- Adjust tactics based on personnel - not every system fits every team
- In-game adjustments: read and react to what the opponent is doing
- Always have counter-actions ready when opponents adjust""",

        Agent.SKILLS_COACH: """You are a Professional Skills Coach - a technical development specialist focused on individual biomechanics, technical execution, and the "Game-Based" approach to training.

TECHNICAL MASTERY - SHOOTING:
- Teach shooting using the BEEF principle (Balance, Eyes, Elbow, Follow-through)
- Refine the "Shooter's Catch" - ready to shoot before receiving the ball
- Shot preparation: hop vs 1-2 step, turn and face
- Free throw routine consistency and mental preparation
- Range development: start close, expand with proper form

TECHNICAL MASTERY - FOOTWORK:
- Advanced footwork: Euro-step, Jump stop, Stride stop, Pro hop
- Triple threat positioning and jab step series
- Pivot foot mastery: front pivot, reverse pivot, drop step
- Post footwork: drop step, jump hook, up-and-under

TECHNICAL MASTERY - BALL HANDLING:
- Master elite penetration tools: Snake dribble, Push dribble, Jab steps
- Pound dribbles, crossovers, between-the-legs, behind-the-back
- Change of pace and direction - sell the move
- Combo moves: crossover to between-legs, hesitation to crossover
- Weak hand development - equal proficiency required

TECHNICAL MASTERY - FINISHING:
- Layup package: finger roll, power finish, reverse, floater
- Contact finishing: absorb and finish through contact
- Shot fakes and up-and-under moves at the rim

PEDAGOGICAL METHODOLOGY:
- Replace static drills with "Game-Based" activities to teach decision-making
- Maintain "Perception-Action Coupling" by including defenders in technical drills
- Use "Discovery Learning" and constraints to force players to find technical solutions
- Progression: technique → speed → pressure → game-like

PHYSICAL CONDITIONING FOR SKILLS:
- Train Alactic systems (<15 seconds) using a 1:8 work-to-rest ratio for maximum explosiveness
- Implement lockdown defensive individual skills: "Big to Bigger" sliding and high-hands "Close Outs"
- Balance skill work with appropriate rest for quality repetitions

CRITICAL APPROACH:
- Individualize training based on player's current level and goals
- Quality over quantity - perfect practice makes perfect
- Video analysis to show players their technique vs ideal technique
- Break complex skills into teachable components, then integrate""",

        Agent.NUTRITIONIST: """You are an expert Sports Nutritionist specializing in basketball players of ALL age groups.

YOUR EXPERTISE:
- Personalized nutrition plans based on individual player data (age, weight, height, position, activity level)
- Pre-game, during-game, and post-game nutrition strategies
- Hydration protocols for training and competition
- Age-appropriate nutrition (youth players need different approaches than adults)
- Muscle building vs. weight management diets
- Supplement guidance (age-appropriate, safe, legal)
- Recovery nutrition and sleep optimization
- Dealing with picky eaters (especially young players)

CRITICAL APPROACH:
- ALWAYS ask for specific player data before giving recommendations: age, weight, height, position, training frequency, goals
- Create PERSONALIZED meal plans - never generic advice
- Consider cultural food preferences and availability
- Adjust recommendations based on game schedule and training intensity
- For youth players: focus on growth, development, and healthy habits
- For adult players: focus on performance optimization and recovery

Provide specific meal plans, grocery lists, and practical recipes when asked.""",

        Agent.STRENGTH_COACH: """You are an elite Strength & Conditioning Coach specializing in basketball.

YOUR EXPERTISE:
- Age-specific athletic development:
  * U10-U12: Coordination, balance, agility, FUN movement patterns, bodyweight exercises
  * U14-U16: Introduction to resistance training, explosive power foundation, jump training basics
  * U18+: Full strength programs, plyometrics, power development, vertical jump optimization
- Basketball-specific physical attributes: vertical leap, lateral quickness, core stability, injury prevention
- Periodization: weekly, monthly, and yearly training plans
- Load management based on game schedule and competition calendar
- Individual player assessment and personalized programs
- Injury prevention and prehab exercises
- Recovery protocols and deload weeks

CRITICAL APPROACH:
- ALWAYS ask for player data before programming: age, training history, current fitness level, injury history, goals
- Create INDIVIDUALIZED programs - never one-size-fits-all
- Consider the basketball practice and game schedule when designing strength work
- Build programs that complement basketball training, not compete with it
- For young players: emphasize movement quality over load
- For older players: progressive overload with proper periodization

Provide detailed workout plans with sets, reps, rest periods, and exercise descriptions.
Can create daily, weekly, monthly, and seasonal training programs based on team schedule and goals.""",

        Agent.ANALYST: """You are an elite Basketball Analytics Expert and Performance Analyst.

YOUR EXPERTISE:
- Team Statistics Analysis:
  * Turnovers vs Assists ratio - identifying ball movement issues
  * Shot selection analysis (2PT vs 3PT attempts, efficiency, shot zones)
  * Free throw rate and drawing fouls
  * Offensive/Defensive efficiency ratings
  * Pace and possession analysis
  * Rebounding (offensive/defensive) and second chance points

- Player Statistics Analysis:
  * Individual scoring efficiency (TS%, eFG%, Points per possession)
  * Usage rate and ball dominance
  * Plus/minus and impact metrics
  * Shot charts and hot zones
  * Assist to turnover ratio
  * Clutch performance (last 5 minutes, close games)

- Actionable Insights:
  * If high turnovers → analyze WHO is turning it over and WHEN (transition vs halfcourt, early vs late clock)
  * If low assists → identify if it's personnel, spacing, or system issue
  * If poor shooting → break down by shot type, defender proximity, catch-and-shoot vs off-dribble
  * Recommend lineup changes based on data
  * Identify which player should have the ball in crucial moments
  * Suggest style-of-play adjustments based on team strengths/weaknesses

- Opponent Scouting:
  * Identify opponent tendencies and weaknesses
  * Suggest game plans based on matchup data
  * Key players to target or avoid

CRITICAL APPROACH:
- ALWAYS ask for specific data/statistics before providing analysis
- Don't guess - request numbers: "How many turnovers? How many assists? What's the shooting breakdown?"
- Provide SPECIFIC, ACTIONABLE recommendations - not generic advice
- Use data to support every recommendation
- Connect statistics to practical on-court solutions
- Consider context: age group, competition level, team goals

When given stats, provide:
1. What the numbers tell us (diagnosis)
2. Why it might be happening (root cause)
3. What to do about it (actionable solutions)
4. How to measure improvement (KPIs to track)""",

        Agent.YOUTH_COACH: """You are an expert Youth Basketball Coach specializing in children ages 5-12.

YOUR PHILOSOPHY:
- FUN FIRST - If kids aren't having fun, they won't learn or stay in the sport
- Development over winning - focus on long-term player development, not short-term results
- Every child is different - adapt to individual learning styles and abilities
- Positive reinforcement - build confidence through encouragement
- Age-appropriate expectations - don't expect adult skills from children

AGE-SPECIFIC APPROACH:

MINI BASKETBALL (Ages 5-8):
- Focus: Basic motor skills, coordination, balance, FUN
- Ball handling: Small balls, basic dribbling games
- Shooting: Lowered baskets, proper form introduction
- Games: Tag games with basketballs, relay races, simple 1v1 and 2v2
- Attention span: 10-15 minutes per activity MAX, then switch
- NO complex plays or tactics - let them play freely
- Key skills: Catching, passing (chest pass only), basic dribble, layups

YOUTH (Ages 9-12):
- Focus: Fundamental skills, teamwork introduction, game understanding
- Ball handling: Both hands, basic moves (crossover, between legs intro)
- Shooting: Correct form emphasis, free throws, short-range shots
- Defense: Stance, sliding, basic concepts (no complex schemes)
- Games: 3v3, 4v4, modified 5v5 with simple rules
- Attention span: 20-30 minutes per activity
- Introduce: Basic spacing, give-and-go, pick concepts (age 11-12)
- Key skills: Triple threat, pivot footwork, passing variety, boxing out

TRAINING SESSION STRUCTURE:
1. Dynamic warm-up with ball (5-10 min) - fun and active
2. Skill station work (15-20 min) - rotate every 5 min
3. Game-like drills/scrimmage (15-20 min) - apply skills
4. Fun game/competition (5-10 min) - end on high note

CRITICAL APPROACH:
- ALWAYS ask the age of players before giving advice
- Use GAMES to teach skills, not boring repetitive drills
- Keep instructions SHORT and SIMPLE
- Demonstrate more, talk less
- Celebrate effort, not just results
- NEVER yell or criticize harshly - redirect positively
- Include ALL players, not just the talented ones

WHAT TO AVOID:
- Zone defenses before age 12
- Full court press before age 10
- Complex plays with more than 2 actions
- Position specialization before age 12
- Excessive focus on winning
- Comparing kids to each other
- Long explanations - keep it simple!"""
    }
    
    prompt = base_prompts[agent]
    
    # Add coach profile context if available
    if coach_profile:
        prompt += f"""

COACH PROFILE - Adapt your answers accordingly:
- Coach Name: {coach_profile.get('name', 'Unknown')}
- Team: {coach_profile.get('team_name', 'Unknown')}
- Age Group: {coach_profile.get('age_group', 'Unknown')}
- Level: {coach_profile.get('level', 'Unknown')}

IMPORTANT: Tailor your advice to the {coach_profile.get('age_group', '')} age group and {coach_profile.get('level', '')} level!"""
    
    # Add accuracy and honesty instructions to ALL agents
    prompt += """

CRITICAL RULES FOR ALL RESPONSES:
1. BE PRECISE - Only provide information you are confident about. No guessing.
2. BE HONEST - If you don't know something or are unsure, say it clearly: "I don't have enough information" or "I'm not certain about this"
3. NO VAGUE ANSWERS - Avoid generic or wishy-washy responses. Be specific and actionable.
4. ASK WHEN NEEDED - If you need more information to give a good answer, ASK for it. Don't assume.
5. ADMIT LIMITATIONS - If a question is outside your expertise or requires real-time data you don't have, say so.
6. SOURCES - If recommending something specific (exercise, diet, play), explain WHY it works.
7. SAFETY FIRST - If unsure about safety implications (nutrition, training load), err on the side of caution and recommend consulting a professional.

IMPORTANT: Detect the user's language and respond in the SAME language (Hebrew or English)."""
    
    return prompt

ROUTER_PROMPT = """You are a routing assistant for a basketball coaching app.

AGENTS AVAILABLE:
- TACTICIAN: ONLY for X's & O's, plays, offensive/defensive schemes, zones, ATOs, pick & roll, spacing, game strategy during play
- SKILLS_COACH: basketball drills, shooting technique, dribbling, footwork (ages 13+)
- NUTRITIONIST: food, diet, meals, nutrition, eating, supplements, meal plans
- STRENGTH_COACH: gym, strength, weights, jumping, speed, agility, workout programs
- ANALYST: statistics, data, numbers, turnovers, assists, percentages, efficiency, analytics
- YOUTH_COACH: kids, children, young players, ages 5-12, mini basketball, youth development
- ASSISTANT_COACH: team management, practice planning, communication, leadership, motivation, scheduling, player relationships, parent communication, team culture, administrative tasks, season planning, tryouts, roster management, team rules, handling conflicts, coach development

IMPORTANT DISTINCTIONS:
- "How to run a practice" → ASSISTANT_COACH (not TACTICIAN)
- "How to manage players" → ASSISTANT_COACH (not TACTICIAN)
- "Team communication" → ASSISTANT_COACH
- "How to beat zone defense" → TACTICIAN
- "Pick and roll coverage" → TACTICIAN
- "Offensive sets" → TACTICIAN

CURRENT SITUATION:
Previous agent: {previous_agent}
Agent's last message: {previous_message}
User's response: {question}

ROUTING RULES:
1. If the previous agent ASKED FOR INFORMATION and the user is PROVIDING that information → STAY with the SAME agent
2. If the user mentions ages 5-12, kids, children, mini basketball → YOUTH_COACH
3. If about team MANAGEMENT, PLANNING, COMMUNICATION, LEADERSHIP → ASSISTANT_COACH
4. If about ON-COURT TACTICS, PLAYS, SCHEMES → TACTICIAN
5. Numbers, measurements, statistics responses are ALWAYS continuations → STAY with same agent
6. When in doubt → STAY with the same agent

Which agent should handle this? Answer with ONE word: TACTICIAN, SKILLS_COACH, NUTRITIONIST, STRENGTH_COACH, ANALYST, YOUTH_COACH, or ASSISTANT_COACH"""


ROUTER_PROMPT_NO_CONTEXT = """Determine which coach should answer this basketball question.

AGENTS:
- TACTICIAN: ONLY for X's & O's, plays, offensive/defensive schemes, zones, ATOs, pick & roll, spacing, game strategy during play
- SKILLS_COACH: basketball drills, shooting technique, dribbling, footwork (ages 13+)
- NUTRITIONIST: food, diet, meals, nutrition, eating, supplements, meal plans
- STRENGTH_COACH: gym, strength, weights, jumping, speed, agility, workout programs
- ANALYST: statistics, data, numbers, turnovers, assists, percentages, efficiency, analytics
- YOUTH_COACH: kids, children, young players, ages 5-12, mini basketball, youth development
- ASSISTANT_COACH: team management, practice planning, communication, leadership, motivation, scheduling, player relationships, parent communication, team culture, administrative tasks, season planning, tryouts, roster management, team rules, handling conflicts

IMPORTANT DISTINCTIONS:
- "How to run a practice" → ASSISTANT_COACH (not TACTICIAN)
- "How to manage players" → ASSISTANT_COACH (not TACTICIAN)
- "Team communication" → ASSISTANT_COACH
- "Season planning" → ASSISTANT_COACH
- "How to beat zone defense" → TACTICIAN
- "Pick and roll coverage" → TACTICIAN
- "Offensive sets" → TACTICIAN

Question: {question}

Answer with ONE word: TACTICIAN, SKILLS_COACH, NUTRITIONIST, STRENGTH_COACH, ANALYST, YOUTH_COACH, or ASSISTANT_COACH"""

# ============================================================================
# CSS STYLING
# ============================================================================
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('BACKGROUND_URL_PLACEHOLDER');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Global text color - prevent dark text on dark background */
    .stApp p, .stApp span, .stApp li, .stApp label, .stApp div {
        color: #FFFFFF;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(13,13,13,0.95) 0%, rgba(26,26,26,0.95) 50%, rgba(13,13,13,0.95) 100%);
        border-right: 1px solid rgba(255, 107, 53, 0.3);
    }
    
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background: rgba(30, 30, 30, 0.8) !important;
        border: 1px solid rgba(255, 107, 53, 0.3) !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
        color: #FF6B35 !important;
    }
    
    .hero-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #FF6B35, #FF8C42, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 0.5rem;
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
        background: linear-gradient(135deg, rgba(20,20,20,0.9), rgba(30,30,30,0.85));
        border: 2px solid rgba(255, 107, 53, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 0 30px rgba(255, 107, 53, 0.2);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stChatMessage"] {
        background: linear-gradient(135deg, rgba(25,25,25,0.85), rgba(35,35,35,0.8));
        border: 1px solid rgba(255, 107, 53, 0.2);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.8rem 0;
        backdrop-filter: blur(5px);
    }
    
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div {
        color: #FFFFFF !important;
    }
    
    [data-testid="stChatMessage"] strong {
        color: #FF6B35 !important;
    }
    
    [data-testid="stChatInput"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    [data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important;
        background: rgba(25, 25, 25, 0.95) !important;
        border: 2px solid rgba(255, 107, 53, 0.5) !important;
        border-radius: 25px !important;
        padding: 0.8rem 1rem !important;
    }
    
    [data-testid="stChatInput"] textarea:focus {
        border-color: #FF6B35 !important;
        box-shadow: 0 0 15px rgba(255, 107, 53, 0.4) !important;
    }
    
    [data-testid="stChatInput"] textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    [data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #FF6B35, #FF8C42) !important;
        border-radius: 50% !important;
        color: #000 !important;
    }
    
    [data-testid="stChatInput"] button:hover {
        box-shadow: 0 0 20px rgba(255, 107, 53, 0.6) !important;
    }
    
    [data-testid="stBottom"] {
        background: rgba(13, 13, 13, 0.98) !important;
        border-top: 1px solid rgba(255, 107, 53, 0.3) !important;
    }
    
    [data-testid="stBottom"] > div {
        background: transparent !important;
    }
    
    [data-testid="stBottom"] * {
        background-color: transparent !important;
    }
    
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] > div > div {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    .stButton > button {
        font-family: 'Orbitron', monospace;
        font-weight: 600;
        background: rgba(255, 107, 53, 0.2);
        color: #FF6B35;
        border: 2px solid #FF6B35;
        border-radius: 25px;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FF6B35, #FF8C42);
        color: #000;
        box-shadow: 0 0 30px rgba(255, 107, 53, 0.5);
    }
    
    .welcome-banner {
        background: linear-gradient(135deg, rgba(255,107,53,0.2), rgba(255,140,66,0.15), rgba(0,212,255,0.1));
        border: 2px solid rgba(255, 107, 53, 0.4);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
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
        background: linear-gradient(90deg, transparent, rgba(255,107,53,0.5), transparent);
        margin: 1.5rem 0;
    }
    
    .response-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 107, 53, 0.2);
        border: 1px solid rgba(255, 107, 53, 0.5);
        border-radius: 20px;
        padding: 0.4rem 1rem;
        margin-bottom: 1rem;
        font-family: 'Orbitron', monospace;
        font-size: 0.85rem;
        font-weight: 600;
        color: #FF6B35;
    }
    
    .login-container {
        background: linear-gradient(135deg, rgba(20,20,20,0.95), rgba(30,30,30,0.9));
        border: 2px solid rgba(255, 107, 53, 0.5);
        border-radius: 20px;
        padding: 2rem;
        max-width: 500px;
        margin: 2rem auto;
        backdrop-filter: blur(10px);
    }
    
    .profile-card {
        background: rgba(255, 107, 53, 0.1);
        border: 1px solid rgba(255, 107, 53, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .history-item {
        background: rgba(30, 30, 30, 0.8);
        border: 1px solid rgba(255, 107, 53, 0.2);
        border-radius: 10px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .history-item:hover {
        border-color: #FF6B35;
        background: rgba(255, 107, 53, 0.1);
    }
    
    /* Form styling */
    .stTextInput input, .stSelectbox select {
        background: rgba(30, 30, 30, 0.9) !important;
        border: 1px solid rgba(255, 107, 53, 0.3) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: #FF6B35 !important;
        box-shadow: 0 0 10px rgba(255, 107, 53, 0.3) !important;
    }
    
    ::-webkit-scrollbar {width: 8px;}
    ::-webkit-scrollbar-track {background: #0D0D0D;}
    ::-webkit-scrollbar-thumb {background: linear-gradient(#FF6B35, #FF8C42); border-radius: 4px;}
    
    /* Mobile-only buttons - hide on desktop */
    .mobile-buttons {
        display: none;
    }
    
    @media (max-width: 768px) {
        .mobile-buttons {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
    }
    
    /* Sidebar toggle arrow for desktop */
    .sidebar-toggle {
        position: fixed;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        background: linear-gradient(135deg, #FF6B35, #FF8C42);
        color: #000;
        border: none;
        border-radius: 0 10px 10px 0;
        padding: 15px 8px;
        cursor: pointer;
        z-index: 1000;
        font-size: 1.2rem;
        box-shadow: 2px 0 10px rgba(255, 107, 53, 0.3);
        transition: all 0.3s ease;
    }
    
    .sidebar-toggle:hover {
        padding-left: 15px;
        box-shadow: 2px 0 20px rgba(255, 107, 53, 0.5);
    }
    
    @media (max-width: 768px) {
        .sidebar-toggle {
            display: none;
        }
    }
</style>
""".replace('BACKGROUND_URL_PLACEHOLDER', BACKGROUND_URL)

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================
@st.cache_resource
def get_supabase_client():
    """Initialize Supabase client"""
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if not url or not key:
            return None
        return create_client(url, key)
    except Exception as e:
        st.error(f"Failed to connect to Supabase: {e}")
        return None

def get_coach_by_email(supabase, email):
    """Get coach profile by email"""
    try:
        result = supabase.table("coaches").select("*").eq("email", email).execute()
        if result.data:
            return result.data[0]
        return None
    except Exception:
        return None

def create_coach(supabase, name, email, team_name, age_group, level):
    """Create new coach profile"""
    try:
        result = supabase.table("coaches").insert({
            "name": name,
            "email": email,
            "team_name": team_name,
            "age_group": age_group,
            "level": level
        }).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        st.error(f"Error creating profile: {e}")
        return None

def get_coach_conversations(supabase, coach_id):
    """Get all conversations for a coach"""
    try:
        result = supabase.table("conversations").select("*").eq("coach_id", coach_id).order("created_at", desc=True).execute()
        return result.data or []
    except Exception:
        return []

def create_conversation(supabase, coach_id, title):
    """Create new conversation"""
    try:
        result = supabase.table("conversations").insert({
            "coach_id": coach_id,
            "title": title
        }).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None

def save_message(supabase, conversation_id, role, content, agent=None):
    """Save message to database"""
    try:
        supabase.table("messages").insert({
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "agent": agent
        }).execute()
    except Exception:
        pass

def get_conversation_messages(supabase, conversation_id):
    """Get all messages for a conversation"""
    try:
        result = supabase.table("messages").select("*").eq("conversation_id", conversation_id).order("created_at").execute()
        return result.data or []
    except Exception:
        return []

def update_conversation_title(supabase, conversation_id, title):
    """Update conversation title"""
    try:
        supabase.table("conversations").update({"title": title}).eq("id", conversation_id).execute()
    except Exception:
        pass

def get_agent_documents(supabase, agent_name):
    """Get all documents for a specific agent (simple retrieval without embeddings)"""
    try:
        result = supabase.table("documents").select("title, content").eq("agent", agent_name).execute()
        return result.data or []
    except Exception:
        return []

def get_agent_knowledge(supabase, agent):
    """Build knowledge context from agent's documents"""
    agent_name = agent.value  # e.g., "youth_coach"
    documents = get_agent_documents(supabase, agent_name)
    
    if not documents:
        return ""
    
    knowledge = "\n\nKNOWLEDGE BASE - Use this information to answer questions:\n"
    knowledge += "=" * 50 + "\n"
    
    for doc in documents:
        knowledge += f"\n### {doc.get('title', 'Document')}\n"
        knowledge += f"{doc.get('content', '')}\n"
        knowledge += "-" * 30 + "\n"
    
    knowledge += "\nIMPORTANT: Use the knowledge base above when relevant. If the question is about something in your knowledge base, prioritize that information."
    
    return knowledge

# ============================================================================
# OPENAI FUNCTIONS
# ============================================================================
@st.cache_resource
def get_openai_client():
    """Initialize OpenAI client"""
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            return None
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize OpenAI: {e}")
        return None

def route_question(question, client, chat_history=None):
    """Route question to appropriate agent with smart context awareness"""
    try:
        # Check if we have previous context
        previous_agent = None
        previous_message = None
        
        if chat_history and len(chat_history) >= 1:
            # Find the last assistant message
            for msg in reversed(chat_history):
                if msg.get("role") == "assistant" and msg.get("agent"):
                    previous_agent = msg.get("agent")
                    previous_message = msg.get("raw_content", msg.get("content", ""))[:300]
                    break
        
        # SMART CHECK: If previous agent asked a question and user gives short/data response, STAY
        if previous_agent and previous_message:
            # Check if previous message contains a question
            has_question = "?" in previous_message or any(word in previous_message.lower() for word in 
                ["please provide", "tell me", "what is", "how much", "how many", "ספר לי", "מה", "כמה", "איזה", "אנא"])
            
            # Check if user response looks like data/continuation (short, has numbers, answering format)
            is_data_response = (
                len(question) < 200 or  # Short response
                any(char.isdigit() for char in question) or  # Contains numbers
                question.strip().startswith(("גיל", "משקל", "גובה", "age", "weight", "height", "כן", "לא", "yes", "no"))
            )
            
            # If agent asked question and user seems to be answering → STAY with same agent
            if has_question and is_data_response:
                # Return previous agent directly without asking Router
                for agent in Agent:
                    if agent.value == previous_agent:
                        return agent
        
        # Use Router for new topics or when no clear continuation
        if previous_agent and previous_message:
            prompt = ROUTER_PROMPT.format(
                previous_agent=previous_agent.upper().replace("_", " "),
                previous_message=previous_message[:200],
                question=question
            )
        else:
            prompt = ROUTER_PROMPT_NO_CONTEXT.format(question=question)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,
            temperature=0
        )
        result = response.choices[0].message.content.strip().upper()
        
        if "TACTICIAN" in result:
            return Agent.TACTICIAN
        elif "SKILLS" in result:
            return Agent.SKILLS_COACH
        elif "NUTRITION" in result:
            return Agent.NUTRITIONIST
        elif "STRENGTH" in result:
            return Agent.STRENGTH_COACH
        elif "ANALYST" in result:
            return Agent.ANALYST
        elif "YOUTH" in result:
            return Agent.YOUTH_COACH
        return Agent.ASSISTANT_COACH
    except Exception:
        return Agent.ASSISTANT_COACH

def get_agent_response(question, agent, chat_history, client, coach_profile=None, supabase=None):
    """Get response from specific agent with RAG knowledge"""
    try:
        system_prompt = get_system_prompt(agent, coach_profile)
        
        # Add RAG knowledge if available
        if supabase:
            knowledge = get_agent_knowledge(supabase, agent)
            if knowledge:
                system_prompt += knowledge
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add recent history
        if chat_history:
            for msg in chat_history[-4:]:
                role = "user" if msg["role"] == "user" else "assistant"
                content = msg.get("raw_content", msg["content"])
                messages.append({"role": role, "content": content})
        
        messages.append({"role": "user", "content": question})
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def format_response(response, agent):
    """Format response with agent badge"""
    info = AGENT_INFO[agent]
    badge = f'<div class="response-badge"><span>{info["icon"]}</span><span>{info["name"]}</span></div>'
    return badge + "\n\n" + response

def get_agent_from_value(value):
    """Convert string value to Agent enum"""
    if isinstance(value, Agent):
        return value
    for agent in Agent:
        if agent.value == value:
            return agent
    return Agent.ASSISTANT_COACH

# ============================================================================
# UI COMPONENTS
# ============================================================================
def render_login_page(supabase):
    """Render login/registration page"""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    st.markdown('''
    <div class="scoreboard">
        <div class="hero-title">HOOPS AI</div>
        <div class="hero-subtitle">Your Personal Assistant Coach</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="welcome-banner">
        <div class="welcome-title">🏀 Welcome to HOOPS AI!</div>
        <div class="welcome-text">Enter your details to get personalized coaching advice tailored to your team.</div>
        <div class="welcome-text" style="margin-top:0.5rem; direction:rtl;">הכנס את הפרטים שלך לקבלת ייעוץ מותאם אישית 🇮🇱</div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            st.markdown("### Welcome Back, Coach!")
            login_email = st.text_input("Email", key="login_email", placeholder="your@email.com")
            
            if st.button("🚀 LOGIN", use_container_width=True, key="login_btn"):
                if login_email:
                    coach = get_coach_by_email(supabase, login_email)
                    if coach:
                        st.session_state.coach = coach
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("Coach not found. Please register first.")
                else:
                    st.warning("Please enter your email.")
        
        with tab2:
            st.markdown("### Create Your Profile")
            
            reg_name = st.text_input("Coach Name", key="reg_name", placeholder="John Smith")
            reg_email = st.text_input("Email", key="reg_email", placeholder="your@email.com")
            reg_team = st.text_input("Team Name", key="reg_team", placeholder="Lakers Youth")
            reg_age = st.selectbox("Age Group", AGE_GROUPS, key="reg_age")
            reg_level = st.selectbox("Level", LEVELS, key="reg_level")
            
            if st.button("🏀 CREATE PROFILE", use_container_width=True, key="register_btn"):
                if reg_name and reg_email:
                    # Check if email exists
                    existing = get_coach_by_email(supabase, reg_email)
                    if existing:
                        st.error("Email already registered. Please login.")
                    else:
                        coach = create_coach(supabase, reg_name, reg_email, reg_team, reg_age, reg_level)
                        if coach:
                            st.session_state.coach = coach
                            st.session_state.logged_in = True
                            st.success("Profile created! Redirecting...")
                            st.rerun()
                else:
                    st.warning("Please fill in Name and Email.")

def render_sidebar(supabase):
    """Render sidebar with logo, profile, history"""
    with st.sidebar:
        # Logo
        st.markdown(f'''
        <div style="text-align:center; padding:1rem;">
            <img src="{LOGO_URL}" style="width:180px;">
        </div>
        <div class="sidebar-divider"></div>
        ''', unsafe_allow_html=True)
        
        # Coach Profile
        coach = st.session_state.get('coach', {})
        st.markdown(f'''
        <div class="profile-card">
            <div style="font-family:'Orbitron',monospace; color:#FF6B35; font-size:0.8rem; margin-bottom:0.5rem;">👤 COACH PROFILE</div>
            <div style="font-weight:600; font-size:1.1rem;">{coach.get('name', 'Unknown')}</div>
            <div style="color:#888; font-size:0.85rem;">{coach.get('team_name', '')} | {coach.get('age_group', '')} | {coach.get('level', '')}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
        # New Chat Button
        if st.button("➕ NEW CHAT", use_container_width=True):
            st.session_state.current_conversation = None
            st.session_state.messages = []
            st.rerun()
        
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
        # Chat History
        st.markdown('''
        <div style="font-family:'Orbitron',monospace; color:#FF6B35; font-size:0.9rem; margin-bottom:1rem; letter-spacing:2px;">
            📜 CHAT HISTORY
        </div>
        ''', unsafe_allow_html=True)
        
        conversations = get_coach_conversations(supabase, coach.get('id'))
        
        if conversations:
            for conv in conversations[:10]:  # Show last 10
                title = conv.get('title', 'New Chat')[:30]
                if len(conv.get('title', '')) > 30:
                    title += "..."
                
                if st.button(f"💬 {title}", key=f"conv_{conv['id']}", use_container_width=True):
                    st.session_state.current_conversation = conv
                    # Load messages
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
        
        # Coaching Staff
        st.markdown('''
        <div style="font-family:'Orbitron',monospace; color:#FF6B35; font-size:0.9rem; margin-bottom:1rem; letter-spacing:2px;">
            👥 COACHING STAFF
        </div>
        ''', unsafe_allow_html=True)
        
        for agent in Agent:
            info = AGENT_INFO[agent]
            with st.expander(f"{info['icon']} {info['name']}", expanded=False):
                st.markdown(f'''
                <div style="font-family:'Rajdhani',sans-serif;">
                    <div style="color:{info['color']}; font-weight:600;">{info['title']}</div>
                    <div style="color:#888; font-size:0.85rem;">{info['specialty']}</div>
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
        
        st.markdown('''
        <div class="sidebar-divider"></div>
        <div style="text-align:center; padding:1rem;">
            <div style="font-family:'Rajdhani',sans-serif; color:#666; font-size:0.8rem;">
                Powered by<br>
                <span style="color:#FF6B35; font-family:'Orbitron',monospace;">OpenAI GPT</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)

def render_header():
    """Render main header"""
    st.markdown('''
    <div class="scoreboard">
        <div class="hero-title">HOOPS AI</div>
        <div class="hero-subtitle">Your Personal Assistant Coach</div>
    </div>
    ''', unsafe_allow_html=True)

def render_welcome():
    """Render welcome banner for new chats"""
    if not st.session_state.messages:
        coach = st.session_state.get('coach', {})
        
        # Mobile-only buttons (hidden on desktop via CSS)
        st.markdown('''
        <div class="mobile-buttons">
        </div>
        ''', unsafe_allow_html=True)
        
        # Mobile buttons using Streamlit (will be hidden on desktop)
        is_mobile = st.session_state.get('is_mobile', False)
        
        # Show mobile buttons
        col_new, col_history, col_exit = st.columns(3)
        with col_new:
            if st.button("➕ NEW", key="new_chat_main", use_container_width=True, help="Start new chat"):
                st.session_state.current_conversation = None
                st.session_state.messages = []
                st.rerun()
        with col_history:
            if st.button("📜 HISTORY", key="history_main", use_container_width=True, help="View chat history"):
                pass  # Sidebar will open
        with col_exit:
            if st.button("🚪 EXIT", key="exit_main", use_container_width=True, help="Logout"):
                st.session_state.logged_in = False
                st.session_state.coach = None
                st.session_state.messages = []
                st.session_state.current_conversation = None
                st.rerun()
        
        st.markdown(f'''
        <div class="welcome-banner">
            <div class="welcome-title">👋 Hey Coach {coach.get('name', '').split()[0] if coach.get('name') else ''}!</div>
            <div class="welcome-text">Your AI coaching staff is ready. Ask anything about basketball strategy, player development, or team management.</div>
            <div class="welcome-text" style="margin-top:0.5rem;">Tailored for: <strong style="color:#FF6B35;">{coach.get('team_name', '')} | {coach.get('age_group', '')} | {coach.get('level', '')}</strong></div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div style="font-family:'Orbitron',monospace; color:#FF6B35; font-size:0.9rem; margin:1.5rem 0 1rem; letter-spacing:2px;">
            ⚡ QUICK PLAYS
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)
        
        with col1:
            if st.button("🎯 PRACTICE PLAN\n\nBuild a 90-min practice", use_container_width=True):
                st.session_state.pending_prompt = "Build me a 90-minute practice plan for my team, considering our age group and level."
        with col2:
            if st.button("📋 BEAT ZONE\n\nAttack 2-3 zone defense", use_container_width=True):
                st.session_state.pending_prompt = "How should we attack a 2-3 zone defense? Give me specific actions and player movements."
        with col3:
            if st.button("💪 SHOOTING FORM\n\nTeach correct mechanics", use_container_width=True):
                st.session_state.pending_prompt = "How do I teach correct shooting mechanics to my players? Break it down step by step."
        with col4:
            if st.button("👶 FUN DRILLS\n\nGames for kids 6-10", use_container_width=True):
                st.session_state.pending_prompt = "Give me fun and engaging basketball games and drills for kids ages 6-10."
        with col5:
            if st.button("📊 GAME ANALYSIS\n\nAnalyze team stats", use_container_width=True):
                st.session_state.pending_prompt = "I want to analyze my team's performance. What statistics should I provide you?"
        with col6:
            if st.button("📁 UPLOAD STATS\n\nAnalyze from file", use_container_width=True):
                st.session_state.show_file_upload = True
        
        # File upload section
        if st.session_state.get('show_file_upload', False):
            st.markdown('''
            <div style="background: rgba(255,107,53,0.1); border: 1px solid rgba(255,107,53,0.3); border-radius: 15px; padding: 1rem; margin: 1rem 0;">
                <div style="font-family:'Orbitron',monospace; color:#FF6B35; font-size:0.9rem; margin-bottom:0.5rem;">📁 UPLOAD STATISTICS FILE</div>
                <div style="color:#B0B0B0; font-size:0.85rem;">Upload CSV, Excel, or text file with player/team/game statistics</div>
            </div>
            ''', unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=['csv', 'xlsx', 'xls', 'txt'],
                key="stats_file",
                label_visibility="collapsed"
            )
            
            analysis_type = st.selectbox(
                "What do you want to analyze?",
                ["Player individual stats", "Team stats", "Game stats", "Season overview", "Compare players"],
                key="analysis_type"
            )
            
            if uploaded_file is not None:
                try:
                    # Read file content
                    if uploaded_file.name.endswith('.csv'):
                        import pandas as pd
                        df = pd.read_csv(uploaded_file)
                        file_content = df.to_string()
                    elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                        import pandas as pd
                        df = pd.read_excel(uploaded_file)
                        file_content = df.to_string()
                    else:
                        file_content = uploaded_file.read().decode('utf-8')
                    
                    if st.button("🔍 ANALYZE NOW", use_container_width=True):
                        st.session_state.pending_prompt = f"""Please analyze the following {analysis_type.lower()}:

DATA:
{file_content}

Provide:
1. Key insights from the data
2. Strengths identified
3. Areas for improvement
4. Specific recommendations
5. What to focus on in practice"""
                        st.session_state.show_file_upload = False
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error reading file: {e}")
            
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.show_file_upload = False
                st.rerun()

def render_chat(client, supabase):
    """Render chat interface"""
    coach = st.session_state.get('coach', {})
    
    # Sidebar toggle arrow for desktop (when sidebar is collapsed)
    st.markdown('''
    <div class="sidebar-toggle" onclick="window.parent.document.querySelector('[data-testid=collapsedControl]').click()">
        ▶
    </div>
    ''', unsafe_allow_html=True)
    
    # Mobile-only buttons at top when there are messages
    if st.session_state.messages:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("➕ NEW", key="new_chat_top", use_container_width=True):
                st.session_state.current_conversation = None
                st.session_state.messages = []
                st.rerun()
        with col2:
            if st.button("📜 HISTORY", key="history_top", use_container_width=True):
                pass  # User will click sidebar
        with col3:
            if st.button("🚪 EXIT", key="logout_top", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.coach = None
                st.session_state.messages = []
                st.session_state.current_conversation = None
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
    
    # Handle pending prompt from quick buttons
    prompt = st.session_state.pop("pending_prompt", None)
    
    # Or get new input
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
        
        # Route and respond
        with st.spinner("🏀 Analyzing..."):
            agent = route_question(prompt, client, st.session_state.messages[:-1])
        
        info = AGENT_INFO[agent]
        with st.chat_message("assistant", avatar=info["icon"]):
            with st.spinner(f"Consulting {info['name']}..."):
                raw_response = get_agent_response(
                    prompt, agent, 
                    st.session_state.messages[:-1], 
                    client, 
                    coach,  # Pass coach profile
                    supabase  # Pass supabase for RAG
                )
                formatted = format_response(raw_response, agent)
            st.markdown(formatted, unsafe_allow_html=True)
        
        # Save assistant message
        if st.session_state.current_conversation:
            save_message(supabase, st.session_state.current_conversation['id'], "assistant", formatted, agent.value)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": formatted,
            "raw_content": raw_response,
            "agent": agent.value
        })
        st.rerun()

# ============================================================================
# MAIN
# ============================================================================
def main():
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_conversation" not in st.session_state:
        st.session_state.current_conversation = None
    
    # Initialize clients
    supabase = get_supabase_client()
    openai_client = get_openai_client()
    
    if not supabase:
        st.error("⚠️ Database connection failed. Check SUPABASE_URL and SUPABASE_KEY in secrets.")
        st.stop()
    
    if not openai_client:
        st.error("⚠️ OpenAI connection failed. Check OPENAI_API_KEY in secrets.")
        st.stop()
    
    # Show login or main app
    if not st.session_state.logged_in:
        render_login_page(supabase)
    else:
        st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
        render_sidebar(supabase)
        render_header()
        render_welcome()
        render_chat(openai_client, supabase)

if __name__ == "__main__":
    main()