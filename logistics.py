# -*- coding: utf-8 -*-
"""
HOOPS AI - Logistics Module
Calendar, Facilities, and Players Management UI
"""

import streamlit as st
from datetime import date, datetime, timedelta
import calendar

from config import EVENT_TYPES, FACILITY_TYPES, PLAYER_POSITIONS
from utils import (
    get_events, get_events_for_month, get_event_by_id, create_event, update_event, delete_event,
    get_facilities, get_facility_by_id, create_facility, update_facility, delete_facility,
    get_players, get_player_by_id, create_player, update_player, delete_player
)

# ============================================================================
# CALENDAR VIEW
# ============================================================================
def render_calendar(supabase, coach_id):
    """Render monthly calendar with events"""
    
    # Month navigation
    if 'calendar_date' not in st.session_state:
        st.session_state.calendar_date = date.today()
    
    current_date = st.session_state.calendar_date
    
    # Header with navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("◀ Previous", key="cal_prev", use_container_width=True):
            # Go to previous month
            if current_date.month == 1:
                st.session_state.calendar_date = current_date.replace(year=current_date.year - 1, month=12, day=1)
            else:
                st.session_state.calendar_date = current_date.replace(month=current_date.month - 1, day=1)
            st.rerun()
    
    with col2:
        month_name = current_date.strftime("%B %Y")
        st.markdown(f'''
        <div style="text-align:center; font-family:'Orbitron',monospace; font-size:1.5rem; color:#FF6B35; padding:0.5rem;">
            📅 {month_name}
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        if st.button("Next ▶", key="cal_next", use_container_width=True):
            # Go to next month
            if current_date.month == 12:
                st.session_state.calendar_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
            else:
                st.session_state.calendar_date = current_date.replace(month=current_date.month + 1, day=1)
            st.rerun()
    
    # Get events for the month
    events = get_events_for_month(supabase, coach_id, current_date.year, current_date.month)
    
    # Create events dictionary by date
    events_by_date = {}
    for event in events:
        event_date = event['event_date']
        if event_date not in events_by_date:
            events_by_date[event_date] = []
        events_by_date[event_date].append(event)
    
    # Calendar grid
    cal = calendar.Calendar(firstweekday=6)  # Start with Sunday
    month_days = cal.monthdayscalendar(current_date.year, current_date.month)
    
    # Day headers
    st.markdown('''
    <div style="display:grid; grid-template-columns:repeat(7, 1fr); gap:2px; margin-bottom:5px;">
        <div style="text-align:center; font-weight:bold; color:#FF6B35; padding:5px;">SUN</div>
        <div style="text-align:center; font-weight:bold; color:#FF6B35; padding:5px;">MON</div>
        <div style="text-align:center; font-weight:bold; color:#FF6B35; padding:5px;">TUE</div>
        <div style="text-align:center; font-weight:bold; color:#FF6B35; padding:5px;">WED</div>
        <div style="text-align:center; font-weight:bold; color:#FF6B35; padding:5px;">THU</div>
        <div style="text-align:center; font-weight:bold; color:#FF6B35; padding:5px;">FRI</div>
        <div style="text-align:center; font-weight:bold; color:#FF6B35; padding:5px;">SAT</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Calendar weeks
    for week in month_days:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.markdown('<div style="height:80px;"></div>', unsafe_allow_html=True)
                else:
                    day_str = f"{current_date.year}-{current_date.month:02d}-{day:02d}"
                    day_events = events_by_date.get(day_str, [])
                    
                    # Check if today
                    is_today = (day == date.today().day and 
                               current_date.month == date.today().month and 
                               current_date.year == date.today().year)
                    
                    # Event indicators
                    event_dots = ""
                    if day_events:
                        for e in day_events[:3]:  # Show max 3 dots
                            if e['type'] == 'practice':
                                event_dots += "🟢"
                            elif e['type'] == 'game':
                                event_dots += "🔴"
                            else:
                                event_dots += "🔵"
                    
                    # Day cell style
                    bg_color = "rgba(255,107,53,0.3)" if is_today else "rgba(30,30,30,0.8)"
                    border = "2px solid #FF6B35" if is_today else "1px solid rgba(255,107,53,0.2)"
                    
                    if st.button(
                        f"{day}\n{event_dots}" if event_dots else str(day),
                        key=f"day_{day_str}",
                        use_container_width=True,
                        help=f"{len(day_events)} events" if day_events else "No events"
                    ):
                        st.session_state.selected_date = day_str
                        st.session_state.show_day_events = True
                        st.rerun()
    
    # Legend
    st.markdown('''
    <div style="margin-top:1rem; padding:0.5rem; background:rgba(30,30,30,0.8); border-radius:10px;">
        <span style="color:#888; font-size:0.85rem;">Legend: 🟢 Practice | 🔴 Game | 🔵 Other</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # Show selected day events
    if st.session_state.get('show_day_events') and st.session_state.get('selected_date'):
        render_day_events(supabase, coach_id, st.session_state.selected_date)


def render_day_events(supabase, coach_id, selected_date):
    """Show events for a selected day"""
    
    st.markdown(f'''
    <div style="background:rgba(30,30,30,0.95); border:2px solid #FF6B35; border-radius:15px; padding:1.5rem; margin-top:1rem;">
        <div style="font-family:'Orbitron',monospace; color:#FF6B35; font-size:1.1rem; margin-bottom:1rem;">
            📆 Events for {selected_date}
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    events = get_events(supabase, coach_id, selected_date, selected_date)
    
    if events:
        for event in events:
            event_icon = "🏀" if event['type'] == 'practice' else "🎮" if event['type'] == 'game' else "📋"
            facility_name = event.get('facilities', {}).get('name', 'TBD') if event.get('facilities') else 'TBD'
            
            st.markdown(f'''
            <div style="background:rgba(50,50,50,0.8); border-left:4px solid #FF6B35; padding:1rem; margin:0.5rem 0; border-radius:0 10px 10px 0;">
                <div style="font-weight:700; color:#FFFFFF;">{event_icon} {event['title']}</div>
                <div style="color:#B0B0B0; font-size:0.9rem;">
                    ⏰ {event.get('time_start', 'TBD')} - {event.get('time_end', 'TBD')} | 📍 {facility_name}
                </div>
                {f"<div style='color:#FF6B35;'>vs {event['opponent']} ({event.get('home_away', 'TBD')})</div>" if event.get('opponent') else ""}
            </div>
            ''', unsafe_allow_html=True)
            
            # Edit/Delete buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Edit", key=f"edit_event_{event['id']}", use_container_width=True):
                    st.session_state.editing_event = event['id']
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"delete_event_{event['id']}", use_container_width=True):
                    if delete_event(supabase, event['id']):
                        st.success("Event deleted!")
                        st.rerun()
    else:
        st.info("No events scheduled for this day.")
    
    # Add event button
    if st.button("➕ Add Event for This Day", key="add_event_day", use_container_width=True):
        st.session_state.adding_event = True
        st.session_state.new_event_date = selected_date
        st.rerun()
    
    if st.button("❌ Close", key="close_day_view", use_container_width=True):
        st.session_state.show_day_events = False
        st.rerun()


# ============================================================================
# EVENT FORM
# ============================================================================
def render_event_form(supabase, coach_id, event_id=None):
    """Render form to add/edit an event with recurring option"""
    
    is_edit = event_id is not None
    event = get_event_by_id(supabase, event_id) if is_edit else {}
    
    # Back button (outside form)
    if st.button("⬅️ Back", key="back_from_event"):
        st.session_state.adding_event = False
        st.session_state.editing_event = None
        st.session_state.show_day_events = False
        st.rerun()
    
    st.markdown(f'''
    <div style="font-family:'Orbitron',monospace; color:#FF6B35; font-size:1.2rem; margin-bottom:1rem;">
        {"✏️ EDIT EVENT" if is_edit else "➕ ADD NEW EVENT"}
    </div>
    ''', unsafe_allow_html=True)
    
    with st.form(key="event_form"):
        event_type = st.selectbox(
            "Event Type",
            EVENT_TYPES,
            index=EVENT_TYPES.index(event.get('type', 'practice')) if event.get('type') in EVENT_TYPES else 0
        )
        
        title = st.text_input("Title (optional)", value=event.get('title', ''))
        
        col1, col2 = st.columns(2)
        with col1:
            default_date = datetime.strptime(st.session_state.get('new_event_date', date.today().isoformat()), '%Y-%m-%d').date() if not is_edit else datetime.strptime(event.get('event_date', date.today().isoformat()), '%Y-%m-%d').date()
            event_date = st.date_input("Start Date", value=default_date)
        
        with col2:
            facilities = get_facilities(supabase, coach_id)
            facility_options = ["None"] + [f['name'] for f in facilities]
            facility_ids = [None] + [f['id'] for f in facilities]
            
            current_facility_idx = 0
            if event.get('facility_id'):
                for idx, fid in enumerate(facility_ids):
                    if fid == event['facility_id']:
                        current_facility_idx = idx
                        break
            
            facility_selection = st.selectbox("Facility", facility_options, index=current_facility_idx)
            selected_facility_id = facility_ids[facility_options.index(facility_selection)]
        
        col3, col4 = st.columns(2)
        with col3:
            time_start = st.time_input("Start Time", value=datetime.strptime(event.get('time_start', '18:00'), '%H:%M:%S').time() if event.get('time_start') else datetime.strptime('18:00', '%H:%M').time())
        with col4:
            time_end = st.time_input("End Time", value=datetime.strptime(event.get('time_end', '19:30'), '%H:%M:%S').time() if event.get('time_end') else datetime.strptime('19:30', '%H:%M').time())
        
        # Recurring event option (only for new events)
        if not is_edit:
            st.markdown("---")
            st.markdown("**🔄 Recurring Event (Optional)**")
            
            is_recurring = st.checkbox("Repeat this event weekly", value=False)
            
            if is_recurring:
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    # Show which day of week
                    day_name = event_date.strftime('%A')
                    st.info(f"📅 Will repeat every **{day_name}**")
                with col_r2:
                    # End date for recurring
                    default_end = event_date + timedelta(weeks=12)  # 3 months default
                    recurring_end_date = st.date_input("Repeat until", value=default_end)
        else:
            is_recurring = False
            recurring_end_date = None
        
        # Game-specific fields
        if event_type == 'game':
            st.markdown("---")
            st.markdown("**🏀 Game Details**")
            col5, col6 = st.columns(2)
            with col5:
                opponent = st.text_input("Opponent", value=event.get('opponent', ''))
            with col6:
                home_away = st.selectbox("Home/Away", ["home", "away", "neutral"], 
                    index=["home", "away", "neutral"].index(event.get('home_away', 'home')) if event.get('home_away') else 0)
        else:
            opponent = None
            home_away = None
        
        notes = st.text_area("Notes", value=event.get('notes', ''))
        
        col_submit, col_cancel = st.columns(2)
        with col_submit:
            submitted = st.form_submit_button("💾 Save", use_container_width=True)
        with col_cancel:
            cancelled = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submitted:
            # Auto-generate title if empty
            final_title = title if title else f"{event_type.capitalize()}"
            
            data = {
                "type": event_type,
                "title": final_title,
                "event_date": event_date.isoformat(),
                "time_start": time_start.strftime('%H:%M:%S'),
                "time_end": time_end.strftime('%H:%M:%S'),
                "facility_id": selected_facility_id,
                "opponent": opponent,
                "home_away": home_away,
                "notes": notes
            }
            
            if is_edit:
                update_event(supabase, event_id, data)
                st.success("Event updated!")
            else:
                # Handle recurring events
                if is_recurring and recurring_end_date:
                    events_created = 0
                    current_date = event_date
                    
                    while current_date <= recurring_end_date:
                        event_data = data.copy()
                        event_data["event_date"] = current_date.isoformat()
                        create_event(supabase, coach_id, event_data)
                        events_created += 1
                        current_date += timedelta(weeks=1)
                    
                    st.success(f"✅ Created {events_created} recurring events!")
                else:
                    create_event(supabase, coach_id, data)
                    st.success("Event created!")
            
            st.session_state.adding_event = False
            st.session_state.editing_event = None
            st.rerun()
        
        if cancelled:
            st.session_state.adding_event = False
            st.session_state.editing_event = None
            st.rerun()


# ============================================================================
# FACILITIES VIEW
# ============================================================================
def render_facilities(supabase, coach_id):
    """Render facilities management"""
    
    st.markdown('''
    <div style="font-family:'Orbitron',monospace; color:#FF6B35; font-size:1.3rem; margin-bottom:1rem;">
        🏟️ FACILITIES
    </div>
    ''', unsafe_allow_html=True)
    
    # Add button
    if st.button("➕ Add Facility", key="add_facility_btn", use_container_width=False):
        st.session_state.adding_facility = True
        st.rerun()
    
    # Show form if adding/editing
    if st.session_state.get('adding_facility') or st.session_state.get('editing_facility'):
        render_facility_form(supabase, coach_id, st.session_state.get('editing_facility'))
        return
    
    # List facilities
    facilities = get_facilities(supabase, coach_id)
    
    if not facilities:
        st.info("No facilities added yet. Click 'Add Facility' to get started.")
        return
    
    for facility in facilities:
        with st.container():
            st.markdown(f'''
            <div style="background:linear-gradient(135deg, rgba(30,30,30,0.9), rgba(40,40,40,0.8)); 
                        border-left:4px solid #9B59B6; border-radius:0 15px 15px 0; 
                        padding:1rem; margin:0.5rem 0;">
                <div style="font-weight:700; color:#FFFFFF; font-size:1.1rem;">🏟️ {facility['name']}</div>
                <div style="color:#B0B0B0; font-size:0.9rem; margin-top:0.3rem;">
                    📍 {facility.get('address', 'No address')}
                </div>
                <div style="color:#888; font-size:0.85rem;">
                    📞 {facility.get('contact_name', 'N/A')} - {facility.get('contact_phone', 'N/A')}
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Edit", key=f"edit_fac_{facility['id']}", use_container_width=True):
                    st.session_state.editing_facility = facility['id']
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"del_fac_{facility['id']}", use_container_width=True):
                    if delete_facility(supabase, facility['id']):
                        st.success("Facility deleted!")
                        st.rerun()


def render_facility_form(supabase, coach_id, facility_id=None):
    """Render form to add/edit a facility"""
    
    is_edit = facility_id is not None
    facility = get_facility_by_id(supabase, facility_id) if is_edit else {}
    
    # Back button (outside form)
    if st.button("⬅️ Back", key="back_from_facility"):
        st.session_state.adding_facility = False
        st.session_state.editing_facility = None
        st.rerun()
    
    st.markdown(f'''
    <div style="font-family:'Orbitron',monospace; color:#FF6B35; font-size:1.2rem; margin-bottom:1rem;">
        {"✏️ EDIT FACILITY" if is_edit else "➕ ADD NEW FACILITY"}
    </div>
    ''', unsafe_allow_html=True)
    
    with st.form(key="facility_form"):
        name = st.text_input("Facility Name *", value=facility.get('name', ''))
        address = st.text_input("Address", value=facility.get('address', ''))
        
        facility_type = st.selectbox(
            "Type",
            FACILITY_TYPES,
            index=FACILITY_TYPES.index(facility.get('type', 'gym')) if facility.get('type') in FACILITY_TYPES else 0
        )
        
        col1, col2 = st.columns(2)
        with col1:
            contact_name = st.text_input("Contact Name", value=facility.get('contact_name', ''))
        with col2:
            contact_phone = st.text_input("Contact Phone", value=facility.get('contact_phone', ''))
        
        cost = st.number_input("Cost per Hour (optional)", value=float(facility.get('cost_per_hour', 0) or 0), min_value=0.0)
        notes = st.text_area("Notes", value=facility.get('notes', ''))
        
        col_submit, col_cancel = st.columns(2)
        with col_submit:
            submitted = st.form_submit_button("💾 Save", use_container_width=True)
        with col_cancel:
            cancelled = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submitted and name:
            data = {
                "name": name,
                "address": address,
                "type": facility_type,
                "contact_name": contact_name,
                "contact_phone": contact_phone,
                "cost_per_hour": cost if cost > 0 else None,
                "notes": notes
            }
            
            if is_edit:
                update_facility(supabase, facility_id, data)
                st.success("Facility updated!")
            else:
                create_facility(supabase, coach_id, data)
                st.success("Facility created!")
            
            st.session_state.adding_facility = False
            st.session_state.editing_facility = None
            st.rerun()
        
        if cancelled:
            st.session_state.adding_facility = False
            st.session_state.editing_facility = None
            st.rerun()


# ============================================================================
# PLAYERS VIEW
# ============================================================================
def render_players(supabase, coach_id):
    """Render players roster management"""
    
    st.markdown('''
    <div style="font-family:'Orbitron',monospace; color:#FF6B35; font-size:1.3rem; margin-bottom:1rem;">
        👥 PLAYERS ROSTER
    </div>
    ''', unsafe_allow_html=True)
    
    # Add button
    if st.button("➕ Add Player", key="add_player_btn", use_container_width=False):
        st.session_state.adding_player = True
        st.rerun()
    
    # Show form if adding/editing
    if st.session_state.get('adding_player') or st.session_state.get('editing_player'):
        render_player_form(supabase, coach_id, st.session_state.get('editing_player'))
        return
    
    # List players
    players = get_players(supabase, coach_id)
    
    if not players:
        st.info("No players added yet. Click 'Add Player' to get started.")
        return
    
    # Display as cards
    for player in players:
        position_color = "#FF6B35" if player.get('position') == 'Guard' else "#00D4FF" if player.get('position') == 'Forward' else "#00FF87"
        
        st.markdown(f'''
        <div style="background:linear-gradient(135deg, rgba(30,30,30,0.9), rgba(40,40,40,0.8)); 
                    border-left:4px solid {position_color}; border-radius:0 15px 15px 0; 
                    padding:1rem; margin:0.5rem 0;">
            <div style="display:flex; align-items:center; gap:1rem;">
                <div style="background:{position_color}; color:#000; font-weight:900; font-size:1.5rem; 
                            width:50px; height:50px; border-radius:50%; display:flex; 
                            align-items:center; justify-content:center;">
                    {player.get('jersey_number', '?')}
                </div>
                <div>
                    <div style="font-weight:700; color:#FFFFFF; font-size:1.1rem;">
                        {player['first_name']} {player['last_name']}
                    </div>
                    <div style="color:{position_color}; font-size:0.9rem;">{player.get('position', 'N/A')}</div>
                </div>
            </div>
            <div style="color:#888; font-size:0.85rem; margin-top:0.5rem;">
                👨‍👩‍👦 {player.get('parent1_name', 'N/A')} - 📞 {player.get('parent1_phone', 'N/A')}
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Edit", key=f"edit_player_{player['id']}", use_container_width=True):
                st.session_state.editing_player = player['id']
                st.rerun()
        with col2:
            if st.button("🗑️ Remove", key=f"del_player_{player['id']}", use_container_width=True):
                if delete_player(supabase, player['id']):
                    st.success("Player removed!")
                    st.rerun()


def render_player_form(supabase, coach_id, player_id=None):
    """Render form to add/edit a player"""
    
    is_edit = player_id is not None
    player = get_player_by_id(supabase, player_id) if is_edit else {}
    
    # Back button (outside form)
    if st.button("⬅️ Back", key="back_from_player"):
        st.session_state.adding_player = False
        st.session_state.editing_player = None
        st.rerun()
    
    st.markdown(f'''
    <div style="font-family:'Orbitron',monospace; color:#FF6B35; font-size:1.2rem; margin-bottom:1rem;">
        {"✏️ EDIT PLAYER" if is_edit else "➕ ADD NEW PLAYER"}
    </div>
    ''', unsafe_allow_html=True)
    
    with st.form(key="player_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *", value=player.get('first_name', ''))
        with col2:
            last_name = st.text_input("Last Name *", value=player.get('last_name', ''))
        
        col3, col4, col5 = st.columns(3)
        with col3:
            jersey_number = st.number_input("Jersey #", value=int(player.get('jersey_number', 0) or 0), min_value=0, max_value=99)
        with col4:
            position = st.selectbox("Position", [""] + PLAYER_POSITIONS, 
                index=PLAYER_POSITIONS.index(player.get('position')) + 1 if player.get('position') in PLAYER_POSITIONS else 0)
        with col5:
            dob = st.date_input("Date of Birth", 
                value=datetime.strptime(player['date_of_birth'], '%Y-%m-%d').date() if player.get('date_of_birth') else None)
        
        st.markdown("**Parent/Guardian 1**")
        col6, col7 = st.columns(2)
        with col6:
            parent1_name = st.text_input("Parent 1 Name", value=player.get('parent1_name', ''))
        with col7:
            parent1_phone = st.text_input("Parent 1 Phone", value=player.get('parent1_phone', ''))
        
        st.markdown("**Parent/Guardian 2 (Optional)**")
        col8, col9 = st.columns(2)
        with col8:
            parent2_name = st.text_input("Parent 2 Name", value=player.get('parent2_name', ''))
        with col9:
            parent2_phone = st.text_input("Parent 2 Phone", value=player.get('parent2_phone', ''))
        
        emergency_phone = st.text_input("Emergency Phone", value=player.get('emergency_phone', ''))
        notes = st.text_area("Notes (medical, allergies, etc.)", value=player.get('notes', ''))
        
        col_submit, col_cancel = st.columns(2)
        with col_submit:
            submitted = st.form_submit_button("💾 Save", use_container_width=True)
        with col_cancel:
            cancelled = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submitted and first_name and last_name:
            data = {
                "first_name": first_name,
                "last_name": last_name,
                "jersey_number": jersey_number if jersey_number > 0 else None,
                "position": position if position else None,
                "date_of_birth": dob.isoformat() if dob else None,
                "parent1_name": parent1_name,
                "parent1_phone": parent1_phone,
                "parent2_name": parent2_name if parent2_name else None,
                "parent2_phone": parent2_phone if parent2_phone else None,
                "emergency_phone": emergency_phone,
                "notes": notes
            }
            
            if is_edit:
                update_player(supabase, player_id, data)
                st.success("Player updated!")
            else:
                create_player(supabase, coach_id, data)
                st.success("Player added!")
            
            st.session_state.adding_player = False
            st.session_state.editing_player = None
            st.rerun()
        
        if cancelled:
            st.session_state.adding_player = False
            st.session_state.editing_player = None
            st.rerun()


# ============================================================================
# MAIN LOGISTICS PAGE
# ============================================================================
def render_logistics_page(supabase, coach_id):
    """Main logistics page with tabs"""
    
    st.markdown('''
    <div style="background:linear-gradient(135deg, rgba(20,20,20,0.9), rgba(30,30,30,0.85));
                border:1px solid rgba(155,89,182,0.5); border-radius:15px; padding:1.5rem; margin-bottom:1.5rem;">
        <div style="font-family:'Orbitron',monospace; font-size:1.8rem; font-weight:700; color:#9B59B6; margin-bottom:0.5rem;">
            📋 TEAM MANAGER
        </div>
        <div style="color:#B0B0B0;">Manage your schedule, facilities, and players roster</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Check if we're in a form mode
    if st.session_state.get('adding_event') or st.session_state.get('editing_event'):
        render_event_form(supabase, coach_id, st.session_state.get('editing_event'))
        return
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📅 CALENDAR", "🏟️ FACILITIES", "👥 PLAYERS"])
    
    with tab1:
        render_calendar(supabase, coach_id)
    
    with tab2:
        render_facilities(supabase, coach_id)
    
    with tab3:
        render_players(supabase, coach_id)