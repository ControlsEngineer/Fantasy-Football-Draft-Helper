## This is my Draft Optimization Tool for the 2023 Fantasy Football Draft
## Must be used with a CSV file of player season-long point projections

## Import Modules
import csv
from statistics import mean
from Player_Selector import *
import PySimpleGUI as sg

## Create Initial GUI to give owner Draft Options
sg.theme('DarkGrey5')   # Add a touch of color

initial_layout = [
    [sg.Text('Customize Your Draft Settings', font=('Helvetica', 16), justification='center')],
    [sg.Text('_' * 80, justification='center')],

                    [sg.Text(' ')],
                    [sg.Text('League Size:                 '), sg.Combo([8, 10, 12], default_value=8, key='league_size')],
                    [sg.Text(' ', font=('AnyFontName', 3))],
                    [sg.Text('Scoring Format:             '), sg.Button('Standard',key='Standard',button_color=('black', 'gray'), size=(10,1)), sg.Button('0.5 PPR',key='0.5 PPR',button_color=('black', 'gray'),size=(10,1)), sg.Button('PPR',key='PPR',button_color=('black', 'gray'),size=(10,1)),],
                    [sg.Text('-' * 50)],
                    [sg.Text(' ')],
                    [sg.Text('Number of QBs desired: '), sg.Combo([1, 2], default_value=2, key='Number_of_QBs')],
                    [sg.Text('Number of RBs desired: '), sg.Combo([3, 4, 5], default_value=5, key='Number_of_RBs')], 
                    [sg.Text('Number of WRs desired:'), sg.Combo([3, 4, 5], default_value=5, key='Number_of_WRs')], 
                    [sg.Text('Number of TEs desired: '), sg.Combo([1, 2], default_value=1, key='Number_of_TEs')],
                    [sg.Text(' ')],
                    [sg.Button('Ok',bind_return_key=True)] ]



initial_window = sg.Window('Fantasy Football Draft Aid 2023', initial_layout)
# Event Loop to process "events" and get the "values" of the inputs
scoring_format = 0

recently_added_players = []  # List to keep track of players added by the user in order
recently_deleted_players_from_board = []  # Stack to keep track of players deleted from the board
while True:
    initial_event, initial_values = initial_window.read()
    if initial_event == sg.WIN_CLOSED:
        initial_window.close()
        break
    if initial_event == 'Standard':
        scoring_format = 'player_rankings_standard.csv'
        initial_window.find_element('Standard').Update(button_color=('black', 'yellow'))
        initial_window.find_element('0.5 PPR').Update(button_color=('black', 'gray'))
        initial_window.find_element('PPR').Update(button_color=('black', 'gray'))
    if initial_event == '0.5 PPR':
        scoring_format = 'player_rankings_half_PPR.csv'
        initial_window.find_element('0.5 PPR').Update(button_color=('black', 'yellow'))
        initial_window.find_element('PPR').Update(button_color=('black', 'gray'))
        initial_window.find_element('Standard').Update(button_color=('black', 'gray'))
    if initial_event == 'PPR':
        scoring_format = 'player_rankings_PPR.csv'
        initial_window.find_element('PPR').Update(button_color=('black', 'yellow'))
        initial_window.find_element('0.5 PPR').Update(button_color=('black', 'gray'))
        initial_window.find_element('Standard').Update(button_color=('black', 'gray'))
    if initial_event == 'Ok':
        if scoring_format == 0:
            sg.popup_error('Please Select a Scoring Format')
        else:
            league_size = int(initial_values['league_size'])
            Number_of_QBs = int(initial_values['Number_of_QBs'])
            Number_of_RBs = int(initial_values['Number_of_RBs'])
            Number_of_WRs = int(initial_values['Number_of_WRs'])
            Number_of_TEs = int(initial_values['Number_of_TEs'])
            break


initial_window.close()
## Open CSV file with {player, position, projected points, Team, and ADP}, and convert it to a list
data = {'QB': [], 'RB': [], 'WR': [], 'TE': []}

with open(scoring_format, newline='', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for player, position, points, team, adp in list(reader):
        if position in data:
            data[position].append((player, position, points, team, adp))


## Number of players from each position left to draft, ie 2 QBs, 5 RBs, 5 WRs, 1 TE
## Order: QB,RB,WR,TE
Positions_Remaining = [Number_of_QBs,Number_of_RBs,Number_of_WRs,Number_of_TEs]
# Break the data list into positional lists
# QBs
QBs = list(data['QB'])

# RBs
RBs = list(data['RB'])

# WRs
WRs = list(data['WR'])

# TEs
TEs = list(data['TE'])

# Initialize Team
spacing = 50
My_QBs = []
My_RBs = []
My_WRs = []
My_TEs = []

for i in range(Number_of_QBs):
    My_QBs.append(' '*spacing)
for i in range(Number_of_RBs):
    My_RBs.append(' '*spacing)
for i in range(Number_of_WRs):
    My_WRs.append(' '*spacing)
for i in range(Number_of_TEs):
    My_TEs.append(' '*spacing)

## Create the Draft Tool GUI
# All the stuff inside your window.
def create_grid_layout(data):
    #Create a grid layout for the right-hand side of the main window.
    grid_layout = []
    grid_layout.append([sg.Text(' ')])
    grid_layout.append([sg.Text(' ')])
    grid_layout.append([sg.Text(' ')])
    grid_layout.append([sg.Text(' ')])
    grid_layout.append([sg.Text(' ')])
    grid_layout.append([sg.Text(' ')])
    
    positions_col1 = [('RB', 'Running Backs'), ('QB', 'Quarterbacks')]
    positions_col2 = [('WR', 'Wide Receivers'), ('TE', 'Tight Ends')]
    col1_layout = []

    col2_layout = []
    # Create layout for column 1
    for pos, display_name in positions_col1:
        col1_layout.append([sg.Text(display_name, font=('Helvetica', 14, 'bold'), size=(15, 1), pad=(5,5))])

        for player_tuple in data[pos][:4]:
            player, position, points, team, adp = player_tuple
            button_text = f"{player}\n{team}"
            col1_layout.append([sg.Button(button_text, key=f"PLAYER_{player}", size=(20, 2))])
    # Create layout for column 2
    for pos, display_name in positions_col2:
        col2_layout.append([sg.Text(display_name, font=('Any', 15, 'bold'))])
        for player_tuple in data[pos][:4]:
            player, position, points, team, adp = player_tuple
            button_text = f"{player}\n{team}"
            col2_layout.append([sg.Button(button_text, key=f"PLAYER_{player}", size=(20, 2))])
    grid_layout.append([sg.Column(col1_layout), sg.Column(col2_layout)])
    return grid_layout
    # Create layout for column 2
    for pos, display_name in positions_col2:
        col2_layout.append([sg.Text(display_name, font=('Any', 15, 'bold'))])
        for player_tuple in data[pos]:
            player, position, points, team, adp = player_tuple
            button_text = f"{player}\n{team}"
            col2_layout.append([sg.Button(button_text, key=f"PLAYER_{player}", size=(20, 2))])
    grid_layout.append([sg.Column(col1_layout), sg.Column(col2_layout)])
    return grid_layout
    # Create layout for column 2
    for pos, display_name in positions_col2:
        col2_layout.append([sg.Text(display_name, font=('Any', 15, 'bold'))])
        for player_tuple in data[pos]:
            player, position, points, team, adp = player_tuple
            button_text = f"{player}\n{team}"
            col2_layout.append([sg.Button(button_text, key=f"PLAYER_{player}", size=(20, 2))])
            grid_layout.append([sg.Column(col1_layout), sg.Column(col2_layout)])
            return grid_layout
            row_layout.append(sg.Button(button_text, key=f"PLAYER_{player}", size=(20, 2)))
        if idx % 2 == 1 or idx == len(positions) - 1:
            grid_layout.append(row_layout)
            row_layout = []
    return grid_layout

#Create Positional Layouts for GUI

RB_layout = []
for i in range(len(My_RBs)):
    RB_layout.append([sg.Text(f"{i+1}. ", font=('Helvetica', 12), size=(5, 1), pad=(3,3)), 
                      sg.Text(My_RBs[i], font=('Helvetica', 12), key=f'RB_{i+1}', size=(25, 1), pad=(3,3))])


WR_layout = []
for i in range(len(My_WRs)):
    WR_layout.append([sg.Text(f"{i+1}. ", font=('Helvetica', 12), size=(5, 1), pad=(3,3)), 
                      sg.Text(My_WRs[i], font=('Helvetica', 12), key=f'WR_{{i+1}}', size=(25, 1), pad=(3,3))])


QB_layout = []
for i in range(len(My_QBs)):
    QB_layout.append([sg.Text(f"{i+1}. ", font=('Helvetica', 12), size=(5, 1), pad=(3,3)), 
                      sg.Text(My_QBs[i], font=('Helvetica', 12), key=f'QB_{{i+1}}', size=(25, 1), pad=(3,3))])


TE_layout = []
for i in range(len(My_TEs)):
    TE_layout.append([sg.Text(f"{i+1}. ", font=('Helvetica', 12), size=(5, 1), pad=(3,3)), 
                      sg.Text(My_TEs[i], font=('Helvetica', 12), key=f'TE_{{i+1}}', size=(25, 1), pad=(3,3))])

    
# Global list to hold player names added to the left_column
added_players = []
# Function to update the "left column" when the window is refreshed for players
def create_left_column():
    """
    Generate a new left_column layout, preserving player names added in previous iterations.
    """
    
    #Create Positional Layouts for GUI
    RB_layout = []
    for i in range(len(My_RBs)):
        RB_layout.append([sg.Text(f"{i+1}. ", font=('Helvetica', 12), size=(5, 1), pad=(3,3)), 
                          sg.Text(My_RBs[i], font=('Helvetica', 12), key=f'RB_{{i+1}}', size=(25, 1), pad=(3,3))])
        WR_layout = []
    for i in range(len(My_WRs)):
        WR_layout.append([sg.Text(f"{i+1}. ", font=('Helvetica', 12), size=(5, 1), pad=(3,3)), 
                          sg.Text(My_WRs[i], font=('Helvetica', 12), key=f'WR_{{i+1}}', size=(25, 1), pad=(3,3))])
        QB_layout = []
    for i in range(len(My_QBs)):
        QB_layout.append([sg.Text(f"{i+1}. ", font=('Helvetica', 12), size=(5, 1), pad=(3,3)), 
                          sg.Text(My_QBs[i], font=('Helvetica', 12), key=f'QB_{{i+1}}', size=(25, 1), pad=(3,3))])
        TE_layout = []
    for i in range(len(My_TEs)):
        TE_layout.append([sg.Text(f"{i+1}. ", font=('Helvetica', 12), size=(5, 1), pad=(3,3)), 
                          sg.Text(My_TEs[i], font=('Helvetica', 12), key=f'TE_{{i+1}}', size=(25, 1), pad=(3,3))])
    
    # Base layout with placeholder
    left_column = [[sg.Text(' ')],
                   [sg.Text(' ')],
                   [sg.Button('Draft a Player', size=(30, 1))],
                   [sg.Button('Undo Your Pick', size=(14, 1)), sg.Button('Undo Board Pick', size=(14, 1))],
                   [sg.Button('Search Player: '), sg.InputText(key='-SEARCH-', size=(20,1))],
                   [sg.Text(' ')],
                   [sg.Text(' ')], 
                   [sg.Text('Your Team:')],
                   [sg.Text('-' * 25), sg.Text(' ' * 50)],
                   [sg.Text('RBs:')],
                   [sg.Column(RB_layout)],
                   [sg.Text('WRs:')],
                   [sg.Column(WR_layout)],
                   [sg.Text('QBs:')],
                   [sg.Column(QB_layout)],
                   [sg.Text('TEs:')],
                   [sg.Column(TE_layout)]]
    
    return left_column

grid_layout = create_grid_layout(data) 

left_column = [[sg.Text(' ')],
               [sg.Text(' ')],
               [sg.Button('Draft a Player', size=(30, 1))],
               [sg.Button('Undo Your Pick', size=(14, 1)), sg.Button('Undo Board Pick', size=(14, 1))],
               [sg.Button('Search Player: '), sg.InputText(key='-SEARCH-', size=(20,1))],
               [sg.Text(' ')],
               [sg.Text(' ')], 
               [sg.Text('Your Team:')],
               [sg.Text('-' * 25), sg.Text(' ' * 50)],
               [sg.Text('RBs:')],
               [sg.Column(RB_layout)],
               [sg.Text('WRs:')],
               [sg.Column(WR_layout)],
               [sg.Text('QBs:')],
               [sg.Column(QB_layout)],
               [sg.Text('TEs:')],
               [sg.Column(TE_layout)]]

layout = [
    [
        sg.Column(left_column, vertical_alignment='top'), 
        sg.Frame('', [[sg.Column(grid_layout, key='-GRID-')]], key='-GRID-FRAME-', border_width=0)
    ]
]

# Create the Window
window = sg.Window('Fantasy Football Draft Aid 2023', layout, size=(800,700))
#window2_active = False
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    # Remove Custom Player
    if event == 'Search Player: ':
        player_name = values['-SEARCH-']
        # Find the player's position and remove them from the player_data
        for pos, players in data.items():
            for player, position, points, team, adp in players:
                if player == player_name:
                    recently_deleted_players_from_board.append((pos, (player, position, points, team, adp)))
                    data[pos].remove((player, position, points, team, adp))
                    break
        
    # Refresh the grid layout and update the window
    # Close the current window
    window.close()

    # Refresh the grid layout, recreate the left_column and main layout, and open a new window
    grid_layout = create_grid_layout(data)
    left_column = create_left_column()
    layout = [
        [
            sg.Column(left_column, vertical_alignment='top'), 
            sg.Frame('', [[sg.Column(grid_layout, key='-GRID-')]], key='-GRID-FRAME-', border_width=0)
        ]
    ]
    window = sg.Window('Fantasy Football Draft Aid 2023', layout)
            
    # Check if a player button was clicked
    if event.startswith("PLAYER_"):
        player_name = event.split("PLAYER_")[1]
        # Find the player's position and remove them from the player_data
        for pos, players in data.items():
            for player, position, points, team, adp in players:
                if player == player_name:
                    recently_deleted_players_from_board.append((pos, (player, position, points, team, adp)))
                    data[pos].remove((player, position, points, team, adp))
                    break
            
        # Refresh the grid layout and update the window
        # Close the current window
        window.close()
    
        # Refresh the grid layout, recreate the left_column and main layout, and open a new window
        grid_layout = create_grid_layout(data)
        left_column = create_left_column()
        layout = [
            [
                sg.Column(left_column, vertical_alignment='top'), 
                sg.Frame('', [[sg.Column(grid_layout, key='-GRID-')]], key='-GRID-FRAME-', border_width=0)
            ]
        ]
        window = sg.Window('Fantasy Football Draft Aid 2023', layout)
        
    
    if event == 'Undo Your Pick':
        # Check if there are any entries in the recently_added_players list
        # Preserve list for use
        recently_added_players_details = recently_added_players.copy()
        # Check if there are any entries in the recently_added_players list
        if recently_added_players:
            # Pop the last entry from the list
            last_added_player, player_position, player_points, player_team, player_adp = recently_added_players.pop()
            last_added_player_details = recently_added_players_details.pop()
            # Based on the player's position, remove them from the respective list
            if player_position == 'QB':
                My_QBs.remove(last_added_player)
                My_QBs.append(' '*spacing)
                data['QB'].insert(0, last_added_player_details)
            elif player_position == 'RB':
                My_RBs.remove(last_added_player)
                My_RBs.append(' '*spacing)
                data['RB'].insert(0, last_added_player_details)
            elif player_position == 'WR':
                My_WRs.remove(last_added_player)
                My_WRs.append(' '*spacing)
                data['WR'].insert(0, last_added_player_details)
            elif player_position == 'TE':
                My_TEs.remove(last_added_player)
                My_TEs.append(' '*spacing)
                data['TE'].insert(0, last_added_player_details)
        
            # Refresh the GUI
            window.close()
            grid_layout = create_grid_layout(data)
            left_column = create_left_column()
            layout = [
                [
                    sg.Column(left_column, vertical_alignment='top'), 
                    sg.Frame('', [[sg.Column(grid_layout, key='-GRID-')]], key='-GRID-FRAME-', border_width=0)
                ]
            ]
            window = sg.Window('Fantasy Football Draft Aid 2023', layout)
    if event == 'Undo Board Pick':
        # Check if there are any entries in the recently_deleted_players_from_board stack
        if recently_deleted_players_from_board:
            # Pop the top entry from the stack
            deleted_position, key = recently_deleted_players_from_board.pop()
            # Add the player back to the data dictionary under the appropriate key
            data[deleted_position].insert(0, key)
            # Refresh the GUI
            window.close()
            grid_layout = create_grid_layout(data)
            left_column = create_left_column()
            layout = [
                [
                    sg.Column(left_column, vertical_alignment='top'), 
                    sg.Frame('', [[sg.Column(grid_layout, key='-GRID-')]], key='-GRID-FRAME-', border_width=0)
                ]
            ]
            window = sg.Window('Fantasy Football Draft Aid 2023', layout)
    if event == 'Ok':
        player_name = values['input_player']
        checker = 0
        for i in range(len(data)):
            if player_name == data[i][0]:
                del data[i]
                window['input_player'].update('')
                checker = 1
                break
        if checker == 0: 
            sg.popup('Error: Not Valid Player')
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        window.close()
        break
    if event == 'Draft a Player':
        Player_Name,Player_Position,Player_Points,Player_Team,Player_ADP = Player_selector(data, QBs, RBs, WRs, TEs, Positions_Remaining, league_size)    
        decision = sg.PopupYesNo('You should draft:',Player_Name, Player_Position)
        
        if decision == 'Yes':
            #Delete Drafted Player from board
            for key in data:
                for idx, player_tuple in enumerate(data[key]):
                    if Player_Name == player_tuple[0]:
                        deleted_player = data[key].pop(idx)  # Remove and retrieve the player
                        break
                    
            # Append the drafted player's name to the added_players list
            player_name_to_add = Player_Name
            added_players.append(player_name_to_add)
            recently_added_players.append((Player_Name,Player_Position,Player_Points,Player_Team,Player_ADP))
            # Update the remaining positions list with new player, and add player to "My Team List"
            if Player_Position == 'QB':
                Positions_Remaining[0] = Positions_Remaining[0] - 1
                for i in range(len(My_QBs)):
                    if My_QBs[i] == ' '*spacing:
                        My_QBs[i] = Player_Name
                        window_key = f'QB_{i+1}'  # Construct the key dynamically, e.g., 'QB_1', 'QB_2', 'QB_3', etc.
                        window[window_key].update(My_QBs[i])
                        break
            if Player_Position == 'RB':
                Positions_Remaining[1] = Positions_Remaining[1] - 1
                for i in range(len(My_RBs)):
                    if My_RBs[i] == ' '*spacing:
                        My_RBs[i] = Player_Name
                        window_key = f'RB_{i+1}'  # Construct the key dynamically
                        window[window_key].update(My_RBs[i])
                        break
            if Player_Position == 'WR':
                Positions_Remaining[2] = Positions_Remaining[2] - 1
                for i in range(len(My_WRs)):
                    if My_WRs[i] == ' '*spacing:
                        My_WRs[i] = Player_Name
                        window_key = f'WR_{i+1}'  # Construct the key dynamically
                        window[window_key].update(My_WRs[i])
                        break
            if Player_Position == 'TE':
                Positions_Remaining[3] = Positions_Remaining[3] - 1
                for i in range(len(My_TEs)):
                    if My_TEs[i] == ' '*spacing:
                        My_TEs[i] = Player_Name
                        window_key = f'TE_{i+1}'  # Construct the key dynamically
                        window[window_key].update(My_TEs[i])
                        break
        
        if decision == 'No':
            ## Define next best at each position
            #QB:
            if Positions_Remaining[0] != 0:
                Next_QB = data['QB'][0][0]
            if Positions_Remaining[0] == 0:
                Next_QB = 'QB is full'
            #RB:
            if Positions_Remaining[1] != 0:
                Next_RB = data['RB'][0][0]
            if Positions_Remaining[1] == 0:
                Next_RB = 'RB is full'
            #WR:
            if Positions_Remaining[2] != 0:
                Next_WR = data['WR'][0][0]
            if Positions_Remaining[2] == 0:
                Next_WR = 'WR is full'
            #TE:
            if Positions_Remaining[3] != 0:
                Next_TE = data['TE'][0][0]
            if Positions_Remaining[3] == 0:
                Next_TE = 'TE is full'

            window2_active = True
            layout2 = [ [sg.Text('Who do you want to draft?')],
                        [sg.Button(Next_QB), sg.Button(Next_RB), sg.Button(Next_WR), sg.Button(Next_TE)],
                        [sg.Text(' ')],
                        [sg.Text('Manual Input: Player Name'), sg.InputText(key='input_player2')],
                        [sg.Button('Ok',bind_return_key=True)] ]
            # layout2 = [[sg.Button('Remove QB'),sg.Button('Remove RB'),sg.Button('Remove WR'),sg.Button('Remove TE')]]
            window2 = sg.Window('Manual Drafter', layout2)
            while True:
                event2, values2 = window2.Read()
                if event2 == sg.WIN_CLOSED or event2 is None:
                    window2.Close()
                    window2_active = False
                    break
                if event2 == 'Ok':
                    Player_Name2 = values2['input_player2']
                    #Delete Drafted Player from board
                    for key in data:
                        for idx, player_tuple in enumerate(data[key]):
                            if Player_Name2 == player_tuple[0]:
                                Player_Position2 = data[key][0][1]
                                deleted_player = data[key].pop(idx)  # Remove and retrieve the player

                    #Update the remaining positions list with new player
                    if Player_Position2 == 'QB':
                        Positions_Remaining[0] = Positions_Remaining[0] - 1
                        for i in range(len(My_QBs)):
                            if My_QBs[i] == ' '*spacing:
                                My_QBs[i] = Player_Name2
                                window['QB_1'].update(My_QBs[0])
                                window['QB_2'].update(My_QBs[1])
                                break
                    if Player_Position2 == 'RB':
                        Positions_Remaining[1] = Positions_Remaining[1] - 1
                        for i in range(len(My_RBs)):
                            if My_RBs[i] == ' '*spacing:
                                My_RBs[i] = Player_Name2
                                window['RB_1'].update(My_RBs[0])
                                window['RB_2'].update(My_RBs[1])
                                window['RB_3'].update(My_RBs[2])
                                window['RB_4'].update(My_RBs[3])
                                window['RB_5'].update(My_RBs[4])
                                break
                    if Player_Position2 == 'WR':
                        Positions_Remaining[2] = Positions_Remaining[2] - 1
                        for i in range(len(My_WRs)):
                            if My_WRs[i] == ' '*spacing:
                                My_WRs[i] = Player_Name2
                                window['WR_1'].update(My_WRs[0])
                                window['WR_2'].update(My_WRs[1])
                                window['WR_3'].update(My_WRs[2])
                                window['WR_4'].update(My_WRs[3])
                                window['WR_5'].update(My_WRs[4])
                                break
                    if Player_Position2 == 'TE':
                        Positions_Remaining[3] = Positions_Remaining[3] - 1
                        My_TEs[0] = Player_Name2
                        window['TE_1'].update(My_TEs[0])
                    window2.Close()
                    window2_active = False
                    break

                if event2 == Next_QB:
                    if Next_QB == 'QB is full':
                        sg.Popup('You have already selected the maximum number of QBs, select another position')
                    if Next_QB != 'QB is full':
                        Player_Name2 = Next_QB
                        #Delete Drafted Player from board
                        for key in data:
                            for idx, player_tuple in enumerate(data[key]):
                                if Player_Name2 == player_tuple[0]:
                                    deleted_player = data[key].pop(idx)  # Remove and retrieve the player

                        #Update the remaining positions list with new player
                        Positions_Remaining[0] = Positions_Remaining[0] - 1
                        for i in range(len(My_QBs)):
                            if My_QBs[i] == ' '*spacing:
                                My_QBs[i] = Player_Name2
                                window['QB_1'].update(My_QBs[0])
                                window['QB_2'].update(My_QBs[1])
                                break
                        window2.Close()
                        window2_active = False
                        break      

                if event2 == Next_RB:
                    if Next_RB == 'RB is full':
                        sg.Popup('You have already selected the maximum number of RBs, select another position')
                    if Next_RB != 'RB is full':
                        Player_Name2 = Next_RB
                        #Delete Drafted Player from board
                        for key in data:
                            for idx, player_tuple in enumerate(data[key]):
                                if Player_Name2 == player_tuple[0]:
                                    deleted_player = data[key].pop(idx)  # Remove and retrieve the player

                        #Update the remaining positions list with new player
                        Positions_Remaining[1] = Positions_Remaining[1] - 1
                        for i in range(len(My_RBs)):
                            if My_RBs[i] == ' '*spacing:
                                My_RBs[i] = Player_Name2
                                window['RB_1'].update(My_RBs[0])
                                window['RB_2'].update(My_RBs[1])
                                window['RB_3'].update(My_RBs[2])
                                window['RB_4'].update(My_RBs[3])
                                window['RB_5'].update(My_RBs[4])
                                break                
                        window2.Close()
                        window2_active = False
                        break
                
                if event2 == Next_WR:
                    if Next_WR == 'WR is full':
                        sg.Popup('You have already selected the maximum number of WRs, select another position')
                    if Next_WR != 'WR is full':
                        Player_Name2 = Next_WR
                        #Delete Drafted Player from board
                        for key in data:
                            for idx, player_tuple in enumerate(data[key]):
                                if Player_Name2 == player_tuple[0]:
                                    deleted_player = data[key].pop(idx)  # Remove and retrieve the player

                        #Update the remaining positions list with new player
                        Positions_Remaining[2] = Positions_Remaining[2] - 1  
                        for i in range(len(My_WRs)):
                            if My_WRs[i] == ' '*spacing:
                                My_WRs[i] = Player_Name2
                                window['WR_1'].update(My_WRs[0])
                                window['WR_2'].update(My_WRs[1])
                                window['WR_3'].update(My_WRs[2])
                                window['WR_4'].update(My_WRs[3])
                                window['WR_5'].update(My_WRs[4])
                                break              
                        window2.Close()
                        window2_active = False
                        break

                if event2 == Next_TE:
                    if Next_TE == 'TE is full':
                        sg.Popup('You have already selected the maximum number of TEs, select another position')
                    if Next_TE != 'TE is full':
                        Player_Name2 = Next_TE
                        #Delete Drafted Player from board
                        for key in data:
                            for idx, player_tuple in enumerate(data[key]):
                                if Player_Name2 == player_tuple[0]:
                                    deleted_player = data[key].pop(idx)  # Remove and retrieve the player

                        #Update the remaining positions list with new player
                        Positions_Remaining[3] = Positions_Remaining[3] - 1
                        My_TEs[0] = Player_Name2
                        window['TE_1'].update(My_TEs[0])                
                        window2.Close()
                        window2_active = False
                        break
                                                     
window.close()