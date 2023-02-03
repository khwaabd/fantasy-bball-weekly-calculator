import sys
import os
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa


sc = OAuth2(None, None, from_file='oauth2.json')
#print(sc)

gm = yfa.Game(sc, 'nba')
#print(gm)

year_num = sys.argv[1]
#print(year_num)
lg = gm.to_league(gm.league_ids(year=year_num)[0])
weeks=lg.current_week()

week_winners = {}
for i in range(1, weeks):
    stream = os.popen("python3 main.py " + str(i) + " " + year_num)
    output = stream.readlines()
    found = False
    for line in output:
        pass
    week_winners[i] = line
print("\nWinners for Each Week")
winner_totals = {}
for i in week_winners:
    winners=week_winners[i].replace('[','')
    winners=winners.replace(']','')
    winners=winners.replace('\'','')
    winners=winners.replace('\n','')
    winners=winners.replace('"','')
    print("Week " + str(i) + ": " + winners)
    winners=winners.replace(' ','')
    winners_array=winners.split(",")
    for win in winners_array:
        if win in winner_totals:
            winner_totals[win].append(i)
        else:
            winner_totals[win] = []
            winner_totals[win].append(i)

print("\nSeason summary")
for i in winner_totals:
    print(i + ": weeks- [" + ','.join(str(x) for x in winner_totals[i]) + "] total: " + str(len(winner_totals[i])))
