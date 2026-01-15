# -*- coding: utf-8 -*-
"""
HOOPS AI - Configuration
Constants, Agent definitions, and settings
"""

from enum import Enum

# ============================================================================
# APP SETTINGS
# ============================================================================
APP_TITLE = "HOOPS AI - Your Personal Assistant Coach"
APP_ICON = "https://i.postimg.cc/WpnXDQym/LOGO-HOOPS-AI.png"

# ============================================================================
# URLS
# ============================================================================
LOGO_URL = "https://i.postimg.cc/WpnXDQym/LOGO-HOOPS-AI.png"
BACKGROUND_URL = "https://i.postimg.cc/nr6WXxHh/wlm-kdwrsl.jpg"

# ============================================================================
# FORM OPTIONS
# ============================================================================
AGE_GROUPS = ["U10", "U12", "U14", "U16", "U18", "Senior"]
LEVELS = ["Beginner", "League", "Competitive", "Professional"]

# ============================================================================
# FILE UPLOAD SETTINGS
# ============================================================================
ALLOWED_FILE_TYPES = ['csv', 'xlsx', 'xls', 'txt', 'png', 'jpg', 'jpeg', 'webp']
ANALYSIS_TYPES = [
    "Player individual stats",
    "Team stats", 
    "Game stats",
    "Season overview",
    "Compare players"
]

# ============================================================================
# AGENTS
# ============================================================================
class Agent(Enum):
    ASSISTANT_COACH = "assistant_coach"
    TACTICIAN = "tactician"
    SKILLS_COACH = "skills_coach"
    NUTRITIONIST = "nutritionist"
    STRENGTH_COACH = "strength_coach"
    ANALYST = "analyst"
    YOUTH_COACH = "youth_coach"
    TEAM_MANAGER = "team_manager"

AGENT_INFO = {
    Agent.ASSISTANT_COACH: {
        "name": "ASSISTANT COACH",
        "icon": "🎯",
        "title": "General Manager",
        "specialty": "Team Leadership & Strategy",
        "color": "#FF6B35"
    },
    Agent.TEAM_MANAGER: {
        "name": "TEAM MANAGER",
        "icon": "📋",
        "title": "Logistics Coordinator",
        "specialty": "Schedule, Players & Facilities",
        "color": "#9B59B6"
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

# ============================================================================
# ROUTER PROMPTS
# ============================================================================
ROUTER_PROMPT_WITH_CONTEXT = """You are a routing assistant for a basketball coaching app.

AGENTS AVAILABLE:
- TACTICIAN: ONLY for X's & O's, plays, offensive/defensive schemes, zones, ATOs, pick & roll, spacing, game strategy during play
- SKILLS_COACH: basketball drills, shooting technique, dribbling, footwork (ages 13+)
- NUTRITIONIST: food, diet, meals, nutrition, eating, supplements, meal plans
- STRENGTH_COACH: gym, strength, weights, jumping, speed, agility, workout programs
- ANALYST: statistics, data, numbers, turnovers, assists, percentages, efficiency, analytics
- YOUTH_COACH: kids, children, young players, ages 5-12, mini basketball, youth development
- TEAM_MANAGER: schedule, calendar, events, practices, games, facilities, venues, halls, players roster, parent contacts, phone numbers, logistics, transportation
- ASSISTANT_COACH: team management, practice planning, communication, leadership, motivation, player relationships, parent communication, team culture, administrative tasks, season planning, tryouts, roster management, team rules, handling conflicts

IMPORTANT DISTINCTIONS:
- "When is the next practice?" → TEAM_MANAGER
- "What's the schedule this week?" → TEAM_MANAGER
- "Give me the phone number of..." → TEAM_MANAGER
- "Where do we play on Friday?" → TEAM_MANAGER
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
3. If about SCHEDULE, CALENDAR, FACILITIES, PLAYER CONTACTS, LOGISTICS → TEAM_MANAGER
4. If about team MANAGEMENT, PLANNING, COMMUNICATION, LEADERSHIP → ASSISTANT_COACH
5. If about ON-COURT TACTICS, PLAYS, SCHEMES → TACTICIAN
6. Numbers, measurements, statistics responses are ALWAYS continuations → STAY with same agent
7. When in doubt → STAY with the same agent

Which agent should handle this? Answer with ONE word: TACTICIAN, SKILLS_COACH, NUTRITIONIST, STRENGTH_COACH, ANALYST, YOUTH_COACH, TEAM_MANAGER, or ASSISTANT_COACH"""


ROUTER_PROMPT_NO_CONTEXT = """Determine which coach should answer this basketball question.

AGENTS:
- TACTICIAN: ONLY for X's & O's, plays, offensive/defensive schemes, zones, ATOs, pick & roll, spacing, game strategy during play
- SKILLS_COACH: basketball drills, shooting technique, dribbling, footwork (ages 13+)
- NUTRITIONIST: food, diet, meals, nutrition, eating, supplements, meal plans
- STRENGTH_COACH: gym, strength, weights, jumping, speed, agility, workout programs
- ANALYST: statistics, data, numbers, turnovers, assists, percentages, efficiency, analytics
- YOUTH_COACH: kids, children, young players, ages 5-12, mini basketball, youth development
- TEAM_MANAGER: schedule, calendar, events, practices, games, facilities, venues, halls, players roster, parent contacts, phone numbers, logistics, transportation
- ASSISTANT_COACH: team management, practice planning, communication, leadership, motivation, player relationships, parent communication, team culture, administrative tasks, season planning, tryouts, roster management, team rules, handling conflicts

IMPORTANT DISTINCTIONS:
- "When is the next practice?" → TEAM_MANAGER
- "What's the schedule this week?" → TEAM_MANAGER
- "Give me the phone number of..." → TEAM_MANAGER
- "Where do we play on Friday?" → TEAM_MANAGER
- "How to run a practice" → ASSISTANT_COACH (not TACTICIAN)
- "How to manage players" → ASSISTANT_COACH (not TACTICIAN)
- "Team communication" → ASSISTANT_COACH
- "Season planning" → ASSISTANT_COACH
- "How to beat zone defense" → TACTICIAN
- "Pick and roll coverage" → TACTICIAN
- "Offensive sets" → TACTICIAN

Question: {question}

Answer with ONE word: TACTICIAN, SKILLS_COACH, NUTRITIONIST, STRENGTH_COACH, ANALYST, YOUTH_COACH, TEAM_MANAGER, or ASSISTANT_COACH"""

# ============================================================================
# LOGISTICS SETTINGS
# ============================================================================
EVENT_TYPES = ["practice", "game", "tournament", "meeting", "other"]
FACILITY_TYPES = ["gym", "outdoor", "fitness_room", "other"]
PLAYER_POSITIONS = ["Guard", "Forward", "Center"]
