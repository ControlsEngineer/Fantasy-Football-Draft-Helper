def WR_Selector(data,WRs,league_size):
    ## This function evaluates the average value of remaining Tight Ends and the value over replacement of the top remaining Tight End
    ## Value of replacement includes three variables - average projected score of top all players in that position in the top 100 players, the projected score of 
    ## the positional player right before the current top player, and the projected score of the positional player right after the current top player
    ## Take the average of those three values to get the Value of Replacement variable
    
    from statistics import mean 
    
    VOR = league_size*2 #Value over replacement, used for averaging replacement value below. Set to *1 for QBs and TEs, *2 for RBs and WRs
    
    # CSV numbers import as strings. Convert projected points to float
    WRs = [(player, position, float(points), team, adp) for player, position, points, team, adp in WRs]


    #Find highest ranked WR remaining on overall list, and determine their rank
    # data_length = len(data)
    # WRs_length = len(WRs)
    WR_Name = ''
    for i in range(len(data['WR'])):   
        x = i
        WR_Name = data['WR'][i][0]
        WR_Points = data['WR'][i][2]
        WR_Team = data['WR'][i][3]
        WR_ADP = data['WR'][i][4]
        break

    for i in range(len(data['WR'])): 
        if data['WR'][x][0] == data['WR'][i][0]:
            Rank = i

    #Average the WRs from the next VOR amount of players list        
    Next_VOR_WRs = []
    for i in range(VOR):
        if data['WR'][i][1] == 'WR':
            Next_VOR_WRs.append(float(data['WR'][i][2]))
    WR_average = sum(Next_VOR_WRs)/len(Next_VOR_WRs)
    
    #Calculate the replacement value
    if Rank == 0:
        WR_RankUp = float(data['WR'][0][2])
        WR_RankDown = float(data['WR'][1][2])
        WR_data = (WR_average,WR_RankDown,WR_RankUp)
        WR_Replacement_Value = mean(WR_data)
    else:
        for i in range(len(data['WR'])):
            if WR_Name == data['WR'][i][0]:
                WR_RankUp = float(data['WR'][i-1][2])
                WR_RankDown = float(data['WR'][i+1][2])
                WR_data = (WR_average,WR_RankDown,WR_RankUp)
                WR_Replacement_Value = mean(WR_data)
    
    # Calculate the value of replacement
    WR_Value_Over_Replacement = float(data['WR'][Rank][2]) - WR_Replacement_Value
    
    return (WR_Name,WR_Points,WR_Team,WR_ADP,WR_Value_Over_Replacement,WR_Replacement_Value)