'''
Created on Feb 20, 2013

@author: mercicle
'''

import string
import csv
from random import random,randint,choice
from datetime import date
import time

#First specify where you would like to put the cleaned file
player_output_directory = "/Users/mercicle/Desktop/CS171_Scraped_Hockey_Data/Rosters/"
player_csv_name = "all_players_cleaned.csv"

ifile  = open('/Users/mercicle/Desktop/CS171_Scraped_Hockey_Data/Rosters/all_rosters.csv')
reader = csv.reader(ifile)

#read in the data
inData = []
for row in reader:
    inData.append([ row[i] for i in range(0,len(row)) ])
     
k=0

#this will hold the cleaned data
outPlayers=[]

for this_row in inData:
    #if the name column then fix some var names and create labels for new vars
    if k==0:
        #    0           1      2         3       4      5     6     7      8      9       10            11
        #['team_id', 'Season', 'No.', 'Player', 'Pos', 'Age', 'Ht', 'Wt', 'S/C', 'Exp', 'Birth Date', 'Summary']
        
        this_row[2] = 'jersey_number'
        this_row[7] = 'weight'
        this_row[8] = 'shoots'
        this_row[9] = 'years_in_nhl'
        this_row[10] = 'DOB'
        this_row.append('date_index')   #12
        this_row.append('height')       #13
        this_row.append('handed')       #14
        #now the vars from the summary string
        this_row.append('goals')        #15
        this_row.append('assists')      #16
        this_row.append('total_points') #17
        #if goalies
        this_row.append('games_won')    #18
        this_row.append('games_lost')   #19
        this_row.append('games_tied')   #20
        this_row.append('gaa')          #21
        
    elif k>0:
        
        #make Player Name capital letters
        this_row[3] = str(this_row[3]).upper()
        
        #12 date_index
        time_struct = time.strptime(this_row[1][0:4]+"-01-01", "%Y-%m-%d") 
        this_row.insert(12,time.strftime("%m/%d/%Y",time_struct))
        
        #fix years of experience for rookies from character R to 0
        if this_row[9]=='R':
            this_row[9] = 0
        else:
            this_row[9] = int(this_row[9])
            
        #13 height in inches
        #some heights are missing so safety against ''
        if len(this_row[6])>0:
            #multiply feet by 12 inches
            p1 = int(this_row[6][0])*12
            #add the other inches
            p2 = int(this_row[6][2:len(this_row[6])])
            p3=p1+p2
            this_row.insert(13,p3)
        else:
            this_row.insert(13,'')
            
        #now the vars from the summary string and the handed field
        if this_row[4] != 'G':
        
            #4 fix the anamolies in position 
            if this_row[4] != 'G' and this_row[4] != 'C' and this_row[4] != 'RW' and this_row[4] != 'LW' and this_row[4] != 'D':
                split_position = this_row[4].split("/")
                if len(split_position) > 1:
                    if split_position[0]=='W' or split_position[0] == 'F':
                        this_row[4] = 'LW'
                    else:
                        this_row[4] = split_position[0]
                else:
                    if this_row[4]=='W' or this_row[4]== 'F' or this_row[4]== '':
                        this_row[4] = 'LW'

            #14 handed
            this_row.insert(14,this_row[8][0])
            if this_row[14] =='/' or this_row[14] =='' or this_row[14] =='-':
                 this_row[14] ='L'
                 
            #split the string
            split_summary = this_row[11].split(",")
            
            #15 goals
            goals = int(split_summary[0].replace("G",""))
            this_row.insert(15,goals)

            #16 assists
            assists = int(split_summary[1].replace("A",""))
            this_row.insert(16,assists)

            #17 total_points  
            points = int(split_summary[2].replace("P",""))
            this_row.insert(17,points)
            
            #fill in the fields meant for goalies
            this_row.insert(18,'')
            this_row.insert(19,'')
            this_row.insert(20,'')
            this_row.insert(21,'')
        #if goalies
        if this_row[4]=='G':
            #14 handed
            this_row.insert(14,this_row[8][2:3])
            #fill in missing with most likely hand based on dist of handed
            if this_row[14] =='/' or this_row[14] =='' or this_row[14] =='-':
                 this_row[14] ='L'
            
            #fill in the values for player stats with missings
            this_row.insert(15,'')
            this_row.insert(16,'')
            this_row.insert(17,'')
            
            #split the summary field for goalies e.g. '1-0-0, 4.39 GAA'
            split_summary = this_row[11].split(",")
            
            #get the games won, lost, and tied
            goalie_part1 = split_summary[0].split("-")
            goalie_won = int(goalie_part1[0])
            goalie_lost = int(goalie_part1[1])
            goalie_tied = int(goalie_part1[2])
            
            gaa = float(split_summary[1].replace("GAA",""))
            #split_summary has two components: ['1-0-0', '4.39 GAA']
            
            #18 games_won
            this_row.insert(18,goalie_won)
            #19 games_lost
            this_row.insert(19,goalie_lost)
            #20 games_tied
            this_row.insert(20,goalie_tied)
            #21 gaa
            this_row.insert(21,gaa)
            
    #append to appropriate list
    outPlayers.append(this_row)
        
    if k< 100:
        print(this_row)
    k=k+1

#now write the data to csv
with open(player_output_directory + player_csv_name, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(outPlayers)
print "Completed Creating: " + player_output_directory + player_csv_name
