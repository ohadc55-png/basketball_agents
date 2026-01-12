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
        return Agent.ASSISTANT_COACH
    except Exception:
        return Agent.ASSISTANT_COACH

# ============================================================================
# AGENT RESPONSE
# ============================================================================
def get_agent_response(question, agent, chat_history, client, coach_profile=None, supabase=None, image_data=None):
    """Get response from specific agent with RAG knowledge and optional image"""
    try:
        system_prompt = get_system_prompt(agent, coach_profile)
        
        # Add RAG knowledge
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
