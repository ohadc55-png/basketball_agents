# HOOPS AI - Codebase Documentation

## Overview
HOOPS AI is a Streamlit-based basketball coaching assistant application with AI-powered features.
The app provides coaches with an intelligent multi-agent system, team management tools, drill libraries, and practice planning capabilities.

**Last Updated:** February 2026
**Recent Changes:** Complete visual redesign with warm dark theme

---

## Project Structure

```
hoops_ai_complete/
├── app.py                    # Main application entry point
├── config.py                 # Configuration, constants, agent definitions
├── styles.py                 # CSS styling (Modern warm dark theme)
├── utils.py                  # Database operations & utility functions
├── prompts.py                # AI system prompts for each agent
├── logistics.py              # Calendar, facilities, players management
├── analytics_viz.py          # Charts and visualizations for statistics
├── requirements.txt          # Python dependencies
├── favicon.png               # App icon
│
├── components/
│   ├── __init__.py
│   ├── drill_card.py         # Drill card UI component
│   └── timeline.py           # Practice timeline UI component
│
└── pages/
    ├── __init__.py
    ├── drill_library.py      # Drill library page
    └── practice_planner.py   # Practice session planner page
```

---

## Core Files Description

### 1. `app.py` - Main Application
The entry point that orchestrates the entire application.

**Key Functions:**
- `render_login_page()` - Login/Registration UI
- `render_sidebar()` - Navigation sidebar with:
  - Logo & profile info
  - Navigation buttons (CHAT, PLAN, DRILLS, TEAM)
  - Quick Ideas dropdown
  - Recent chats history
  - Coaching staff cards
- `render_header()` - Hero header section
- `render_welcome()` - Welcome banner for new sessions
- `render_file_upload()` - File upload for stats analysis
- `render_chat()` - Main chat interface with AI agents
- `main()` - Page routing between chat/planner/library/logistics

**Session State Variables:**
- `logged_in` - Authentication status
- `coach` - Current coach profile
- `messages` - Chat history
- `current_conversation` - Active conversation
- `current_page` - Current view (chat/planner/library/logistics)
- `show_file_upload` - File upload modal visibility
- `pending_prompt` - Quick idea prompt to process

---

### 2. `config.py` - Configuration
Contains all constants and configurations.

**Settings:**
- `APP_TITLE`, `APP_ICON`, `LOGO_URL`, `BACKGROUND_URL`
- `AGE_GROUPS`: ["U10", "U12", "U14", "U16", "U18", "Senior"]
- `LEVELS`: ["Beginner", "League", "Competitive", "Professional"]
- `ALLOWED_FILE_TYPES`: csv, xlsx, xls, txt, png, jpg, jpeg, webp

**AI Agents (Enum):**
```python
Agent.ASSISTANT_COACH  # Team Leadership & Strategy
Agent.TEAM_MANAGER     # Schedule, Players & Facilities
Agent.TACTICIAN        # X's & O's Expert
Agent.SKILLS_COACH     # Training & Drills
Agent.NUTRITIONIST     # Diet Plans
Agent.STRENGTH_COACH   # Athletic Performance
Agent.ANALYST          # Performance Analytics
Agent.YOUTH_COACH      # Ages 5-12 Specialist
```

**Drill Settings:**
- Categories: offense, defense, shooting, ball_handling, passing, conditioning, warmup, cooldown
- Difficulties: beginner, intermediate, advanced

**Segment Types (for practice planner):**
- warmup, drill, scrimmage, cooldown, break, film

---

### 3. `styles.py` - CSS Styling
Modern warm dark theme with Space Grotesk font.

**Color Palette:**
```css
--primary: #f48c25          /* Warm amber orange */
--primary-light: #ffa94d
--bg-dark: #181411          /* Warm dark brown background */
--bg-surface: #221910       /* Card/surface background */
--border-dark: #393028      /* Border color */
--text-primary: #FFFFFF
--text-secondary: #baab9c
--text-muted: #7a6f63
```

**Key CSS Classes:**
- `.scoreboard`, `.hero-title`, `.hero-subtitle` - Header styles
- `.welcome-banner`, `.welcome-title`, `.welcome-text` - Welcome section
- `.drill-card`, `.drill-card-title`, `.drill-tag` - Drill cards
- `.timeline-segment`, `.segment-time`, `.segment-title` - Timeline
- `.page-header`, `.page-title`, `.page-subtitle` - Page headers
- `.stat-card`, `.stat-value`, `.stat-label` - Statistics cards
- `.filter-chip`, `.ai-chip` - Chips/tags
- `.agent-card` - Coaching staff cards in sidebar

---

### 4. `utils.py` - Database & Utilities
All database operations and helper functions.

**Database Tables (Supabase):**
1. `coaches` - Coach profiles (name, email, team_name, age_group, level)
2. `conversations` - Chat conversations (coach_id, title)
3. `messages` - Chat messages (conversation_id, role, content, agent)
4. `coach_memories` - Saved memories/notes for each coach
5. `events` - Calendar events (date, type, title, opponent, etc.)
6. `facilities` - Facilities/venues (name, type, address, capacity)
7. `players` - Player roster (name, position, jersey_number, parent_phone)
8. `drills` - Drill library (title, description, category, difficulty, etc.)
9. `practice_sessions` - Practice sessions (date, title, focus, notes)
10. `session_segments` - Timeline segments for each session

**Key Functions:**
- `get_supabase_client()`, `get_openai_client()` - Client initialization
- `get_coach_by_email()`, `create_coach()` - Coach management
- `get_coach_conversations()`, `create_conversation()`, `save_message()` - Chat
- `route_question()` - AI agent routing
- `get_agent_response()` - Get response from specific agent
- `format_response()` - Format agent response with badge
- `read_uploaded_file()` - Handle file uploads (CSV, Excel, images)
- CRUD operations for events, facilities, players, drills, sessions, segments

---

### 5. `logistics.py` - Team Management
Calendar, facilities, and players management UI.

**Features:**
- `render_calendar()` - Monthly calendar with events
- `render_event_details()` - Event viewer/editor
- `render_facilities_manager()` - Facilities CRUD
- `render_players_manager()` - Player roster CRUD
- `render_logistics_page()` - Main tabs interface

**Event Types:** practice, game, tournament, meeting, other
**Facility Types:** gym, outdoor, fitness_room, other
**Player Positions:** Guard, Forward, Center

---

### 6. `analytics_viz.py` - Visualizations
Charts for THE ANALYST agent.

**Chart Types:**
- `create_bar_chart()` - Horizontal bar comparison
- `create_pie_chart()` - Distribution pie chart
- `create_shooting_chart()` - Shooting percentages
- `create_player_comparison()` - Multi-metric comparison
- `create_performance_trend()` - Time-based trend line
- `extract_stats_from_text()` - Extract numbers from user input
- `display_analytics()` - Auto-generate relevant charts

---

### 7. `components/drill_card.py` - Drill Card Component
Reusable card for displaying drills.

**Functions:**
- `render_drill_card(drill, on_add_to_session, on_edit, on_delete, show_actions)`
- `render_drill_card_mini(drill)` - Compact version for sidebars

**Displays:** Title, description, category icon, difficulty tag, duration, AI badge

---

### 8. `components/timeline.py` - Timeline Component
Visual timeline for practice sessions.

**Functions:**
- `render_segment(segment, index, total_segments, callbacks)`
- `render_timeline(segments, callbacks)` - Full timeline with stats
- `render_timeline_summary(segments)` - Compact summary view

---

### 9. `pages/drill_library.py` - Drill Library Page
Browse, create, and manage basketball drills.

**Features:**
- Search and filter drills
- Create manual drills
- AI drill generator
- Grid display with drill cards
- Statistics (total drills, AI generated, categories)

---

### 10. `pages/practice_planner.py` - Practice Planner Page
Create and organize practice sessions with visual timeline.

**Features:**
- Session list sidebar
- Session editor with form
- Visual timeline builder
- Add drills from library
- AI session generator
- Segment reordering and editing

---

## Database Schema (Supabase)

### coaches
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| name | text | Coach name |
| email | text | Email (unique) |
| team_name | text | Team name |
| age_group | text | U10-Senior |
| level | text | Skill level |
| created_at | timestamp | Creation date |

### conversations
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| coach_id | uuid | FK to coaches |
| title | text | Conversation title |
| created_at | timestamp | Creation date |

### messages
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| conversation_id | uuid | FK to conversations |
| role | text | user/assistant |
| content | text | Message content |
| agent | text | Which AI agent responded |
| created_at | timestamp | Creation date |

### drills
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| coach_id | uuid | FK to coaches |
| title | text | Drill name |
| description | text | Description |
| category | text | offense/defense/etc |
| difficulty | text | beginner/intermediate/advanced |
| duration_minutes | int | Duration |
| instructions | text | Step-by-step instructions |
| coaching_points | jsonb | Array of key points |
| tags | jsonb | Array of tags |
| is_ai_generated | boolean | Created by AI? |
| created_at | timestamp | Creation date |

### practice_sessions
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| coach_id | uuid | FK to coaches |
| date | date | Session date |
| title | text | Session title |
| focus | text | Main focus area |
| notes | text | Additional notes |
| total_duration | int | Total minutes |
| is_ai_generated | boolean | Created by AI? |
| created_at | timestamp | Creation date |

### session_segments
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| session_id | uuid | FK to practice_sessions |
| drill_id | uuid | FK to drills (optional) |
| segment_type | text | warmup/drill/scrimmage/etc |
| title | text | Segment title |
| duration_minutes | int | Duration |
| notes | text | Notes |
| order_index | int | Position in timeline |
| created_at | timestamp | Creation date |

---

## Dependencies (requirements.txt)

```
streamlit>=1.28.0
openai>=1.0.0
supabase>=2.0.0
pandas>=2.0.0
openpyxl>=3.0.0
plotly>=5.18.0
```

---

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

**Required Secrets (.streamlit/secrets.toml):**
```toml
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-anon-key"
OPENAI_API_KEY = "your-openai-api-key"
```

---

## Recent Visual Upgrade (February 2026)

### Changes Made:
1. **Color Scheme:** Changed from `#FF6B35` to warm amber `#f48c25`
2. **Background:** Warm dark browns (#181411, #221910) instead of pure blacks
3. **Font:** Space Grotesk instead of Orbitron/Rajdhani
4. **Borders:** Softer warm borders (#393028)
5. **Text:** Warm secondary colors (#baab9c, #7a6f63)
6. **Effects:** Subtle hover transitions, cleaner shadows

### Files Modified:
- `styles.py` - Complete CSS rewrite
- `app.py` - Inline style updates
- `config.py` - Color constants
- `logistics.py` - Inline style updates
- `analytics_viz.py` - Chart colors
- `components/drill_card.py` - Card styling
- `components/timeline.py` - Timeline colors

---

## Current Status

### Completed Features:
- [x] Multi-agent AI chat system
- [x] Coach registration/login
- [x] Conversation history
- [x] File upload analysis (CSV, Excel, Images)
- [x] Team calendar
- [x] Facilities management
- [x] Players roster
- [x] Drill library with CRUD
- [x] AI drill generator
- [x] Practice planner with timeline
- [x] Analytics visualizations
- [x] Modern warm dark theme
- [x] Mobile responsive design
- [x] Hebrew + English support

### Potential Future Enhancements:
- [ ] Team statistics dashboard
- [ ] Season planning view
- [ ] Export practice plans to PDF
- [ ] Share drills between coaches
- [ ] Video analysis integration
- [ ] Player performance tracking
- [ ] Parent communication portal

---

## Contact & Support
This documentation was generated to help maintain context across development sessions.
