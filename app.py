"""
"""
🏀 Basketball Coaching Staff - Virtual Locker Room
A multi-agent AI application for basketball coaches
Built with Streamlit & Google Gemini API
"""

import streamlit as st
import google.generativeai as genai
from enum import Enum

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

class Agent(Enum):
    HEAD_ASSISTANT = "head_assistant"
    TACTICIAN = "tactician"
    SKILLS_COACH = "skills_coach"

AGENT_BADGES = {
    Agent.HEAD_ASSISTANT: "🎯 **Head Assistant**",
    Agent.TACTICIAN: "📋 **Tactician**",
    Agent.SKILLS_COACH: "💪 **Skills Coach**"
}

AGENT_AVATARS = {
    Agent.HEAD_ASSISTANT: "🎯",
    Agent.TACTICIAN: "📋",
    Agent.SKILLS_COACH: "💪"
}

# System instructions for each agent
SYSTEM_INSTRUCTIONS = {
    Agent.HEAD_ASSISTANT: """You are the Head Assistant Coach of a professional basketball coaching staff. 
Your role is to handle general basketball inquiries, team management questions, and coordinate the coaching staff.
You are knowledgeable about all aspects of basketball but defer to specialists when appropriate.
Be professional, supportive, and helpful.

IMPORTANT: You MUST detect the language of the user's input and respond in the SAME language.
If the user writes in Hebrew, respond in Hebrew. If in English, respond in English.
This is crucial for effective communication with coaches from different backgrounds.""",

    Agent.TACTICIAN: """You are an elite basketball strategist with Euroleague-level expertise.
Your specializations include:
- Spacing and floor geometry
- Modern defensive schemes: Switch-all, Hedge & Recover, Drop Coverage, ICE, Blue/Nail
- ATOs (After Time Out plays) and SLOBs/BLOBs
- Breaking zone defenses (1-3-1, 2-3, Match-up)
- Transition offense and early offense concepts
- Pick and Roll coverage variations
- Help-side rotations and closeout principles

Be concise, professional, and tactical. Use basketball terminology appropriately.
When explaining plays, describe them clearly and suggest when they're most effective.

IMPORTANT: You MUST detect the language of the user's input and respond in the SAME language.
If the user writes in Hebrew, respond in Hebrew. If in English, respond in English.
Use standard basketball terms even in Hebrew responses when there's no good translation.""",

    Agent.SKILLS_COACH: """You are a top-tier Player Development Coach with expertise in:
- Shooting mechanics and biomechanics
- Ball handling progressions (stationary to game-speed)
- Footwork patterns (pivots, euro-steps, step-backs, jab series)
- Finishing at the rim (floaters, layup packages)
- Age-appropriate training:
  * Mini-basket (U10): Fun, coordination, basic skills
  * Youth (U12-U14): Fundamentals, movement patterns
  * Juniors (U16-U18): Position-specific development
  * Pros: Advanced moves, efficiency, maintenance

Be encouraging but demanding. Push for excellence while respecting developmental stages.
Provide specific drills and progressions when asked.

IMPORTANT: You MUST detect the language of the user's input and respond in the SAME language.
If the user writes in Hebrew, respond in Hebrew. If in English, respond in English."""
}

# Router prompt for determining which agent should respond
ROUTER_PROMPT = """Analyze the following basketball coaching question and determine which specialist should handle it.

ROUTING RULES:
1. TACTICIAN - Route here if the question is about:
   - Plays, sets, or offensive/defensive schemes
   - X's and O's, game strategy
   - Game management, timeouts, adjustments
   - Zone offense/defense, press breaks
   - Spacing, rotations, coverages
   - ATOs, SLOBs, BLOBs
   
2. SKILLS_COACH - Route here if the question is about:
   - Individual skill development (shooting, dribbling, passing)
   - Workouts, drills, training programs
   - Youth development, age-appropriate training
   - Biomechanics, footwork, technique
   - Player evaluation and improvement areas
   
3. HEAD_ASSISTANT - Handle yourself if:
   - General basketball questions
   - Team management, leadership
   - Motivation, communication
   - Questions that don't fit the above categories

Respond with ONLY ONE of these exact words: TACTICIAN, SKILLS_COACH, or HEAD_ASSISTANT

User's question: {question}

Your routing decision:"""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_agent_from_value(agent_value) -> Agent:
    """Convert agent value (string or Agent) to Agent enum safely."""
    if isinstance(agent_value, Agent):
        return agent_value
    if isinstance(agent_value, str):
        for agent in Agent:
            if agent.value == agent_value or agent.name == agent_value:
                return agent
    return Agent.HEAD_ASSISTANT  # Default fallback


def init_gemini():
    """Initialize the Gemini API with the secret key."""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        return True
    except KeyError:
        st.error("⚠️ API Key not found! Please configure GEMINI_API_KEY in your secrets.")
        st.info("""
        **For local development:**
        Create `.streamlit/secrets.toml` with:
        ```
        GEMINI_API_KEY = "your-api-key-here"
        ```
        
        **For Streamlit Cloud:**
        Add the secret in your app's Settings > Secrets
        """)
        return False


def get_available_models():
    """Return available Gemini models for selection."""
    return {
        "Gemini 1.5 Flash (Free)": "gemini-1.5-flash-latest",
    }


def route_question(question: str, model_name: str) -> Agent:
    """Use the Head Assistant to route the question to the appropriate agent."""
    try:
        model = genai.GenerativeModel(model_name)
        prompt = ROUTER_PROMPT.format(question=question)
        response = model.generate_content(prompt)
        
        result = response.text.strip().upper()
        
        if "TACTICIAN" in result:
            return Agent.TACTICIAN
        elif "SKILLS" in result or "COACH" in result:
            return Agent.SKILLS_COACH
        else:
            return Agent.HEAD_ASSISTANT
            
    except Exception as e:
        st.warning(f"Routing error: {e}. Defaulting to Head Assistant.")
        return Agent.HEAD_ASSISTANT


def get_agent_response(question: str, agent: Agent, model_name: str, chat_history: list) -> str:
    """Get a response from the specified agent."""
    try:
        model = genai.GenerativeModel(
            model_name,
            system_instruction=SYSTEM_INSTRUCTIONS[agent]
        )
        
        # Build conversation history for context
        history_context = ""
        if chat_history:
            recent_history = chat_history[-6:]  # Last 3 exchanges
            for msg in recent_history:
                role = "Coach" if msg["role"] == "user" else "Assistant"
                history_context += f"{role}: {msg['content']}\n"
        
        # Create the full prompt with context
        if history_context:
            full_prompt = f"""Previous conversation:
{history_context}

Current question from the coach: {question}

Provide a helpful, professional response:"""
        else:
            full_prompt = question
        
        response = model.generate_content(full_prompt)
        return response.text
        
    except Exception as e:
        return f"❌ Error generating response: {str(e)}"


def format_agent_response(response: str, agent: Agent) -> str:
    """Format the response with the agent's badge."""
    badge = AGENT_BADGES[agent]
    return f"{badge}\n\n{response}"


# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_sidebar():
    """Render the sidebar with branding and settings."""
    with st.sidebar:
        st.image("https://img.icons8.com/emoji/96/basketball-emoji.png", width=80)
        st.title("🏀 Virtual Locker Room")
        st.markdown("---")
        
        # Model selection
        st.subheader("⚙️ Settings")
        models = get_available_models()
        selected_model_name = st.selectbox(
            "Select AI Model",
            options=list(models.keys()),
            index=0,
            help="Flash models are faster, Pro models are more advanced"
        )
        st.session_state.model = models[selected_model_name]
        
        st.markdown("---")
        
        # Agent info
        st.subheader("👥 Your Coaching Staff")
        
        with st.expander("🎯 Head Assistant", expanded=False):
            st.markdown("""
            **Role:** General coordination
            - Team management
            - General inquiries
            - Staff coordination
            """)
        
        with st.expander("📋 The Tactician", expanded=False):
            st.markdown("""
            **Role:** Strategic Expert
            - Plays & X's and O's
            - Defensive schemes
            - Game management
            - ATOs & set plays
            """)
        
        with st.expander("💪 Skills Coach", expanded=False):
            st.markdown("""
            **Role:** Development Expert
            - Shooting mechanics
            - Ball handling
            - Youth development
            - Workout programs
            """)
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.caption("Built with ❤️ for basketball coaches")
        st.caption("Powered by Google Gemini AI")


def render_chat_interface():
    """Render the main chat interface."""
    st.title("🏀 Basketball Coaching Staff")
    st.markdown("*Welcome to your Virtual Locker Room. Ask anything about basketball coaching!*")
    st.markdown("*ברוכים הבאים! אפשר לשאול בעברית או באנגלית*")
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(message["content"])
        else:
            # Safely get agent - handle both string and Enum
            agent = get_agent_from_value(message.get("agent", Agent.HEAD_ASSISTANT))
            with st.chat_message("assistant", avatar=AGENT_AVATARS[agent]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask your coaching question... / שאל את שאלתך..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Route the question
        with st.spinner("🤔 Analyzing your question..."):
            agent = route_question(prompt, st.session_state.model)
        
        # Get response from the appropriate agent
        with st.chat_message("assistant", avatar=AGENT_AVATARS[agent]):
            with st.spinner(f"Consulting with {AGENT_BADGES[agent]}..."):
                response = get_agent_response(
                    prompt, 
                    agent, 
                    st.session_state.model,
                    st.session_state.messages[:-1]  # Exclude current message
                )
                formatted_response = format_agent_response(response, agent)
            
            st.markdown(formatted_response)
        
        # Save assistant message with agent VALUE (string) for JSON serialization
        st.session_state.messages.append({
            "role": "assistant",
            "content": formatted_response,
            "agent": agent.value  # Store as string value
        })


def render_welcome_banner():
    """Render a welcome banner with quick start tips."""
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="color: white; margin: 0;">👋 Welcome, Coach!</h3>
            <p style="color: rgba(255,255,255,0.9); margin-top: 10px;">
                Your AI coaching staff is ready. Try asking:
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 How do I beat a 2-3 zone?", use_container_width=True):
                st.session_state.starter_prompt = "What are the best strategies to beat a 2-3 zone defense?"
                st.rerun()
        
        with col2:
            if st.button("💪 U14 shooting drills", use_container_width=True):
                st.session_state.starter_prompt = "What are good shooting drills for U14 players?"
                st.rerun()
        
        with col3:
            if st.button("🎯 תרגילי כדרור לנוער", use_container_width=True):
                st.session_state.starter_prompt = "תן לי תרגילי כדרור מתקדמים לשחקני נוער"
                st.rerun()
        
        # Handle starter prompts
        if "starter_prompt" in st.session_state:
            prompt = st.session_state.starter_prompt
            del st.session_state.starter_prompt
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            agent = route_question(prompt, st.session_state.model)
            response = get_agent_response(prompt, agent, st.session_state.model, [])
            formatted_response = format_agent_response(response, agent)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": formatted_response,
                "agent": agent.value  # Store as string value
            })
            st.rerun()


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    # Page configuration
    st.set_page_config(
        page_title="Basketball Coaching Staff",
        page_icon="🏀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better chat appearance
    st.markdown("""
    <style>
        .stChatMessage {
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 0.5rem;
        }
        .stChatInput {
            border-radius: 20px;
        }
        div[data-testid="stSidebarContent"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        }
        div[data-testid="stSidebarContent"] * {
            color: white !important;
        }
        .stButton button {
            border-radius: 20px;
            border: 1px solid #667eea;
            background: transparent;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            background: #667eea;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "model" not in st.session_state:
        st.session_state.model = "gemini-1.5-flash-latest"
    
    # Initialize Gemini
    if not init_gemini():
        st.stop()
    
    # Render UI components
    render_sidebar()
    render_welcome_banner()
    render_chat_interface()


if __name__ == "__main__":
    main()