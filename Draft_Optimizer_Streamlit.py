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
            color: #2c3e50;
            margin-top: 25px;
            margin-bottom: 10px;
        }
        .player-section {
            font-size: 20px;
            color: #2980b9;
            white-space: nowrap;
        }
        .sidebar .block-container {
            background-color: #ecf0f1;
            padding: 15px;
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
            background-color: rgba(119, 119, 119, 0.5); /* Lighter Gray with 80% opacity on Hover */
        }
        .stTextInput>div>div>input {
            background-color: #f7f9fa;
            border-radius: 5px;
            border: 1px solid #bdc3c7;
            padding: 8px;
        }
    </style>
""", unsafe_allow_html=True)

### initialize variables to stay keep throughout
def initialize_session_state():
    if 'data' not in st.session_state:
        st.session_state.data = {'QB': [], 'RB': [], 'WR': [], 'TE': []}  # total dictionary of players
    if 'recently_added_players' not in st.session_state:
        st.session_state.recently_added_players = []  # List to keep track of players added by the user in order
    if 'recently_deleted_players' not in st.session_state:
        st.session_state.recently_deleted_players = []  # Stack to keep track of players deleted from the board
    if 'added_players' not in st.session_state:
        st.session_state.added_players = []  # For my team
    if 'Positions_Remaining' not in st.session_state:
        st.session_state.Positions_Remaining = []  # Track the amount of players left to draft at each position
    if 'drafted_player' not in st.session_state:
        st.session_state.drafted_player = ""  # For manually drafting a player
    if 'removed_player' not in st.session_state:
        st.session_state.removed_player = ""  # For manually removing a player
    # Positional players left on the board
    if 'My_QBs' not in st.session_state:
        st.session_state.My_QBs = []
    if 'My_RBs' not in st.session_state:
        st.session_state.My_RBs = []
    if 'My_WRs' not in st.session_state:
        st.session_state.My_WRs = []
    if 'My_TEs' not in st.session_state:
        st.session_state.My_TEs = []
# Call the initialization function at the start of your script
initialize_session_state()


# Function to display the drafter popup, used later in script
def show_popup(data, QBs, RBs, WRs, TEs, Positions_Remaining, league_size):
    with st.form(key='popup_form'):
        st.write('You should draft:')
        Player_Name, Player_Position, Player_Points, Player_Team, Player_ADP = Player_selector(data, QBs, RBs, WRs, TEs, Positions_Remaining, league_size)
        submit_button = st.form_submit_button(f'{Player_Name}')
        
        if submit_button:
            st.session_state.player_name = Player_Name
            st.session_state.player_position = Player_Position
            st.session_state.player_points = Player_Points
            st.session_state.player_team = Player_Team
            st.session_state.player_ADP = Player_ADP
            st.session_state.popup_open = False  # Close the popup
            st.session_state.draft_triggered = True  # Set a flag to indicate a draft was triggered
            st.rerun()  # Use rerun to refresh the app state

# Function to create the initial page
def initial_page():
    st.header("Welcome to the Fantasy Football Draft Aid - 2024")
    st.write("Select your draft settings below.")
    
    league_size = st.selectbox("League Size", [8, 10, 12], help="Choose your league size")
    scoring_format = st.selectbox("Scoring Format", ["Standard", "0.5 PPR", "PPR"], help="Select your scoring format")
    
    draft_limits = {
        "Number of QBs to Draft": {"min": 1, "max": 5, "default": 2},
        "Number of RBs to Draft": {"min": 1, "max": 7, "default": 5},
        "Number of WRs to Draft": {"min": 1, "max": 7, "default": 5},
        "Number of TEs to Draft": {"min": 1, "max": 5, "default": 1}
    }
    
    draft_count = {}
    for position, limits in draft_limits.items():
        draft_count[position] = st.number_input(
            position,
            min_value=limits["min"],
            max_value=limits["max"],
            value=limits["default"],
            help=f"Select the number of {position.split()[2]}s to draft"
        )
        
    if st.button("Enter"):
        st.session_state.league_size = league_size
        st.session_state.scoring_format = scoring_format
        st.session_state.draft_count = draft_count
        st.session_state.page = "main"
        st.rerun()

# Function to create the main page
def main_page():
    st.markdown('<div class="main-title">Fantasy Football Draft Aid 2024</div>', unsafe_allow_html=True)
    st.write(' ')
    league_size = st.session_state.get("league_size", "8")
    scoring_format = st.session_state.get("scoring_format", "0.5 PPR")
    draft_count = st.session_state.get("draft_count", {})
    
    # Choose CSV based on scoring format
    if scoring_format == 'Standard':
        scoring_format = 'player_rankings_standard.csv'
    elif scoring_format == '0.5 PPR':
        scoring_format = 'player_rankings_half_PPR.csv'
    elif scoring_format == 'PPR':
        scoring_format = 'player_rankings_PPR.csv'
   
    # Open CSV file with {player, position, projected points, Team, and ADP}, and convert it to a list, but only the first time
    data = st.session_state.data
    if data == {'QB': [], 'RB': [], 'WR': [], 'TE': []}:
        with open(scoring_format, newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for player, position, points, team, adp in list(reader):
                if position in data:
                    data[position].append((player, position, points, team, adp))
    print(st.session_state.recently_deleted_players)
    recently_added_players = st.session_state.recently_added_players # List to keep track of players added by the user in order
    recently_deleted_players = st.session_state.recently_deleted_players # Stack to keep track of players deleted from the board
    added_players = st.session_state.added_players # For my team

    # Initialize player counts
    Number_of_QBs = draft_count['Number of QBs to Draft']
    Number_of_RBs = draft_count['Number of RBs to Draft']
    Number_of_WRs = draft_count['Number of WRs to Draft']
    Number_of_TEs = draft_count['Number of TEs to Draft']

    # Initialize Positions_Remaining only if it hasn't been set before
    if not st.session_state.Positions_Remaining:
        st.session_state.Positions_Remaining = [Number_of_QBs, Number_of_RBs, Number_of_WRs, Number_of_TEs]
    
    # Break the data list into positional lists
    QBs = list(data['QB'])
    RBs = list(data['RB'])
    WRs = list(data['WR'])
    TEs = list(data['TE'])

    # Initialize Team
    My_QBs = st.session_state.My_QBs
    if My_QBs == []:
        My_QBs = [' '] * Number_of_QBs
    My_RBs = st.session_state.My_RBs
    if My_RBs == []:
        My_RBs = [' '] * Number_of_RBs
    My_WRs = st.session_state.My_WRs
    if My_WRs == []:
        My_WRs = [' '] * Number_of_WRs
    My_TEs = st.session_state.My_TEs
    if My_TEs == []:
        My_TEs = [' '] * Number_of_TEs
    
    # Initialize Pop Up Window Variables
    if 'popup_open' not in st.session_state:
        st.session_state.popup_open = False
    if 'draft_triggered' not in st.session_state:
        st.session_state.draft_triggered = False

    # Button Click
    if st.button("Draft a Player", use_container_width=True):
        st.session_state.popup_open = True       

    # Display the popup if it's open, and modify the board based on the results
    if st.session_state.popup_open:
        print(st.session_state.Positions_Remaining)
        show_popup(data, QBs, RBs, WRs, TEs, st.session_state.Positions_Remaining, league_size)

    # Process the drafted player after the popup is closed
    if st.session_state.get('draft_triggered', False):
        Player_Name = st.session_state.player_name
        Player_Position = st.session_state.player_position
        Player_Points = st.session_state.player_points
        Player_Team = st.session_state.player_team 
        Player_ADP = st.session_state.player_ADP 
        # Delete Drafted Player from board
        for key in data:
            for idx, player_tuple in enumerate(data[key]):
                if Player_Name == player_tuple[0]:
                    data[key].pop(idx)  # Remove the player
                    st.session_state.data = data
                    break                  
        # Append the drafted player's name to the added_players list
        added_players.append(Player_Name)
        recently_added_players.append((Player_Name, Player_Position, Player_Points, Player_Team, Player_ADP))
        # Update the remaining positions list with new player, and add player to "My Team List"
        if Player_Position == 'QB':
            st.session_state.Positions_Remaining[0] -= 1
            for i in range(len(My_QBs)):
                if My_QBs[i] == ' ':
                    My_QBs[i] = Player_Name
                    st.session_state.My_QBs = My_QBs
                    break
        elif Player_Position == 'RB':
            st.session_state.Positions_Remaining[1] -= 1
            for i in range(len(My_RBs)):
                if My_RBs[i] == ' ':
                    My_RBs[i] = Player_Name
                    st.session_state.My_RBs = My_RBs
                    break
        elif Player_Position == 'WR':
            st.session_state.Positions_Remaining[2] -= 1
            for i in range(len(My_WRs)):
                if My_WRs[i] == ' ':
                    My_WRs[i] = Player_Name
                    st.session_state.My_WRs = My_WRs
                    break
        elif Player_Position == 'TE':
            st.session_state.Positions_Remaining[3] -= 1
            for i in range(len(My_TEs)):
                if My_TEs[i] == ' ':
                    My_TEs[i] = Player_Name
                    st.session_state.My_TEs = My_TEs
                    break

        # Reset the draft trigger flag
        st.session_state.draft_triggered = False

    # Display the saved input value - don't need but saved to reference on how to call the variable
    # st.write("Saved Input Value:", st.session_state.input_value)

    ### Undo Options 
    col1, col2 = st.columns(2)     
    with col1:
        if st.button("Undo Your Pick", use_container_width=True):
            if recently_added_players:  # Check if there are players to undo
                last_drafted_player = recently_added_players.pop()  # Get the last drafted player
                player_name = last_drafted_player[0]  # Player name
                player_position = last_drafted_player[1]  # Player position
                player_season_points = float(last_drafted_player[2])  # Convert points to float for comparison
                
                my_players = [My_QBs, My_RBs, My_WRs, My_TEs]
                
                # Check if the last drafted player is in any of the my_players lists
                if player_name not in My_QBs and player_name not in My_RBs and player_name not in My_WRs and player_name not in My_TEs:
                    st.warning(f"{player_name} is not on your team. Use the Undo Board Pick button.")
                    # Optionally, you can push back the last drafted player to recently_added_players
                    recently_added_players.append(last_drafted_player)  # Add it back so it can be undone later
                else:
                    # Add the player back to the data
                    position_list = st.session_state.data[player_position]
                    
                    # Find the correct index to insert the player
                    insert_index = 0
                    for index, player in enumerate(position_list):
                        if float(player[2]) < player_season_points:  # Compare projected points
                            insert_index = index
                            break
                        insert_index = index + 1  # If we don't break, we insert at the end
    
                    # Insert the player back to the correct position in the list
                    position_list.insert(insert_index, (player_name, player_position, last_drafted_player[2], last_drafted_player[3], last_drafted_player[4]))
                    
                    # Update the session state with the modified position list
                    st.session_state.data[player_position] = position_list
                    
                    # Remove the player from the user's team and replace with a blank term
                    if player_position == 'QB':
                        index = My_QBs.index(player_name)  # Find the index of the drafted player
                        My_QBs[index] = ' '  # Replace the drafted player with a blank term
                        st.session_state.My_QBs = My_QBs
                    elif player_position == 'RB':
                        index = My_RBs.index(player_name)
                        My_RBs[index] = ' '
                        st.session_state.My_RBs = My_RBs
                    elif player_position == 'WR':
                        index = My_WRs.index(player_name)
                        My_WRs[index] = ' '
                        st.session_state.My_WRs = My_WRs
                    elif player_position == 'TE':
                        index = My_TEs.index(player_name)
                        My_TEs[index] = ' '
                        st.session_state.My_TEs = My_TEs
    
                    st.success(f"Successfully undid your pick of {player_name}.")
            else:
                st.warning("No picks to undo.")
                
    with col2:
        if st.button("Undo Board Pick", use_container_width=True):
            if recently_deleted_players:
                last_removed_player = recently_deleted_players.pop()  # Get the last drafted player
                player_name = last_removed_player[0]  # Player name
                player_position = last_removed_player[1]  # Player position
                player_season_points = float(last_removed_player[2])  # Convert points to float for comparison
                
                #if player is in My_{position} list, then return st.warning("Last player off board was drafted by you, please use the undo draft pick button")
                my_players = [My_QBs, My_RBs, My_WRs, My_TEs]
                check_for_player = False
                for player_check in my_players:
                    # Check if the term exists in the current list
                    if player_name in player_check:
                        check_for_player = True
                        
                
                if check_for_player == True:
                    st.warning("Last player off board was drafted by you, please use the undo draft pick button")
                
                else:                
                    # Get the list of players for the specific position
                    position_list = st.session_state.data[player_position]
                    
                    # Find the correct index to insert the player
                    insert_index = 0
                    for index, player in enumerate(position_list):
                        if float(player[2]) < player_season_points:  # Compare projected points
                            insert_index = index
                            break
                        insert_index = index + 1  # If we don't break, we insert at the end
        
                    # Insert the player back to the correct position in the list
                    position_list.insert(insert_index, (player_name, player_position, last_removed_player[2], last_removed_player[3], last_removed_player[4]))
        
                    # Update the session state with the modified position list
                    st.session_state.data[player_position] = position_list
                    
                    st.success(f"Successfully undid board pick of {player_name}.")
            else:
                st.warning("No picks to undo.")


    col3, col4 = st.columns(2)
    ### Manually Draft Player Text Input
    with col3:
        def submit1():
            st.session_state.drafted_player = st.session_state.widget1
            st.session_state.widget1 = ''
            st.session_state.button_pressed_draft = True  # Set button pressed to True when input is submitted
    
        drafted_player = st.text_input("Manually Draft Player:", key='widget1', on_change=submit1)
    
        drafted_player = st.session_state.drafted_player
        if st.session_state.get('button_pressed_draft', False):  # Check if the input was activated
            drafted_player_position = 'Not Found'
            for key in data:
                for idx, player_tuple in enumerate(data[key]):
                    if drafted_player.lower() == player_tuple[0].lower():  # Case insensitive comparison
                        drafted_player_position = player_tuple[1]  # Get the position
                        deleted_player = data[key].pop(idx)  # Remove and retrieve the player
                        break  # Exit the loop since the player is found
    
            # Update the remaining positions list with new player, and add player to "My Team List"
            if drafted_player_position == 'QB':
                st.session_state.Positions_Remaining[0] -= 1
                for i in range(len(My_QBs)):
                    if My_QBs[i] == ' ':
                        My_QBs[i] = drafted_player
                        st.session_state.My_QBs = My_QBs
                        recently_added_players.append((drafted_player, drafted_player_position, deleted_player[2], deleted_player[3], deleted_player[4]))
                        break
            elif drafted_player_position == 'RB':
                st.session_state.Positions_Remaining[1] -= 1
                for i in range(len(My_RBs)):
                    if My_RBs[i] == ' ':
                        My_RBs[i] = drafted_player
                        st.session_state.My_RBs = My_RBs
                        recently_added_players.append((drafted_player, drafted_player_position, deleted_player[2], deleted_player[3], deleted_player[4]))
                        break
            elif drafted_player_position == 'WR':
                st.session_state.Positions_Remaining[2] -= 1
                for i in range(len(My_WRs)):
                    if My_WRs[i] == ' ':
                        My_WRs[i] = drafted_player
                        st.session_state.My_WRs = My_WRs
                        recently_added_players.append((drafted_player, drafted_player_position, deleted_player[2], deleted_player[3], deleted_player[4]))
                        break
            elif drafted_player_position == 'TE':
                st.session_state.Positions_Remaining[3] -= 1
                for i in range(len(My_TEs)):
                    if My_TEs[i] == ' ':
                        My_TEs[i] = drafted_player
                        st.session_state.My_TEs = My_TEs
                        recently_added_players.append((drafted_player, drafted_player_position, deleted_player[2], deleted_player[3], deleted_player[4]))
                        break
            elif drafted_player_position == 'Not Found':
                st.error("Player Not Found in Draft Board")

            # Reset the button pressed state after checking
            st.session_state.button_pressed_draft = False
    
    ### Manually Remove Player Text Input
    with col4:
        def submit2():
            st.session_state.removed_player = st.session_state.widget2
            st.session_state.widget2 = ''
            st.session_state.button_pressed_remove = True  # Set button pressed to True when input is submitted
    
        removed_player = st.text_input("Manually Remove Player From Board:", key='widget2', on_change=submit2)
    
        removed_player = st.session_state.removed_player
        if st.session_state.get('button_pressed_remove', False):  # Check if the input was activated
            player_found = False
            for key in data:
                for idx, player_tuple in enumerate(data[key]):
                    if removed_player.lower() == player_tuple[0].lower():  # Case insensitive comparison
                        deleted_player = data[key].pop(idx)  # Remove the player
                        st.session_state.data = data
                        player_found = True
                        recently_deleted_players.append((removed_player, deleted_player[1], deleted_player[2], deleted_player[3], deleted_player[4]))
                        st.session_state.recently_deleted_players = recently_deleted_players
                        break
    
            if not player_found:
                st.error("Player Not Found in Draft Board")
    
            # Reset the button pressed state after checking
            st.session_state.button_pressed_remove = False



    ### Player Buttons
    cola, colb = st.columns(2)
    
    with cola:
        for position in ['RB', 'QB']:
            available_players = data[position][:4]  # Get the top 4 players for this position
            st.markdown(f'<div class="player-section" style="text-align: center;">Next {position}s</div>', unsafe_allow_html=True)
            for player in available_players:
                player_name = player[0]
                if st.button(player_name, key=player_name, use_container_width=True):
                    # Delete Drafted Player from board
                    for key in data:
                        for idx, player_tuple in enumerate(data[key]):
                            if player_name == player_tuple[0]:
                                deleted_player = data[key].pop(idx)  # Remove the player
                                removed_player = player_name
                                st.session_state.data = data
                                recently_deleted_players.append((removed_player, deleted_player[1], deleted_player[2], deleted_player[3], deleted_player[4]))
                                st.session_state.recently_deleted_players = recently_deleted_players
                                st.rerun()
                                break     
    
    with colb:
        for position in ['WR', 'TE']:
            available_players = data[position][:4]  # Get the top 4 players for this position
            st.markdown(f'<div class="player-section" style="text-align: center;">Next {position}s</div>', unsafe_allow_html=True)
            for player in available_players:
                player_name = player[0]
                if st.button(player_name, key=player_name, use_container_width=True):
                    # Delete Drafted Player from board
                    for key in data:
                        for idx, player_tuple in enumerate(data[key]):
                            if player_name == player_tuple[0]:
                                deleted_player = data[key].pop(idx)  # Remove the player
                                removed_player = player_name
                                st.session_state.data = data
                                recently_deleted_players.append((removed_player, deleted_player[1], deleted_player[2], deleted_player[3], deleted_player[4]))
                                st.session_state.recently_deleted_players = recently_deleted_players
                                st.rerun()
                                break   

    # Sidebar - Team Selection
    st.sidebar.markdown('<div class="section-header">Your Team</div>', unsafe_allow_html=True)
    
    # Define a list of positions to iterate over
    positions = ['QB', 'RB', 'WR', 'TE']
    
    # Iterate over each position and display the corresponding players
    for position in positions:
        st.sidebar.markdown(f'<div class="player-section">{position}s</div>', unsafe_allow_html=True)
        
        # Get the list of players for the current position
        my_players = st.session_state.get(f'My_{position}s', [])
        
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
