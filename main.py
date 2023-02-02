from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import json
from collections.abc import Iterable
import sys

sc = OAuth2(None, None, from_file='oauth2.json')
#print(sc)

gm = yfa.Game(sc, 'nba')
#print(gm)

year_num = sys.argv[2]
#print(year_num)
lg = gm.to_league(gm.league_ids(year=year_num)[0])
#print(lg)

stat_ids = {
        "5" : "FG%",
        "8" : "FT%",
        "10" : "3PT",
        "12" : "PTS",
        "15" : "REB",
        "16" : "AST",
        "17" : "STL",
        "18" : "BLK",
        "19" : "TO"
}

week_num = sys.argv[1]
matchups_ret = lg.matchups(week=week_num)
matchups = matchups_ret['fantasy_content']['league'][1]['scoreboard']['0']['matchups']
#print(json.dumps(matchups, indent=2, sort_keys=True))

simple_teams = {}
winners = []
for matchup in matchups:

    if matchup == "count":
        continue

    if "matchup" in matchups[matchup]:
        if "winner_team_key" in  matchups[matchup]["matchup"]:
            winners.append(matchups[matchup]["matchup"]["winner_team_key"])

        team0_obj = matchups[matchup]["matchup"]["0"]["teams"]["0"]["team"][0]
        team1_obj = matchups[matchup]["matchup"]["0"]["teams"]["1"]["team"][0]
        simple_teams[team0_obj[2]["name"]] = {
                'key' : team0_obj[0]["team_key"],
                'id' : team0_obj[1]["team_id"],
                'stats' : {},
                'wins_against' : [],
                'num_wins' : 0,
                'loses_to' : [],
                'num_loss' : 0

        }
        simple_teams[team1_obj[2]["name"]] = {
                'key' : team1_obj[0]["team_key"],
                'id' : team1_obj[1]["team_id"],
                'stats' : {},
                'wins_against' : [],
                'num_wins' : 0,
                'loses_to' : [],
                'num_loss' : 0
        }
        score0 = matchups[matchup]["matchup"]["0"]["teams"]["0"]["team"][1]["team_stats"]["stats"]
        score1 = matchups[matchup]["matchup"]["0"]["teams"]["1"]["team"][1]["team_stats"]["stats"]

        for stat in score0:
            team_name = team0_obj[2]["name"]
            stat_value = stat['stat']['value']
            stat_id = stat['stat']['stat_id']
            team_obj = simple_teams[team_name]
            stats_obj = team_obj['stats']
            if stat_id in stat_ids:
                stats_obj[stat_ids[stat_id]] = float(stat_value)

        for stat in score1:
            team_name = team1_obj[2]["name"]
            stat_value = stat['stat']['value']
            stat_id = stat['stat']['stat_id']
            team_obj = simple_teams[team_name]
            stats_obj = team_obj['stats']
            if stat_id in stat_ids:
                stats_obj[stat_ids[stat_id]] = float(stat_value)


def calculate_winner(team1_name, team2_name):
    team1 = simple_teams[team1_name]
    team2 = simple_teams[team2_name]
    stats1 = team1['stats']
    stats2 = team2['stats']
    team1_cats = 0
    team2_cats = 0

    for stat in stats1:
        #print(stat + " " + str(stats1[stat]) + " " + str(stats2[stat]))
        if stat != "TO":
            if stats1[stat] > stats2[stat]:
                team1_cats = team1_cats + 1
                #print(team1_name)
            elif stats2[stat] > stats1[stat]:
                team2_cats = team2_cats + 1
                #print(team2_name)
        else:
            if stats1[stat] < stats2[stat]:
                team1_cats = team1_cats + 1
                #print(team1_name)
            elif stats2[stat] < stats1[stat]:
                team2_cats = team2_cats + 1
                #print(team2_name)

    print("Total: " + team1_name + ": " + str(team1_cats) + " " + team2_name + ": " + str(team2_cats))
    if team1_cats == team2_cats:
        return "tie", "tie", 0
    elif team1_cats > team2_cats:
        return team1_name, team2_name, team1_cats - team2_cats
    else:
        return team2_name, team1_name, team2_cats - team1_cats

for team in simple_teams:
    for team2 in simple_teams:
        if team == team2:
            continue
        print("")
        winner, loser, margin = calculate_winner(team, team2)
        print(team + " vs." + team2 + " winner:" + winner)
        if winner != "tie":
            if loser in simple_teams[winner]['wins_against']:
                continue
            simple_teams[winner]['num_wins'] = simple_teams[winner]['num_wins'] + 1
            simple_teams[winner]['wins_against'].append(loser)
            simple_teams[loser]['num_loss'] = simple_teams[loser]['num_loss'] + 1
            simple_teams[loser]['loses_to'].append(winner)

print(json.dumps(simple_teams, indent=2, sort_keys=True))

winner_names = []
for team in simple_teams:
    winner_names.append(team)

#print(json.dumps(simple_teams, indent=2, sort_keys=True))
print("Eligible Teams:")
print(json.dumps(winner_names, indent=2, sort_keys=True))

max_wins = 0
min_loss = 99999
for winner in winner_names:
    if simple_teams[winner]['num_wins'] > max_wins:
        max_wins = simple_teams[winner]['num_wins']
    if simple_teams[winner]['num_loss'] < min_loss:
        min_loss = simple_teams[winner]['num_loss']

print("")
print("Max Wins: " + str(max_wins))
print("Min Loss: " + str(min_loss))
print("")

weekly_winners = []
for winner in winner_names:
    if simple_teams[winner]['num_loss'] == min_loss:
        weekly_winners.append(winner)

print("Weekly Winners (people who have minimum losses, calculated above):")
print(weekly_winners)
print("")

if len(weekly_winners) == 1:
    print("Congratulations")
else:
    print("We have a tie!!!, on to phase 3, who would have won from the above?")
    sub_teams = {}
    sub_teams_margins = {}
    for team in weekly_winners:
        for team2 in weekly_winners:
            if team == team2:
                continue
            print("")
            winner, loser, margin = calculate_winner(team, team2)
            print(team + " vs." + team2 + " winner:" + winner)
            if not winner in sub_teams:
                sub_teams[winner] = []
                sub_teams_margins[winner] = []
            if not loser in sub_teams[winner]:
                sub_teams[winner].append(loser)
                sub_teams_margins[winner].append({ "team": loser, "margin" : margin })
    print("")
    print("This is a list of the tied teams and who they would lose to among said tied teams, phase 3 of our rules")
    print(json.dumps(sub_teams, indent=2, sort_keys = True))
    print("")

    min_losers = 999
    for team in sub_teams:
        if len(sub_teams[team]) < min_losers:
            min_losers = len(sub_teams[team])

    print("Min Losses: " + str(min_losers))

    phase_4_ties = []
    for team in sub_teams:
        if len(sub_teams[team]) == min_losers:
            phase_4_ties.append(team)

    print("Phase 4 candidates:")
    print(phase_4_ties)

    if len(phase_4_ties) == 1:
        print("Congratulations!")
    else:
        print("We still have a tie!!!! on to phase 4, margins, lets sum up the margins of each defeat, the team with the highest total margin wins")
        print("here are the margins:")
        print(json.dumps(sub_teams_margins, indent = 2, sort_keys = True))

        total_margins = {}
        for team in sub_teams_margins:
            total_margin = 0
            for game in sub_teams_margins[team]:
                total_margin = total_margin + game['margin']
            total_margins[team]= total_margin

        print("here are the total margins:")
        print(json.dumps(total_margins, indent = 2, sort_keys = True))

        max_margin = 0
        for team in total_margins:
            if total_margins[team] > max_margin:
                max_margin = total_margins[team]

        print("Max Margin: " + str(max_margin))

        final_winners = []
        for team in total_margins:
            if total_margins[team] == max_margin:
                final_winners.append(team)

        print("FINAL WINNERS!!!!!!! if there is a tie i can help no further:")
        print(final_winners)






