def TE_Selector(data,TEs,league_size):
    ## This function evaluates the average value of remaining Tight Ends and the value over replacement of the top remaining Tight End
    ## Value of replacement includes three variables - average projected score of top all players in that position in the top 100 players, the projected score of 
    ## the positional player right before the current top player, and the projected score of the positional player right after the current top player
    ## Take the average of those three values to get the Value of Replacement variable
    
    from statistics import mean 
    
    VOR = league_size*1 #Value over replacement, used for averaging replacement value below. Set to *1 for QBs and TEs, *2 for RBs and WRs
    
    # CSV numbers import as strings. Convert projected points to float
    TEs = [(player, position, float(points), team, adp) for player, position, points, team, adp in TEs]


    #Find highest ranked TE remaining on overall list, and determine their rank
    # data_length = len(data)
    # TEs_length = len(TEs)
    TE_Name = ''
    for i in range(len(data['TE'])):   
        x = i
        TE_Name = data['TE'][i][0]
        TE_Points = data['TE'][i][2]
        TE_Team = data['TE'][i][3]
        TE_ADP = data['TE'][i][4]
        break

    for i in range(len(data['TE'])): 
        if data['TE'][x][0] == data['TE'][i][0]:
            Rank = i

    #Average the TEs from the next VOR amount of players list        
    Next_VOR_TEs = []
    for i in range(VOR):
        if data['TE'][i][1] == 'TE':
            Next_VOR_TEs.append(float(data['TE'][i][2]))
    TE_average = sum(Next_VOR_TEs)/len(Next_VOR_TEs)
    
    #Calculate the replacement value
    if Rank == 0:
        TE_RankUp = float(data['TE'][0][2])
        TE_RankDown = float(data['TE'][1][2])
        TE_data = (TE_average,TE_RankDown,TE_RankUp)
        TE_Replacement_Value = mean(TE_data)
    else:
        for i in range(len(data['TE'])):
            if TE_Name == data['TE'][i][0]:
                TE_RankUp = float(data['TE'][i-1][2])
                TE_RankDown = float(data['TE'][i+1][2])
                TE_data = (TE_average,TE_RankDown,TE_RankUp)
                TE_Replacement_Value = mean(TE_data)
    
    # Calculate the value of replacement
    TE_Value_Over_Replacement = float(data['TE'][Rank][2]) - TE_Replacement_Value
    
    return (TE_Name,TE_Points,TE_Team,TE_ADP,TE_Value_Over_Replacement,TE_Replacement_Value)