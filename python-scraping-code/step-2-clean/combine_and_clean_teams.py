'''
Created on Feb 21, 2013

@author: mercicle
'''
import csv 
from datetime import date
import time

#specify the output directory and filename
output_directory = "/Users/mercicle/Desktop/CS171_Scraped_Hockey_Data/Teams/"
final_csv_name = "combined_teams.csv"


# This is the team acronym list you can get from all_teams.csv
team_acronym_list = ["ANA","BOS","BUF","CGY","CAR","CHI","COL","CBJ","DAL",
                      "DET","EDM","FLA","LAK","MIN","MTL","NSH","NJD","NYI",
                      "NYR","OTT","PHI","PHX","PIT","SJS","STL","TBL","TOR",
                      "VAN","WSH","WPG","CLE","HAM","MTM","MTW","NYA","OTS",
                      "PHQ","PTP","QBC","STE"]

#this will hold the cleaned data
allTeams = [ ]
#team label indicator
tl_ind = 0
for tidx in range(0,len(team_acronym_list)):
    this_team_acronym = team_acronym_list[tidx]

    #where is the input files you are cleaning and combining?
    input_directory = "/Users/mercicle/Desktop/CS171_Scraped_Hockey_Data/Teams/"
    in_csv_name = this_team_acronym + ".csv"
    
    ifile  = open(input_directory + in_csv_name)
    reader = csv.reader(ifile)
    
    #this is a row index i use for conditional processing (mostly to only read in the labels
    #the first time i see them (since every team dataset has a labels 1st row)
    row_idx = 0
    for row in reader:
        # 0              1            2        3      4      5    6    7    8     9     10     11     12     13     14        15            16
        #team_id    url_for_year    Season    Lg    Team    GP    W    L    T    OL    PTS    PTS%    SRS    SOS    Finish    Playoffs    Coaches

        this_row = [ row[i] for i in range(0,len(row)) ]
        this_row = this_row[0:17]
        #if very first row of first dataset, append new date index column
        if row_idx == 0 and tl_ind == 0:
            this_row.append('date_index')
            this_row.append('won_stanley_cup')
            
        if row_idx != 0 or tl_ind == 0:
            #if it's not populated then set to zero
            if len(this_row[6]) < 1:
                this_row[6] = 0
            if len(this_row[7]) < 1:
                this_row[7] = 0
            if len(this_row[8]) < 1:
                this_row[8] = 0
            if len(this_row[9]) < 1:
                this_row[9] = 0           
            
            #12 date_index
            if row_idx != 0 or tl_ind != 0:
                time_struct = time.strptime(this_row[2][0:4]+"-01-01", "%Y-%m-%d") 
                this_row.append(time.strftime("%m/%d/%Y",time_struct))
                
                #if i find the string 'won stanley cup' then 1 else 0
                if this_row[15].find("Won Stanley Cup") > -1:
                    this_row.append(1)
                else:
                    this_row.append(0)
                     
            #finally append the cleaned row
            allTeams.append(this_row)
        row_idx = row_idx + 1
        
    tl_ind = 1
        
#now write the data to csv
with open(output_directory + final_csv_name, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(allTeams)
    
print "Completed Creating: " + output_directory + final_csv_name
