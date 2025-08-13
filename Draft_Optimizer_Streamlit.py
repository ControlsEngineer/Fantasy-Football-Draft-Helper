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
            font-size: 28px;
            font-weight: bold;
            color: #34495e;
            margin-top: 25px;
            margin-bottom: 10px;
        }
        .sub-header {
            font-size: 22px;
            font-weight: 600;
            color: #2c3e50;
            margin-top: 20px;
            margin-bottom: 12px;
        }
        .info-text {
            font-size: 16px;
            color: #7f8c8d;
        }
        .player-section {
            font-size: 21px;
            font-weight: 700;
            color: #3498db;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .player-list {
            font-size: 16px;
            color: #2c3e50;
        }
        .st-tabs [data-baseweb="tab-list"] {
            gap: 0px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 28px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 10px 10px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(49, 51, 63, 0.2);
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(49, 51, 63, 0.2);
            color: rgb(49, 51, 63);
        }
        .stTabs [data-baseweb="tab-highlight"] {
            background-color: transparent;
        }
        button[kind="header"] {
            display: none;
        }
        .my-button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 18px;
            font-weight: bold;
            color: #ffffff;
            background-color: #3498db; /* Button color */
            border: none;
            border-radius: 8px;
            cursor: pointer;
            text-align: center;
        }
        .my-button:hover {
            background-color: #2980b9; /* Hover color */
        }
        .blur-background {
            filter: blur(2px);
        }
        .no-blur-background {
            filter: none;
        }
        .centered-container {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .spaced-column {
            padding: 5px 10px;
        }
        .divider {
            height: 1px;
            background-color: #ccc;
            margin: 15px 0;
        }
        .input-measure-table {
            width: 100%;
            border-collapse: collapse;
        }
        .input-measure-table th, .input-measure-table td {
            border: 1px solid #ddd;
            padding: 6px;
            text-align: center;
        }
        .input-measure-table th {
            background-color: #f9f9f9;
            font-weight: bold;
        }
        .bordered-container {
            border: 1px solid #bdc3c7;
            border-radius: 10px;
        }
        .stButton>button {
            background-color: #212121; /* Dark Gray */
            color: #ffffff; /* White text */
            border-radius: 8px;
            padding: 8px 20px;
            margin: 5px;
            font-size: 16px;
            font-weight: bold;
            border: none;
            white-space: nowrap;
        }
        .stButton>button:hover {
            background-color: rgba(119, 119, 119, 0.5); /* Light Gray (hover) */
            color: #ffffff; /* Keep white text on hover */
        }
        .alert-box {
            background-color: #ffe6e6;
            color: #d9534f;
            border: 1px solid #d9534f;
            border-radius: 5px;
            padding: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Helper to append a small "Pts: XY" badge to a specific Streamlit button
def _add_points_badge(button_label: str, points_text: str):
    st.markdown(f"""
        <style>
            div.stButton > button[aria-label="{button_label}"]::after {{
                content: "  Pts: {points_text}";
                font-size: 12px;
                opacity: 0.85;
                margin-left: 8px;
                white-space: nowrap;
            }}
            div.stButton > button[aria-label="{button_label}"] {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
            }}
        </style>
    """, unsafe_allow_html=True)

### initialize variables to stay keep throughout
def initialize_session_state():
    if 'data' not in st.session_state:
        st.session_state.data = {'QB': [], 'RB': [], 'WR': [], 'TE': []}  # total dictionary of players
    if 'recently_added_players' not in st.session_state:
        st.session_state.recently_added_players = []  # List to keep track of players added by the user in order
    if 'recently_deleted_players' not in st.session_state:
        st.session_state.recently_deleted_players = []  # Stack to keep track of deleted players
    if 'recommended_pick' not in st.session_state:
        st.session_state.recommended_pick = "No recommendation yet."
    if 'page' not in st.session_state:
        st.session_state.page = "initial"
    if 'draft_order' not in st.session_state:
        st.session_state.draft_order = []
    if 'remove_order_counter' not in st.session_state:
        st.session_state.remove_order_counter = 0
    if 'total_wrs' not in st.session_state:
        st.session_state.total_wrs = 0
    if 'total_tes' not in st.session_state:
        st.session_state.total_tes = 0
    if 'total_rbs' not in st.session_state:
        st.session_state.total_rbs = 0
    if 'total_qbs' not in st.session_state:
        st.session_state.total_qbs = 0
    if 'recently_removed' not in st.session_state:
        st.session_state.recently_removed = []
    if 'button_pressed_draft' not in st.session_state:
        st.session_state.button_pressed_draft = False
    if 'button_pressed_remove' not in st.session_state:
        st.session_state.button_pressed_remove = False
    if 'widget1' not in st.session_state:
        st.session_state.widget1 = ''
    if 'widget2' not in st.session_state:
        st.session_state.widget2 = ''
    if 'drafted_player' not in st.session_state:
        st.session_state.drafted_player = ''
    if 'removed_player' not in st.session_state:
        st.session_state.removed_player = ''

initialize_session_state()

def initial_page():
    st.markdown('<div class="main-title">Fantasy Football Draft Aid</div>', unsafe_allow_html=True)
    with st.expander("Instructions", expanded=True):
        st.markdown("""
        This tool helps visualize your draft board and manage player selections.
        """)
    st.markdown('<div class="section-header">League Settings</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        league_size = st.selectbox("League Size", [8, 10, 12], index=1)

    with col2:
        scoring_format = st.selectbox("Scoring Format", ["PPR", "half PPR", "standard"], index=0)

    # Position assumptions based on league size
    if league_size == 8:
        qb_count, rb_count, wr_count, te_count = 2, 5, 5, 1
    elif league_size == 10:
        qb_count, rb_count, wr_count, te_count = 2, 6, 6, 1
    else:  # 12
        qb_count, rb_count, wr_count, te_count = 2, 7, 6, 2

    st.session_state.total_qbs = qb_count
    st.session_state.total_rbs = rb_count
    st.session_state.total_wrs = wr_count
    st.session_state.total_tes = te_count

    st.write(f"Roster assumptions — QB: {qb_count}, RB: {rb_count}, WR: {wr_count}, TE: {te_count}")

    # Load data
    st.markdown('<div class="section-header">Load Rankings CSV</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload rankings CSV for the chosen scoring format", type=['csv'])
    if uploaded_file:
        try:
            st.session_state.data = read_csv(uploaded_file)
            st.success("Rankings loaded.")
        except Exception as e:
            st.error(f"Error loading CSV: {e}")

    # Navigation
    if st.button("Go to Draft Board", use_container_width=True):
        st.session_state.page = "main"
        st.rerun()

def main_page():
    st.markdown('<div class="main-title">Draft Board</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-text">Click a player to remove them when drafted. Use Undo to restore.</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Draft Board", "Add/Remove Players", "My Team"])

    with tabs[0]:
        show_draft_board()
    with tabs[1]:
        add_remove_players()
    with tabs[2]:
        show_my_team()

def read_csv(file):
    data = {'QB': [], 'RB': [], 'WR': [], 'TE': []}
    csv_reader = csv.DictReader(file)
    # Expected columns: Name,Position,Points,Team (order may vary)
    for row in csv_reader:
        name = row.get('Name') or row.get('Player') or row.get('player') or row.get('name')
        pos = (row.get('Position') or row.get('POS') or row.get('position') or "").strip().upper()
        points_raw = row.get('Points') or row.get('FPts') or row.get('Proj') or row.get('Projected') or row.get('points') or "0"
        team = row.get('Team') or row.get('team') or row.get('NFL Team') or ""
        try:
            points = float(points_raw)
        except:
            try:
                points = float(points_raw.replace(',', ''))
            except:
                points = 0.0

        if pos in data:
            data[pos].append((name, team, points, pos))

    # Sort each position by points desc
    for k in data:
        data[k].sort(key=lambda x: x[2], reverse=True)
    return data

def show_draft_board():
    data = st.session_state.data
    recently_deleted_players = st.session_state.recently_deleted_players

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="sub-header">Top QBs</div>', unsafe_allow_html=True)
        for p in data['QB'][:10]:
            st.write(f"{p[0]} — {p[2]:.1f}")
    with col2:
        st.markdown('<div class="sub-header">Top RBs</div>', unsafe_allow_html=True)
        for p in data['RB'][:10]:
            st.write(f"{p[0]} — {p[2]:.1f}")
    with col3:
        st.markdown('<div class="sub-header">Top WRs</div>', unsafe_allow_html=True)
        for p in data['WR'][:10]:
            st.write(f"{p[0]} — {p[2]:.1f}")
    with col4:
        st.markdown('<div class="sub-header">Top TEs</div>', unsafe_allow_html=True)
        for p in data['TE'][:10]:
            st.write(f"{p[0]} — {p[2]:.1f}")

    st.divider()

    col_undo, col_redo = st.columns(2)
    with col_undo:
        if st.button("Undo Last Removal", use_container_width=True):
            if recently_deleted_players:
                last_removed = recently_deleted_players.pop()
                name, team, points, pos = last_removed
                st.session_state.data[pos].append((name, team, points, pos))
                st.session_state.data[pos].sort(key=lambda x: x[2], reverse=True)
                st.session_state.recently_deleted_players = recently_deleted_players
                st.success(f"Restored {name}")
            else:
                st.warning("No players to undo.")

    with col_redo:
        st.button("Redo (coming soon)", use_container_width=True, disabled=True)

    st.divider()

    ### Player Buttons
    cola, colb = st.columns(2)

    with cola:
        for position in ['RB', 'QB']:
            available_players = data[position][:4]  # Get the top 4 players for this position
            st.markdown(f'<div class="player-section" style="text-align: center;">Next {position}s</div>', unsafe_allow_html=True)
            for player in available_players:
                player_name = player[0]
                player_points = player[2]
                _add_points_badge(player_name, str(player_points))
                if st.button(player_name, key=player_name, use_container_width=True):
                    # Delete Drafted Player from board
                    for key in data:
                        for idx, player_tuple in enumerate(data[key]):
                            if player_name == player_tuple[0]:
                                deleted_player = data[key].pop(idx)  # Remove the player
                                removed_player = player_name
                                st.session_state.data = data
                                recently_deleted_players.append((removed_player, deleted_player[1], deleted_player[2], deleted_player[3]))
                                st.session_state.recently_deleted_players = recently_deleted_players
                                st.rerun()
                                break     

    with colb:
        for position in ['WR', 'TE']:
            available_players = data[position][:4]  # Get the top 4 players for this position
            st.markdown(f'<div class="player-section" style="text-align: center;">Next {position}s</div>', unsafe_allow_html=True)
            for player in available_players:
                player_name = player[0]
                player_points = player[2]
                _add_points_badge(player_name, str(player_points))
                if st.button(player_name, key=player_name, use_container_width=True):
                    # Delete Drafted Player from board
                    for key in data:
                        for idx, player_tuple in enumerate(data[key]):
                            if player_name == player_tuple[0]:
                                deleted_player = data[key].pop(idx)  # Remove the player
                                removed_player = player_name
                                st.session_state.data = data
                                recently_deleted_players.append((removed_player, deleted_player[1], deleted_player[2], deleted_player[3]))
                                st.session_state.recently_deleted_players = recently_deleted_players
                                st.rerun()
                                break     

def add_remove_players():
    st.markdown('<div class="section-header">Add/Remove Players</div>', unsafe_allow_html=True)
    data = st.session_state.data
    recently_deleted_players = st.session_state.recently_deleted_players

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sub-header">Add Player</div>', unsafe_allow_html=True)

        # Input fields for adding a player
        name = st.text_input("Player Name:")
        team = st.text_input("Team (optional):")
        points = st.number_input("Projected Points:", min_value=0.0, step=0.1)
        position = st.selectbox("Position:", ['QB', 'RB', 'WR', 'TE'])

        if st.button("Add Player", use_container_width=True):
            if name:
                new_player = (name, team, float(points), position)
                data[position].append(new_player)
                data[position].sort(key=lambda x: x[2], reverse=True)
                st.session_state.data = data
                st.session_state.recently_added_players.append(new_player)
                st.success(f"Added {name} to {position}.")
            else:
                st.warning("Enter a name to add a player.")

        st.divider()

        st.markdown('<div class="sub-header">Undo Last Add</div>', unsafe_allow_html=True)
        if st.button("Undo Add", use_container_width=True):
            if st.session_state.recently_added_players:
                last_added = st.session_state.recently_added_players.pop()
                name, team, points, position = last_added
                # Remove this exact tuple if present
                try:
                    data[position].remove(last_added)
                    st.session_state.data = data
                    st.warning(f"Removed last added: {name} from {position}.")
                except ValueError:
                    st.info("Last added player not found.")
            else:
                st.warning("No adds to undo.")

    with col2:
        st.markdown('<div class="sub-header">Remove Player</div>', unsafe_allow_html=True)

        def submit2():
            st.session_state.removed_player = st.session_state.widget2
            st.session_state.widget2 = ''
            st.session_state.button_pressed_remove = True

        removed_player = st.text_input("Remove player by name (case-insensitive):", key='widget2', on_change=submit2)

        removed_player = st.session_state.removed_player
        if st.session_state.get('button_pressed_remove', False):  # Check if the input was activated
            player_found = False
            for key in data:
                for idx, player_tuple in enumerate(data[key]):
                    if removed_player.lower() == player_tuple[0].lower():  # Case insensitive comparison
                        deleted_player = data[key].pop(idx)  # Remove the player
                        st.session_state.data = data
                        player_found = True
                        recently_deleted_players.append((deleted_player[0], deleted_player[1], deleted_player[2], deleted_player[3]))
                        st.session_state.recently_deleted_players = recently_deleted_players
                        break

            if not player_found:
                st.error("Player Not Found in Draft Board")
            else:
                st.success(f"Removed {removed_player} from the draft board")

        st.divider()

        st.markdown('<div class="sub-header">Undo Last Removal</div>', unsafe_allow_html=True)
        if st.button("Undo Removal", use_container_width=True):
            if recently_deleted_players:
                last_removed = recently_deleted_players.pop()
                name, team, points, position = last_removed
                st.session_state.data[position].append((name, team, points, position))
                st.session_state.data[position].sort(key=lambda x: x[2], reverse=True)
                st.session_state.recently_deleted_players = recently_deleted_players
                st.success(f"Restored {name} to {position}.")
            else:
                st.warning("No picks to undo.")

def show_my_team():
    st.markdown('<div class="section-header">My Team</div>', unsafe_allow_html=True)
    st.sidebar.markdown("### My Picks")
    my_players = [p[0] for p in st.session_state.recently_added_players]  # Example list; adapt as needed

    # Display players in a numbered list
    for i, player in enumerate(my_players, start=1):
            st.sidebar.text(f"{i}. {player}")

# Main application logic
if 'page' not in st.session_state:
    st.session_state.page = "initial"

if st.session_state.page == "initial":
    initial_page()
else:
    main_page()
