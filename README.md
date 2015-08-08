
Web Scraping Hockey Data in Python and Visualizing in Tableau
------

You can use these scripts (most likely with some modifications based on changes in the hockey-reference website html and the python package updates) to scrape player and team hockey data since the inception of the National Hockey League to build predictive models and visualizations of player and team hockey data.  

To run these scripts the only thing you should need to change is the input/output directory names in the code. Here is an example from my code: input_directory = "/Users/mercicle/Desktop/CS171_Scraped_Hockey_Data/Teams/"
So you will need to replace “/Users/mercicle/Desktop/” with your directory.

Also, note I developed these in Eclipse just in case you run into encoding problems.

Step 1: scraping
1. teams.py
2. team_by_year.py
3. team_by_year_all.py 
4. roster_by_year.py
5. roster_by_year_all.py

Step 2: cleaning and combining data
The clean-rosters.py will cleanup the player file (will create all_players_cleaned.csv), and the combine-and-clean-teams.py will combine all of the individual team files and do some minor cleaning in the process (updates combined_teams.csv) 

The final cleaned datasets are in the /data folder and the tableau workbooks are in the tableau-visualizations folder. 

Please send me an email with any questions. I didn't get a chance to build predictive models in this space yet but I think there is a lot of potential and the data provided here is only a step away from predicting player and team performance.

Have fun!
John Mercer (analyticsurgeon at gmail.com)

