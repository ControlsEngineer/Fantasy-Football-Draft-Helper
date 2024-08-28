def Player_selector(data, QBs, RBs, WRs, TEs, Positions_Remaining,league_size):
    ## This function will determine the best player to draft
    ## Method: Select the top player, and fill the remaining draft spots with value of replacement for the respective position
    ## Compare which top positional player will give you the highest points
    
    ## Import the functions
    from QB_Selector import QB_Selector
    from RB_Selector import RB_Selector
    from WR_Selector import WR_Selector
    from TE_Selector import TE_Selector
    
    # ## Call the functions 
    QB_Name, QB_Points, QB_Team, QB_ADP, QB_Value_Over_Replacement, QB_Replacement_Value = QB_Selector(data,QBs,league_size)
    RB_Name, RB_Points, RB_Team, RB_ADP, RB_Value_Over_Replacement, RB_Replacement_Value = RB_Selector(data,RBs,league_size)
    WR_Name, WR_Points, WR_Team, WR_ADP, WR_Value_Over_Replacement, WR_Replacement_Value = WR_Selector(data,WRs,league_size)
    TE_Name, TE_Points, TE_Team, TE_ADP, TE_Value_Over_Replacement, TE_Replacement_Value = TE_Selector(data,TEs,league_size)

    # 1. Determine positional needs using list indices
    positional_weights = {
        'QB': Positions_Remaining[0] / league_size,
        'RB': Positions_Remaining[1] / league_size,
        'WR': Positions_Remaining[2] / league_size,
        'TE': Positions_Remaining[3] / league_size
    }

    # 2. Weight VOR by positional needs
    weighted_values = {
        'QB': QB_Value_Over_Replacement * positional_weights['QB'],
        'RB': RB_Value_Over_Replacement * positional_weights['RB'],
        'WR': WR_Value_Over_Replacement * positional_weights['WR'],
        'TE': TE_Value_Over_Replacement * positional_weights['TE']
    }

    # 3. Find the position with the highest weighted VOR
    best_position = max(weighted_values, key=weighted_values.get)
    
    # Case 1: QB Select:
    if best_position == 'QB':
        Player_Name = QB_Name
        Player_Position = 'QB'
        Player_Points = QB_Points
        Player_Team = QB_Team
        Player_ADP = QB_ADP
    # Case 2: RB Select:
    elif best_position == 'RB':
        Player_Name = RB_Name
        Player_Position = 'RB'
        Player_Points = RB_Points
        Player_Team = RB_Team
        Player_ADP = RB_ADP
    # Case 3: WR Select:
    elif best_position == 'WR':
        Player_Name = WR_Name
        Player_Position = 'WR'
        Player_Points = WR_Points
        Player_Team = WR_Team
        Player_ADP = WR_ADP
    # Case 4: TE Select:
    elif best_position == 'TE':
        Player_Name = TE_Name
        Player_Position = 'TE'
        Player_Points = TE_Points
        Player_Team = TE_Team
        Player_ADP = TE_ADP

    return(Player_Name,Player_Position,Player_Points,Player_Team, Player_ADP)
    
    
    
    
    
    
    
    