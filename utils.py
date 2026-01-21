# -*- coding: utf-8 -*-
"""
HOOPS AI - Utilities
Database functions, file handling, and helper functions
"""

import streamlit as st
import base64
import pandas as pd
from openai import OpenAI
from supabase import create_client

from config import (
    Agent, AGENT_INFO,
    ROUTER_PROMPT_WITH_CONTEXT, ROUTER_PROMPT_NO_CONTEXT
)
from prompts import (
    SYSTEM_PROMPTS, COACH_PROFILE_TEMPLATE, RESPONSE_RULES,
    KNOWLEDGE_BASE_HEADER, KNOWLEDGE_BASE_FOOTER,
    FILE_ANALYSIS_PROMPT, IMAGE_ANALYSIS_PROMPT
)

# ============================================================================
# CLIENT INITIALIZATION
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

# ============================================================================
# DATABASE FUNCTIONS - COACHES
# ============================================================================
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
        if result.data:
            return result.data[0]
        return None
    except Exception:
        return None

# ============================================================================
# DATABASE FUNCTIONS - CONVERSATIONS
# ============================================================================
def get_coach_conversations(supabase, coach_id):
    """Get coach's conversation history"""
    try:
        result = supabase.table("conversations").select("*").eq("coach_id", coach_id).order("created_at", desc=True).limit(20).execute()
        return result.data or []
    except Exception:
        return []

def create_conversation(supabase, coach_id, title):
    """Create new conversation"""
    try:
        result = supabase.table("conversations").insert({
            "coach_id": coach_id,
            "title": title[:50] if title else "New Chat"
        }).execute()
        if result.data:
            return result.data[0]
        return None
    except Exception:
        return None

def save_message(supabase, conversation_id, role, content, agent=None):
    """Save message to conversation"""
    try:
        data = {
            "conversation_id": conversation_id,
            "role": role,
            "content": content
        }
        if agent:
            data["agent"] = agent
        supabase.table("messages").insert(data).execute()
    except Exception:
        pass

def get_conversation_messages(supabase, conversation_id):
    """Get all messages in a conversation"""
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

# ============================================================================
# DATABASE FUNCTIONS - COACH MEMORIES
# ============================================================================

# Triggers for auto-saving memories
MEMORY_TRIGGERS = {
    "time_based": [
        "לאימון", "מחר", "השבוע", "בשבוע הבא", "ביום", "לפני המשחק", "אחרי המשחק",
        "tomorrow", "next week", "for practice", "for the game", "this week", "next practice"
    ],
    "player_related": [
        "השחקן", "שחקן מספר", "הילד", "הבן שלי", "player", "my son", "my kid", "the player"
    ],
    "issues": [
        "מתקשה", "בעיה", "לא מצליח", "קושי", "חולשה", "צריך לשפר",
        "struggling", "problem", "issue", "weakness", "needs to improve", "difficulty"
    ],
    "goals": [
        "המטרה", "היעד", "רוצה להשיג", "לשפר", "goal", "objective", "want to achieve", "improve"
    ],
    "plans": [
        "תוכנית", "אסטרטגיה", "תכנון", "plan", "strategy", "program", "schedule"
    ],
    "positive_feedback": [
        "תודה", "מעולה", "בדיוק מה שצריך", "אשמור", "אני הולך ליישם",
        "thanks", "perfect", "exactly what I needed", "I'll use this", "great idea"
    ]
}

def get_coach_memories(supabase, coach_id, limit=10):
    """Get recent memories for a coach"""
    try:
        result = supabase.table("coach_memories")\
            .select("*")\
            .eq("coach_id", coach_id)\
            .eq("status", "active")\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        return result.data or []
    except Exception as e:
        print(f"Error getting memories: {e}")
        return []

def save_memory(supabase, coach_id, category, title, content, conversation_id=None, importance=1):
    """Save a new memory for a coach"""
    try:
        data = {
            "coach_id": coach_id,
            "category": category,
            "title": title[:100] if title else "Memory",
            "content": content[:500] if content else "",
            "importance": importance,
            "status": "active"
        }
        if conversation_id:
            data["conversation_id"] = conversation_id
        
        result = supabase.table("coach_memories").insert(data).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error saving memory: {e}")
        return None

def detect_memory_triggers(user_message, ai_response):
    """Detect if conversation should be saved to memory"""
    text_to_check = (user_message + " " + ai_response).lower()
    
    detected_triggers = []
    
    for trigger_type, keywords in MEMORY_TRIGGERS.items():
        for keyword in keywords:
            if keyword.lower() in text_to_check:
                detected_triggers.append(trigger_type)
                break
    
    return list(set(detected_triggers))

def is_exceptional_conversation(user_message, ai_response, message_count=1):
    """Check if conversation is exceptional and should be saved"""
    # Long response (detailed answer)
    if len(ai_response.split()) > 300:
        return True, "long_response"
    
    # Multiple back-and-forth (engaged conversation)
    if message_count > 4:
        return True, "engaged_conversation"
    
    # Response contains a list/plan (structured content)
    list_indicators = ["1.", "2.", "3.", "א.", "ב.", "•", "-  "]
    if sum(1 for ind in list_indicators if ind in ai_response) >= 3:
        return True, "structured_plan"
    
    return False, None

def extract_memory_title(user_message, category):
    """Extract a short title from the user's message"""
    # Take first 50 chars or first sentence
    title = user_message[:80]
    if "?" in title:
        title = title.split("?")[0] + "?"
    elif "." in title:
        title = title.split(".")[0]
    
    # Add category prefix
    category_prefixes = {
        "drill": "🏀 ",
        "issue": "⚠️ ",
        "goal": "🎯 ",
        "player": "👤 ",
        "tactic": "📋 ",
        "plan": "📅 ",
        "general": "💡 "
    }
    prefix = category_prefixes.get(category, "💡 ")
    
    return prefix + title.strip()

def determine_memory_category(triggers, user_message):
    """Determine the category of memory based on triggers"""
    if "player_related" in triggers:
        return "player"
    elif "issues" in triggers:
        return "issue"
    elif "goals" in triggers:
        return "goal"
    elif "plans" in triggers or "time_based" in triggers:
        return "plan"
    elif any(word in user_message.lower() for word in ["תרגיל", "drill", "exercise"]):
        return "drill"
    elif any(word in user_message.lower() for word in ["טקטיקה", "משחק", "הגנה", "התקפה", "tactic", "offense", "defense"]):
        return "tactic"
    else:
        return "general"

def process_memory_save(supabase, coach_id, user_message, ai_response, conversation_id=None, message_count=1):
    """Main function to decide if and what to save to memory"""
    # Check triggers
    triggers = detect_memory_triggers(user_message, ai_response)
    
    # Check if exceptional
    is_exceptional, exception_type = is_exceptional_conversation(user_message, ai_response, message_count)
    
    # Decide if we should save
    should_save = len(triggers) > 0 or is_exceptional
    
    if not should_save:
        return None
    
    # Determine category and importance
    category = determine_memory_category(triggers, user_message)
    importance = 2 if is_exceptional or len(triggers) > 1 else 1
    
    # Create title and content
    title = extract_memory_title(user_message, category)
    
    # Content is a summary: user question + key part of response
    response_summary = ai_response[:300] + "..." if len(ai_response) > 300 else ai_response
    content = f"שאלה: {user_message[:150]}\n\nתשובה: {response_summary}"
    
    # Save to database
    memory = save_memory(supabase, coach_id, category, title, content, conversation_id, importance)
    
    return memory

def build_memory_context(memories):
    """Build context string from memories for system prompt"""
    if not memories:
        return ""
    
    context = "\n\n=== COACH'S HISTORY - IMPORTANT CONTEXT ===\n"
    context += "The following are previous conversations and plans with this coach. Use this context to provide continuity:\n\n"
    
    for i, mem in enumerate(memories[:10], 1):
        created = mem.get('created_at', '')[:10]  # Just the date
        category = mem.get('category', 'general')
        title = mem.get('title', 'Memory')
        content = mem.get('content', '')[:200]
        
        context += f"{i}. [{created}] {title}\n"
        context += f"   {content}\n\n"
    
    context += "=== END OF HISTORY ===\n"
    context += "Use this history to:\n"
    context += "- Reference previous conversations when relevant\n"
    context += "- Ask about progress on previous plans/drills\n"
    context += "- Maintain continuity in coaching relationship\n"
    context += "- But don't force it - only mention if naturally relevant\n\n"
    
    return context

# ============================================================================
# DATABASE FUNCTIONS - DOCUMENTS (RAG)
# ============================================================================
def get_agent_documents(supabase, agent_name):
    """Get all documents for a specific agent"""
    try:
        result = supabase.table("documents").select("title, content").eq("agent", agent_name).execute()
        return result.data or []
    except Exception:
        return []

def get_agent_knowledge(supabase, agent):
    """Build knowledge context from agent's documents"""
    agent_name = agent.value
    documents = get_agent_documents(supabase, agent_name)
    
    if not documents:
        return ""
    
    knowledge = KNOWLEDGE_BASE_HEADER
    
    for doc in documents:
        knowledge += f"\n### {doc.get('title', 'Document')}\n"
        knowledge += f"{doc.get('content', '')}\n"
        knowledge += "-" * 30 + "\n"
    
    knowledge += KNOWLEDGE_BASE_FOOTER
    return knowledge

# ============================================================================
# PROMPT BUILDER
# ============================================================================
def get_system_prompt(agent, coach_profile=None):
    """Generate complete system prompt for an agent"""
    prompt = SYSTEM_PROMPTS[agent]
    
    # Add coach profile context
    if coach_profile:
        prompt += COACH_PROFILE_TEMPLATE.format(
            name=coach_profile.get('name', 'Unknown'),
            team_name=coach_profile.get('team_name', 'Unknown'),
            age_group=coach_profile.get('age_group', 'Unknown'),
            level=coach_profile.get('level', 'Unknown')
        )
    
    # Add response rules
    prompt += RESPONSE_RULES
    
    return prompt

# ============================================================================
# ROUTING
# ============================================================================
def route_question(question, client, chat_history=None):
    """Route question to appropriate agent with smart context awareness"""
    try:
        previous_agent = None
        previous_message = None
        
        if chat_history and len(chat_history) >= 1:
            for msg in reversed(chat_history):
                if msg.get("role") == "assistant" and msg.get("agent"):
                    previous_agent = msg.get("agent")
                    previous_message = msg.get("raw_content", msg.get("content", ""))[:300]
                    break
        
        # Smart continuation check
        if previous_agent and previous_message:
            has_question = "?" in previous_message or any(word in previous_message.lower() for word in 
                ["please provide", "tell me", "what is", "how much", "how many", "ספר לי", "מה", "כמה", "איזה", "אנא"])
            
            is_data_response = (
                len(question) < 200 or
                any(char.isdigit() for char in question) or
                question.strip().startswith(("גיל", "משקל", "גובה", "age", "weight", "height", "כן", "לא", "yes", "no"))
            )
            
            if has_question and is_data_response:
                for agent in Agent:
                    if agent.value == previous_agent:
                        return agent
        
        # Use Router
        if previous_agent and previous_message:
            prompt = ROUTER_PROMPT_WITH_CONTEXT.format(
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
        elif "TEAM_MANAGER" in result or "MANAGER" in result:
            return Agent.TEAM_MANAGER
        return Agent.ASSISTANT_COACH
    except Exception:
        return Agent.ASSISTANT_COACH

# ============================================================================
# AGENT RESPONSE
# ============================================================================
def get_agent_response(question, agent, chat_history, client, coach_profile=None, supabase=None, image_data=None):
    """Get response from specific agent with RAG knowledge, memories, and optional image"""
    try:
        system_prompt = get_system_prompt(agent, coach_profile)
        
        # Add coach memories for context
        if supabase and coach_profile:
            memories = get_coach_memories(supabase, coach_profile.get('id'), limit=10)
            if memories:
                memory_context = build_memory_context(memories)
                system_prompt += memory_context
        
        # Add RAG knowledge
        if supabase:
            knowledge = get_agent_knowledge(supabase, agent)
            if knowledge:
                system_prompt += knowledge
        
        # Add logistics context for Team Manager
        if agent == Agent.TEAM_MANAGER and supabase and coach_profile:
            logistics_context = get_logistics_context(supabase, coach_profile.get('id'))
            system_prompt += logistics_context
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add recent history
        if chat_history:
            for msg in chat_history[-4:]:
                role = "user" if msg["role"] == "user" else "assistant"
                content = msg.get("raw_content", msg["content"])
                messages.append({"role": role, "content": content})
        
        # Handle image
        if image_data:
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{image_data['mime_type']};base64,{image_data['data']}"
                        }
                    }
                ]
            })
            model = "gpt-4o"
        else:
            messages.append({"role": "user", "content": question})
            model = "gpt-4o-mini"
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# ============================================================================
# RESPONSE FORMATTING
# ============================================================================
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
# FILE HANDLING
# ============================================================================
def read_uploaded_file(uploaded_file):
    """Read and process uploaded file, return content and type"""
    file_name = uploaded_file.name.lower()
    
    # Image files
    if file_name.endswith(('.png', '.jpg', '.jpeg', '.webp')):
        file_bytes = uploaded_file.getvalue()
        image_data = base64.b64encode(file_bytes).decode('utf-8')
        
        if file_name.endswith('.png'):
            mime_type = "image/png"
        elif file_name.endswith('.webp'):
            mime_type = "image/webp"
        else:
            mime_type = "image/jpeg"
        
        return {
            "type": "image",
            "data": image_data,
            "mime_type": mime_type
        }
    
    # CSV files
    elif file_name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        return {
            "type": "data",
            "content": df.to_string()
        }
    
    # Excel files
    elif file_name.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(uploaded_file)
        return {
            "type": "data",
            "content": df.to_string()
        }
    
    # Text files
    else:
        content = uploaded_file.read().decode('utf-8')
        return {
            "type": "data",
            "content": content
        }

def build_analysis_prompt(file_result, analysis_type):
    """Build the appropriate analysis prompt based on file type"""
    if file_result["type"] == "image":
        return IMAGE_ANALYSIS_PROMPT.format(analysis_type=analysis_type)
    else:
        return FILE_ANALYSIS_PROMPT.format(
            analysis_type=analysis_type,
            file_content=file_result["content"]
        )

# ============================================================================
# LOGISTICS - FACILITIES
# ============================================================================
def get_facilities(supabase, coach_id):
    """Get all facilities for a coach"""
    try:
        result = supabase.table("facilities").select("*").eq("coach_id", coach_id).order("name").execute()
        return result.data or []
    except Exception:
        return []

def get_facility_by_id(supabase, facility_id):
    """Get a single facility by ID"""
    try:
        result = supabase.table("facilities").select("*").eq("id", facility_id).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None

def create_facility(supabase, coach_id, data):
    """Create a new facility"""
    try:
        data["coach_id"] = coach_id
        result = supabase.table("facilities").insert(data).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None

def update_facility(supabase, facility_id, data):
    """Update a facility"""
    try:
        result = supabase.table("facilities").update(data).eq("id", facility_id).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None

def delete_facility(supabase, facility_id):
    """Delete a facility"""
    try:
        supabase.table("facilities").delete().eq("id", facility_id).execute()
        return True
    except Exception:
        return False

# ============================================================================
# LOGISTICS - EVENTS
# ============================================================================
def get_events(supabase, coach_id, start_date=None, end_date=None):
    """Get events for a coach, optionally filtered by date range"""
    try:
        query = supabase.table("events").select("*, facilities(name, address)").eq("coach_id", coach_id)
        if start_date:
            query = query.gte("event_date", start_date)
        if end_date:
            query = query.lte("event_date", end_date)
        result = query.order("event_date").order("time_start").execute()
        return result.data or []
    except Exception:
        return []

def get_events_for_month(supabase, coach_id, year, month):
    """Get all events for a specific month"""
    from datetime import date
    import calendar
    
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    
    return get_events(supabase, coach_id, first_day.isoformat(), last_day.isoformat())

def get_event_by_id(supabase, event_id):
    """Get a single event by ID"""
    try:
        result = supabase.table("events").select("*, facilities(name, address)").eq("id", event_id).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None

def create_event(supabase, coach_id, data):
    """Create a new event"""
    try:
        data["coach_id"] = coach_id
        result = supabase.table("events").insert(data).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None

def update_event(supabase, event_id, data):
    """Update an event"""
    try:
        result = supabase.table("events").update(data).eq("id", event_id).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None

def delete_event(supabase, event_id):
    """Delete an event"""
    try:
        supabase.table("events").delete().eq("id", event_id).execute()
        return True
    except Exception:
        return False

# ============================================================================
# LOGISTICS - PLAYERS
# ============================================================================
def get_players(supabase, coach_id, active_only=True):
    """Get all players for a coach"""
    try:
        query = supabase.table("players").select("*").eq("coach_id", coach_id)
        if active_only:
            query = query.eq("is_active", True)
        result = query.order("jersey_number").order("last_name").execute()
        return result.data or []
    except Exception:
        return []

def get_player_by_id(supabase, player_id):
    """Get a single player by ID"""
    try:
        result = supabase.table("players").select("*").eq("id", player_id).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None

def create_player(supabase, coach_id, data):
    """Create a new player"""
    try:
        data["coach_id"] = coach_id
        result = supabase.table("players").insert(data).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None

def update_player(supabase, player_id, data):
    """Update a player"""
    try:
        result = supabase.table("players").update(data).eq("id", player_id).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None

def delete_player(supabase, player_id):
    """Delete (deactivate) a player"""
    try:
        supabase.table("players").update({"is_active": False}).eq("id", player_id).execute()
        return True
    except Exception:
        return False

# ============================================================================
# LOGISTICS - DATA FOR TEAM MANAGER AGENT
# ============================================================================
def get_logistics_context(supabase, coach_id):
    """Get all logistics data formatted for the Team Manager agent"""
    from datetime import date, timedelta
    
    # Get upcoming events (next 30 days)
    today = date.today()
    end_date = today + timedelta(days=30)
    events = get_events(supabase, coach_id, today.isoformat(), end_date.isoformat())
    
    # Get all facilities
    facilities = get_facilities(supabase, coach_id)
    
    # Get all active players
    players = get_players(supabase, coach_id, active_only=True)
    
    # Format context
    context = "\n\n=== TEAM LOGISTICS DATA ===\n"
    
    # Events
    context += "\n📅 UPCOMING EVENTS (Next 30 days):\n"
    if events:
        for e in events:
            facility_name = e.get('facilities', {}).get('name', 'TBD') if e.get('facilities') else 'TBD'
            context += f"- {e['event_date']} | {e.get('time_start', 'TBD')} | {e['type'].upper()}: {e['title']}"
            if e.get('opponent'):
                context += f" vs {e['opponent']}"
            context += f" @ {facility_name}\n"
    else:
        context += "No upcoming events scheduled.\n"
    
    # Facilities
    context += "\n🏟️ FACILITIES:\n"
    if facilities:
        for f in facilities:
            context += f"- {f['name']}"
            if f.get('address'):
                context += f" | {f['address']}"
            if f.get('contact_phone'):
                context += f" | Contact: {f.get('contact_name', 'N/A')} ({f['contact_phone']})"
            context += "\n"
    else:
        context += "No facilities registered.\n"
    
    # Players
    context += "\n👥 PLAYERS ROSTER:\n"
    if players:
        for p in players:
            context += f"- #{p.get('jersey_number', 'N/A')} {p['first_name']} {p['last_name']}"
            if p.get('position'):
                context += f" ({p['position']})"
            if p.get('parent1_name') and p.get('parent1_phone'):
                context += f" | Parent: {p['parent1_name']} - {p['parent1_phone']}"
            context += "\n"
    else:
        context += "No players registered.\n"
    
    context += "\n=== END LOGISTICS DATA ===\n"
    
    return context