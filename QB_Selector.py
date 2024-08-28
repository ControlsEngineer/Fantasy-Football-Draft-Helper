def QB_Selector(data,QBs,league_size):
    ## This function evaluates the average value of remaining Tight Ends and the value over replacement of the top remaining Tight End
    ## Value of replacement includes three variables - average projected score of top all players in that position in the top 100 players, the projected score of 
    ## the positional player right before the current top player, and the projected score of the positional player right after the current top player
    ## Take the average of those three values to get the Value of Replacement variable
    
    from statistics import mean 
    
    VOR = league_size*1 #Value over replacement, used for averaging replacement value below. Set to *1 for QBs and TEs, *2 for RBs and WRs
    
    # CSV numbers import as strings. Convert projected points to float
    QBs = [(player, position, float(points), team, adp) for player, position, points, team, adp in QBs]


    #Find highest ranked QB remaining on overall list, and determine their rank
    # data_length = len(data)
    # QBs_length = len(QBs)
    QB_Name = ''
    for i in range(len(data['QB'])):   
        x = i
        QB_Name = data['QB'][i][0]
        QB_Points = data['QB'][i][2]
        QB_Team = data['QB'][i][3]
        QB_ADP = data['QB'][i][4]
        break

    for i in range(len(data['QB'])): 
        if data['QB'][x][0] == data['QB'][i][0]:
            Rank = i

    #Average the QBs from the next VOR amount of players list        
    Next_VOR_QBs = []
    for i in range(VOR):
        if data['QB'][i][1] == 'QB':
            Next_VOR_QBs.append(float(data['QB'][i][2]))
    QB_average = sum(Next_VOR_QBs)/len(Next_VOR_QBs)
    
    #Calculate the replacement value
    if Rank == 0:
        QB_RankUp = float(data['QB'][0][2])
        QB_RankDown = float(data['QB'][1][2])
        QB_data = (QB_average,QB_RankDown,QB_RankUp)
        QB_Replacement_Value = mean(QB_data)
    else:
        for i in range(len(data['QB'])):
            if QB_Name == data['QB'][i][0]:
                QB_RankUp = float(data['QB'][i-1][2])
                QB_RankDown = float(data['QB'][i+1][2])
                QB_data = (QB_average,QB_RankDown,QB_RankUp)
                QB_Replacement_Value = mean(QB_data)
    
    # Calculate the value of replacement
    QB_Value_Over_Replacement = float(data['QB'][Rank][2]) - QB_Replacement_Value
    
    return (QB_Name,QB_Points,QB_Team,QB_ADP,QB_Value_Over_Replacement,QB_Replacement_Value)