import csv 
from pattern.web import URL, DOM

"""
Author: John Mercer
Last Run: 2/10/13
This code creates a csv file composed of a teams stats by year
"""

# This is the team acronym list you can get from all_teams.csv
# You could read them on the fly but I like seeing them here in the code
# The team list is pretty stable so this should not be too risky

team_acronym_list = ["ANA","BOS","BUF","CGY","CAR","CHI","COL","CBJ","DAL",
                      "DET","EDM","FLA","LAK","MIN","MTL","NSH","NJD","NYI",
                      "NYR","OTT","PHI","PHX","PIT","SJS","STL","TBL","TOR",
                      "VAN","WSH","WPG","CLE","HAM","MTM","MTW","NYA","OTS",
                      "PHQ","PTP","QBC","STE"]

for tidx in range(0,len(team_acronym_list)):
    this_team_acronym = team_acronym_list[tidx]

    #First specify where you would like to dump the NHL team file
    output_directory = "/Users/mercicle/Desktop/CS171_Scraped_Hockey_Data/Teams/"
    my_csv_name = this_team_acronym + ".csv"
    
    #sometimes the name of the team changes but it stays in the same town and has 
    #for example detroit red wings used to be called the detroit cougars in 1930 so the acronym is DTC for the url building
    # so I can't assume the top level acronyms I compiled for the organization will work for building the 
    # team-year-summary stats pages
    
    file_for_team_year_urls=[]
    file_for_team_year_urls.append(["team_year_url"])
    
    #this is the page I want to scrape
    url = URL("http://www.hockey-reference.com/teams/" + this_team_acronym)
    dom = DOM(url.download(cached=True))
    
    all_trs = dom.by_tag("tr")
    
    #get the raw object with the labels (variable names) for each season
    season_labels = all_trs[0].by_tag("th")
    
    #build the final list of variables called season_label_container
    season_label_container=[]
    for label in season_labels:
        season_label_container.append(label.content.encode("utf8"))
    
    #add in a column for the team acronym to act as a key
    season_label_container.insert(0,"team_id")
    
    #now add a column to hold the year dependent team acronym
    season_label_container.insert(1,"url_for_year")
    
    #the season_container holds all of the seasons for the specified team
    season_container=[]
    season_container.append(season_label_container)
    
    #so I want to use a .by_tag("tr")
    trs = dom.by_tag("tr")
    
    #set the tr tag index to 0
    tr_idx = 0
    
    for t in trs:
    
        #this will hold the statistics and info in t
        this_season_container=[]
        
        #tr_idx = 0 holds the labels so I don't need them - already got them
        if tr_idx > 0:
            #the index of the td's
            td_idx = 0
            for tds in t.by_tag("td"):
                #little nuance: I need to get the right team acronym because sometime it changes based on the year
                #if the team rebranded(see Detroit example above)
                if td_idx == 0:
                    this_years_acronym = str(tds)[str(tds).find("/teams")+7:str(tds).find("/teams")+10]
                    
                #indicator telling me an "a" tag is present
                a_tag_present = 0
                #some of the elements have an extra tag and some do not
                for tag_a in tds.by_tag("a"):
                    a_tag_present = 1
                    this_season_container.append(tag_a.content.encode("utf8"))
                if a_tag_present == 0:
                    this_season_container.append(tds.content.encode("utf8"))
                #now update the td index
                td_idx = td_idx + 1
            
            #add the team acronym used in the teams table (this is not dependent upon the year)
            this_season_container.insert(0,this_team_acronym)
            
            #before appending to the season_container, build the url and add it to the list
            year_for_url = str(int(this_season_container[1][0:4])+1)
            
            #make this type of url: http://www.hockey-reference.com/teams/DET/1938.html
            url_for_this_year = "http://www.hockey-reference.com/teams/" + this_years_acronym + "/" + year_for_url + ".html"
            this_season_container.insert(1,url_for_this_year)
            
            #file_for_team_year_urls.append
            season_container.append(this_season_container)
            
        #now update the tr tag index to visit the next year
        tr_idx = tr_idx + 1
        
    #now write the data to csv
    with open(output_directory + my_csv_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(season_container)
    
    print "Completed Creating: " + output_directory + my_csv_name
