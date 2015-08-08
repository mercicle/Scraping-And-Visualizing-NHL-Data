import csv 
from pattern.web import URL, DOM

"""
Author: John Mercer
Last Run: 2/11/13
This code creates a csv file of the roster of a team for a given year
"""

# First get the loop working to iterate through all the years for one team
input_directory = "/Users/mercicle/Desktop/CS171_Scraped_Hockey_Data/Teams/"


#list of all teams i will iterate through
team_acronym_list = ["ANA","BOS","BUF","CGY","CAR","CHI","COL","CBJ","DAL",
                      "DET","EDM","FLA","LAK","MIN","MTL","NSH","NJD","NYI",
                      "NYR","OTT","PHI","PHX","PIT","SJS","STL","TBL","TOR",
                      "VAN","WSH","WPG","CLE","HAM","MTM","MTW","NYA","OTS",
                      "PHQ","PTP","QBC","STE"]

#team_acronym_list = ["ANA","BOS","BUF"]

#this will hold all the rosters for each team for each year
roster_container = []

#I use this to only write the roster labels once when compiling the roster dataset
labels_written = 0

#iterate through each team
for tidx in range(0,len(team_acronym_list)):
    
    #set the team id to a new variable just bc it looks better
    this_team_acronym = team_acronym_list[tidx]
    
    #let myself(and you) know where the algorithm is at
    print "Writing " + this_team_acronym + " ..."
    
    #First specify my csv file name
    input_csv = input_directory + this_team_acronym + ".csv"
    
    #open it up and read it in
    opened_csv  = open(input_csv, "rU")
    reader = csv.reader(opened_csv, dialect=csv.excel_tab)
    
    #for row in reader means for each season the team existed
    for row in reader:
        #this is the row of the csv file
        x = str(row[0]).split(",")
        #the first row is the labels so don't need that
        if x[1] != "url_for_year":
            #this is the url
            this_team_year_url = x[1]
            #this is the year I want to append to each roster element
            this_season = x[2]

            #this is the page I want to scrape
            url = URL(this_team_year_url)
            dom = DOM(url.download(timeout=90,cached=True))
            
            all_trs = dom.by_tag("tr")
            
            #only write the labels for the very first roster/year
            if labels_written == 0:
                #get the raw object with the labels (variable names) for each season
                roster_labels = all_trs[3].by_tag("th")
                
                #build the final list of variables called season_label_container
                roster_labels_container=[]
                for label in roster_labels:
                    roster_labels_container.append(label.content.encode("utf8"))
                
                #add in a column for the team acronym to act as a key
                roster_labels_container.insert(0,"team_id")
                roster_labels_container.insert(1,"Season")
                
                #the roster_container holds all of the players for the specified team/year
                #add logic here to only write the first time, use index
                roster_container.append(roster_labels_container)
                
                #now, next iteration, remind myselfI wrote them already
                labels_written = 1
                
            # this is so powerful - I just needed to look and find the id for the roster table
            all_divs = dom.by_id("roster")
            #roster_trs holds a list of players info
            roster_trs = all_divs.by_tag("tr")
            
            #iterate through each player in the roster
            for trs in roster_trs:
                
                #this will hold the final encoded info/stats pulled from the current player
                this_roster_farian = []
                #stop and laugh: bahaha
                
                #now add the team id and the season
                this_roster_farian.append(this_team_acronym) 
                this_roster_farian.append(this_season) 
                
                for t in trs.by_tag("td"):
                        #the player name has a link to the player, 
                        #e.g. '<a href="/players/m/milledr01.html">Drew Miller</a>'
                        # so I need to test if the tag 'a' is there
                        
                        #indicator telling me an "a" tag is present
                        a_tag_present = 0
                      
                        for tag_a in t.by_tag("a"):
                            a_tag_present = 1
                            this_roster_farian.append(tag_a.content.encode("utf8"))
                        if a_tag_present == 0:
                            this_roster_farian.append(t.content.encode("utf8"))
                
                
                #now append the player to the roster list, but check >0 because the first label entry is len zero
                if len(this_roster_farian)>2:
                    roster_container.append(this_roster_farian)

# First get the loop working to iterate through all the years for one team
output_directory = "/Users/mercicle/Desktop/CS171_Scraped_Hockey_Data/Rosters/"
my_output_csv_name = "all_rosters.csv"
#now write the data to csv
with open(output_directory + my_output_csv_name, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(roster_container)

print "Completed Creating: " + output_directory + my_output_csv_name

    