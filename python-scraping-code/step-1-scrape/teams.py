import csv 
from pattern.web import URL, DOM

"""
Author: John Mercer
Last Run: 2/10/13

This code creates a csv file composed of summary stats on all NHL hockey teams. Its structure is:
team_acronym, Franchise, Lg, From, To, Yrs, GP, W, L, T, OL, PTS, PTS%, Yrs Plyf, Div, Conf, Champ, St Cup

"""

#First specify where you would like to dump the NHL team file
output_directory = "/Users/mercicle/Desktop/CS171_Scraped_Hockey_Data/"
my_csv_name = "all_teams.csv"

#this is the page I want to scrape
url = URL("http://www.hockey-reference.com/teams/")
dom = DOM(url.download(cached=True))

#the team labels are held inside a 
#<tr class="">
#...
#</tr>
team_labels = dom.by_tag("tr")

# there are two sets of labels: 1. active and 2. defunct franchises
# I use team_labels[0] but it doesn't matter because the labels are the same
# get "th"'s b/c the elements look like this: <th align="left"  class="tooltip sort_default_asc" >Franchise</th>
all_labels = team_labels[0].by_tag("th")

team_label_container=[]
for label in all_labels:
    team_label_container.append(label.content.encode("utf8"))
  
# team_label_container now has the headers
team_label_container.insert(0,'team_acronym') 

team_container=[]
team_container.append(team_label_container)

#Now get the statistics.
teams = dom.by_class("full_table")

for team in teams:
    this_team_container=[]
    for td in team.by_tag("td"):
        #http://stackoverflow.com/questions/2365411/python-convert-unicode-to-ascii-without-errors
        this_team_container.append(td.content.encode("utf8"))

    # original comes out like this: ['<a href="/teams/ANA/">Anaheim Ducks</a>', 'NHL',...]
    #split the first element to create two entries: 1. for the URL and 2. the other for franchise
    team_acronym = this_team_container[0][this_team_container[0].find("/teams")+7:this_team_container[0].find("/teams")+10]
    franchise = this_team_container[0].split(">")[1][0:len(this_team_container[0].split(">")[1])-3]
    #now remove the <a href> element and replace with the cleaned acronym and franchise
    this_team_container.pop(0)
    this_team_container.insert(0,team_acronym)
    this_team_container.insert(1,franchise)
    
    #I only want to analyze NHL teams
    if this_team_container[2]=="NHL":
        team_container.append(this_team_container)
    
print "Completed Compiling Teams..."
#First write all teams to a file all_teams.csv

#now write the data to csv
with open(output_directory + my_csv_name, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(team_container)

print "Completed Creating: " + output_directory + my_csv_name
