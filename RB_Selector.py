def RB_Selector(data,RBs,league_size):
    ## This function evaluates the average value of remaining Tight Ends and the value over replacement of the top remaining Tight End
    ## Value of replacement includes three variables - average projected score of top all players in that position in the top 100 players, the projected score of 
    ## the positional player right before the current top player, and the projected score of the positional player right after the current top player
    ## Take the average of those three values to get the Value of Replacement variable
    
    from statistics import mean 
    
    VOR = league_size*2 #Value over replacement, used for averaging replacement value below. Set to *1 for QBs and TEs, *2 for RBs and WRs
    
    # CSV numbers import as strings. Convert projected points to float
    RBs = [(player, position, float(points), team, adp) for player, position, points, team, adp in RBs]


    #Find highest ranked RB remaining on overall list, and determine their rank
    # data_length = len(data)
    # RBs_length = len(RBs)
    RB_Name = ''
    for i in range(len(data['RB'])):   
        x = i
        RB_Name = data['RB'][i][0]
        RB_Points = data['RB'][i][2]
        RB_Team = data['RB'][i][3]
        RB_ADP = data['RB'][i][4]
        break

    for i in range(len(data['RB'])): 
        if data['RB'][x][0] == data['RB'][i][0]:
            Rank = i

    #Average the RBs from the next VOR amount of players list        
    Next_VOR_RBs = []
    for i in range(VOR):
        if data['RB'][i][1] == 'RB':
            Next_VOR_RBs.append(float(data['RB'][i][2]))
    RB_average = sum(Next_VOR_RBs)/len(Next_VOR_RBs)
    
    #Calculate the replacement value
    if Rank == 0:
        RB_RankUp = float(data['RB'][0][2])
        RB_RankDown = float(data['RB'][1][2])
        RB_data = (RB_average,RB_RankDown,RB_RankUp)
        RB_Replacement_Value = mean(RB_data)
    else:
        for i in range(len(data['RB'])):
            if RB_Name == data['RB'][i][0]:
                RB_RankUp = float(data['RB'][i-1][2])
                RB_RankDown = float(data['RB'][i+1][2])
                RB_data = (RB_average,RB_RankDown,RB_RankUp)
                RB_Replacement_Value = mean(RB_data)
    
    # Calculate the value of replacement
    RB_Value_Over_Replacement = float(data['RB'][Rank][2]) - RB_Replacement_Value
    
    return (RB_Name,RB_Points,RB_Team,RB_ADP,RB_Value_Over_Replacement,RB_Replacement_Value)