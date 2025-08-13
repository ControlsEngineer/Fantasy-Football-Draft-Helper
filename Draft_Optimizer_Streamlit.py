import streamlit as st
import csv
from Player_Selector import *

# Custom CSS for styling
st.markdown("""
    <style>
        .main-title {
            font-size: 40px;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 25px;
        }
        .section-header {
            font-size: 22px;
            font-weight: 600;
            color: #34495e;
            margin-top: 20px;
            margin-bottom: 10px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
        }
        .player-card {
            background-color: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 8px 20px;
            margin: 5px;
            font-size: 16px;
        }
        .button {
            background-color: #3498db;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        .button:hover { background-color: #2980b9; }
        .danger { background-color: #e74c3c; }
        .danger:hover { background-color: #c0392b; }
        .success { background-color: #2ecc71; }
        .success:hover { background-color: #27ae60; }
        .neutral { background-color: #95a5a6; }
        .neutral:hover { background-color: #7f8c8d; }
        .team-slot {
            background-color: #ffffff;
            border: 1px dashed #bdc3c7;
            padding: 6px 10px;
            border-radius: 6px;
            margin-bottom: 6px;
            min-height: 32px;
        }
    </style>
""", unsafe_allow_html=True)

### initialize variables to stay keep throughout
def initialize_session_state():
    if 'data' not in st.session_state:
        st.session_state.data = {'QB': [], 'RB': [], 'WR': [], 'TE': []}  # total dictionary of players (tuples of 4)
    if 'recently_added_players' not in st.session_state:
        st.session_state.recently_added_players = []  # List to keep track of players added by the user in order
    if 'recently_deleted_players' not in st.session_state:
        st.session_state.recently_deleted_players = []  # Stack to keep track of players deleted from the board
    if 'added_players' not in st.session_state:
        st.session_state.added_players = []  # For my team
    if 'Positions_Remaining' not in st.session_state:
        st.session_state.Positions_Remaining = [0, 0, 0, 0]  # QBs, RBs, WRs, TEs
    if 'My_QBs' not in st.session_state:
        st.session_state.My_QBs = []
    if 'My_RBs' not in st.session_state:
        st.session_state.My_RBs = []
    if 'My_WRs' not in st.session_state:
        st.session_state.My_WRs = []
    if 'My_TEs' not in st.session_state:
        st.session_state.My_TEs = []
    if 'popup_open' not in st.session_state:
        st.session_state.popup_open = False
    if 'draft_triggered' not in st.session_state:
        st.session_state.draft_triggered = False

# Call the initialization function at the start of your script
initialize_session_state()


# Function to display the drafter popup, used later in script
def show_popup(data, QBs, RBs, WRs, TEs, Positions_Remaining, league_size):
    with st.form(key='popup_form'):
        st.write('You should draft:')
        # Player_Selector can return 4 or 5 values. If 5, ignore the 5th.
        rec = Player_Selector(data, QBs, RBs, WRs, TEs, Positions_Remaining, league_size)
        if len(rec) >= 4:
            Player_Name, Player_Position, Player_Points, Player_Team = rec[:4]
        else:
            Player_Name, Player_Position, Player_Points, Player_Team = rec[0], rec[1], rec[2], ''
        submit_button = st.form_submit_button(f'{Player_Name}')
        
        if submit_button:
            st.session_state.player_name = Player_Name
            st.session_state.player_position = Player_Position
            st.session_state.player_points = Player_Points
            st.session_state.player_team = Player_Team
            st.session_state.popup_open = False  # Close the popup
            st.session_state.draft_triggered = True  # Set a flag to indicate a draft was triggered
            st.rerun()  # Use rerun to refresh the app state

# Function to create the initial page
def initial_page():
    st.header("Welcome to the Fantasy Football Draft Aid - 2025")
    st.write("Select your draft settings below.")
    
    league_size = st.selectbox("League Size", [8, 10, 12], help="Choose your league size")
    scoring_format = st.selectbox("Scoring Format", ["Standard", "0.5 PPR", "PPR"], help="Select your scoring format")
    
    # Set draft positions based on league size
    if league_size == 8:
        QBs = 2
        RBs = 5
        WRs = 5
        TEs = 1
    elif league_size == 10:
        QBs = 2
        RBs = 6
        WRs = 6
        TEs = 1
    else:  # 12 teams
        QBs = 2
        RBs = 7
        WRs = 6
        TEs = 2

    # Store them for later
    st.session_state.Positions_Remaining = [QBs, RBs, WRs, TEs]

    # Enter button
    if st.button("Enter"):
        st.session_state.page = 'main'
        st.rerun()

# Function to create the main app page
def main_page():
    st.markdown('<div class="main-title">Fantasy Football Draft Aid</div>', unsafe_allow_html=True)

    # Load scoring format
    scoring_format = 'player_rankings_PPR.csv'
    if st.session_state.get('page_scoring') == 'Standard':
        scoring_format = 'player_rankings_standard.csv'
    elif st.session_state.get('page_scoring') == '0.5 PPR':
        scoring_format = 'player_rankings_half_PPR.csv'

    # Open CSV file (player, position, points, team) and convert it to a list once
    data = st.session_state.data
    if data == {'QB': [], 'RB': [], 'WR': [], 'TE': []}:
        try:
            with open(scoring_format, newline='', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                for player, position, points, team in list(reader):
                    # Skip headers or malformed rows
                    if position not in {'QB','RB','WR','TE'}:
                        continue
                    data[position].append((player, position, points, team))
        except FileNotFoundError:
            st.error(f"Could not find rankings file: {scoring_format}. Place it next to this script or provide the correct path.")
            st.stop()

    # Keep local aliases
    QBs, RBs, WRs, TEs = st.session_state.Positions_Remaining
    
    # If popup requested, show it
    if st.session_state.get('popup_open', False):
        show_popup(data, QBs, RBs, WRs, TEs, st.session_state.Positions_Remaining, sum(st.session_state.Positions_Remaining))

    # Draft recommendation trigger
    if st.button("Recommend a Pick"):
        st.session_state.popup_open = True
        st.rerun()

    # Layout for available players
    col1, col2, col3, col4 = st.columns(4)

    def render_position(col, position_key, label):
        with col:
            st.markdown(f'<div class="section-header">Top {label}</div>', unsafe_allow_html=True)
            available = data[position_key][:10]
            for player_name, pos, pts, team in available:
                with st.form(key=f"add_{position_key}_{player_name}"):
                    st.write(f"{player_name} — {team} — {pts}")
                    if st.form_submit_button("Add to My Board"):
                        # Add to user's board and remove from available list
                        st.session_state.recently_added_players.append((player_name, pos, pts, team))
                        # remove from data
                        for i, tpl in enumerate(data[position_key]):
                            if tpl[0] == player_name:
                                data[position_key].pop(i)
                                break
                        st.session_state.data = data
                        st.rerun()

    render_position(col1, 'QB', 'QBs')
    render_position(col2, 'RB', 'RBs')
    render_position(col3, 'WR', 'WRs')
    render_position(col4, 'TE', 'TEs')

    # Sidebar - Team Selection
    st.sidebar.markdown('<div class="section-header">Your Team</div>', unsafe_allow_html=True)

    def render_team(section_label, key_name, count):
        st.sidebar.markdown(f"**{section_label} ({count})**")
        slots = getattr(st.session_state, key_name)
        # Normalize slots length
        while len(slots) < count:
            slots.append(' ')
        for i in range(count):
            slots[i] = st.sidebar.text_input(f"{section_label[:-1]} {i+1}", slots[i], key=f"{key_name}_{i}")
        setattr(st.session_state, key_name, slots)

    render_team("QBs", "My_QBs", QBs)
    render_team("RBs", "My_RBs", RBs)
    render_team("WRs", "My_WRs", WRs)
    render_team("TEs", "My_TEs", TEs)

    # Undo last add
    if st.sidebar.button("Undo Add"):
        if st.session_state.recently_added_players:
            last = st.session_state.recently_added_players.pop()
            player_name, player_position, player_points, player_team = last
            # Insert back into sorted position list by points (desc)
            position_list = data[player_position]
            insert_index = 0
            try:
                p_pts = float(player_points)
            except Exception:
                p_pts = -1e9
            while insert_index < len(position_list):
                try:
                    cur_pts = float(position_list[insert_index][2])
                except Exception:
                    cur_pts = -1e9
                if p_pts >= cur_pts:
                    break
                insert_index += 1
            position_list.insert(insert_index, (player_name, player_position, player_points, player_team))
            st.session_state.data[player_position] = position_list
            # Remove from user's team if present
            for key_name in ["My_QBs","My_RBs","My_WRs","My_TEs"]:
                slots = getattr(st.session_state, key_name)
                for i in range(len(slots)):
                    if slots[i] == player_name:
                        slots[i] = ' '
                        break
                setattr(st.session_state, key_name, slots)
            st.rerun()

    # Manual remove from board (drafted by others)
    st.sidebar.markdown('<div class="section-header">Mark Player Drafted (remove from board)</div>', unsafe_allow_html=True)
    remove_name = st.sidebar.text_input("Player Name to Remove", "")
    if st.sidebar.button("Remove from Board") and remove_name:
        found = False
        for key in list(data.keys()):
            for idx, tpl in enumerate(list(data[key])):
                if tpl[0].strip().lower() == remove_name.strip().lower():
                    deleted_player = data[key].pop(idx)
                    st.session_state.data = data
                    st.session_state.recently_deleted_players.append(deleted_player)
                    found = True
                    break
            if found:
                break
        st.rerun()

    # Undo remove
    if st.sidebar.button("Undo Remove"):
        if st.session_state.recently_deleted_players:
            last_removed_player = st.session_state.recently_deleted_players.pop()
            player_name, player_position, player_points, player_team = last_removed_player
            position_list = data[player_position]
            insert_index = 0
            try:
                p_pts = float(player_points)
            except Exception:
                p_pts = -1e9
            while insert_index < len(position_list):
                try:
                    cur_pts = float(position_list[insert_index][2])
                except Exception:
                    cur_pts = -1e9
                if p_pts >= cur_pts:
                    break
                insert_index += 1
            position_list.insert(insert_index, (player_name, player_position, player_points, player_team))
            st.session_state.data[player_position] = position_list
            st.rerun()

    # Simple navigation
    st.sidebar.markdown('<div class="section-header">Navigation</div>', unsafe_allow_html=True)
    if st.sidebar.button("Back to Start"):
        st.session_state.page = 'start'
        st.rerun()

# Router
if 'page' not in st.session_state:
    st.session_state.page = 'start'

if st.session_state.page == 'start':
    # Store selections for later use in main_page
    st.session_state.page_scoring = st.selectbox("Scoring Format", ["Standard", "0.5 PPR", "PPR"], index=2)
    st.session_state.page_league = st.selectbox("League Size", [8,10,12], index=2)
    if st.button("Enter"):
        # Initialize positions for chosen league size
        if st.session_state.page_league == 8:
            st.session_state.Positions_Remaining = [2,5,5,1]
        elif st.session_state.page_league == 10:
            st.session_state.Positions_Remaining = [2,6,6,1]
        else:
            st.session_state.Positions_Remaining = [2,7,6,2]
        st.session_state.page = 'main'
        st.rerun()
else:
    main_page()
