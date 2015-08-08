import csv 
from pattern.web import URL, DOM

"""
Author: John Mercer
Last Run: 2/11/13
This code creates a csv file of the roster of a team for a given year
"""

# First get the loop working to iterate through all the years for one team
input_directory = "/Users/mercicle/Desktop/CS171_Scraped_Hockey_Data/Teams/"
this_team_acronym = "DET"

my_csv_name = this_team_acronym + ".csv"

ifile  = open(input_directory+my_csv_name, "rU")
reader = csv.reader(ifile, dialect=csv.excel_tab)

team_year_urls = []
seasons = []
for row in reader:
    x = str(row[0]).split(",")
    if x[1] != "url_for_year":
        #this is the url
        team_year_urls.append(x[1])
        #this is the year I want to append to each roster element
        seasons.append(x[2])
        
this_season = "2011-12"
#team_year_data looks like: ['http://www.hockey-reference.com/teams/DET/2012.html', ...]

sample_team_year_url = "http://www.hockey-reference.com/teams/DET/2012.html";

#this is the page I want to scrape

url = URL(sample_team_year_url)
dom = DOM(url.download(timeout=60,cached=True))

all_trs = dom.by_tag("tr")

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
roster_container = []
roster_container.append(roster_labels_container)
print roster_labels_container

# this is so powerful - I just needed to look and find the id for the roster table
all_divs = dom.by_id("roster")
#roster_trs holds a list of players info
roster_trs = all_divs.by_tag("tr")

#iterate through each player in the roster
for trs in roster_trs:

    #this will hold the final encoded info/stats pulled from the current player
    this_roster_farian = []
    #now add the team id and the season
    this_roster_farian.append(this_team_acronym) 
    this_roster_farian.append(this_season) 
    
    for t in trs.by_tag("td"):
            #the player name has a link to the player, 
            #e.g. '<a href="/players/m/milledr01.html">Drew Miller</a>'
            # so I need to test if the tag is there
            
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

print roster_container[1]
    