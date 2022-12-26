import requests
import json
from collections import defaultdict

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

API_KEY = "cdd9980947c042d3e2623d1f826681c0"
sport = "americanfootball_nfl" # can use upcoming
regions = "us"
markets = "h2h"
api_link = "https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={apiKey}&regions={regions}&markets={markets}&oddsFormat={oddsFormat}".format(sport=sport,apiKey=API_KEY,markets=markets,regions=regions,oddsFormat="decimal")
print(api_link)
response = requests.get(api_link)
# print(response.status_code)
# jprint(response.json())

data = response.json()

games = defaultdict(lambda: defaultdict(list))

for i in range(len(data)):
    game_name = ""
    game_name += data[i]["home_team"] + " vs. " + data[i]["away_team"]
    games[game_name] = []

    for bookmaker in data[i]["bookmakers"]:
        to_add = []
        to_add.append(bookmaker["title"])
        to_add.append((bookmaker["markets"][0]["outcomes"][0]["name"], bookmaker["markets"][0]["outcomes"][0]["price"]))
        to_add.append((bookmaker["markets"][0]["outcomes"][1]["name"], bookmaker["markets"][0]["outcomes"][1]["price"]))
        games[game_name].append(to_add)

arb_ops = []

def compute(o1, o2):
    return (1/o1 + 1/o2)

for gname in games:
    for i in range(len(games[gname])):
        company1 = games[gname][i]
        for j in range(i + 1, len(games[gname])):
            company2 = games[gname][j]
            
            calculate = compute(company1[1][1], company2[2][1])
            if calculate < 1:
                arb_ops.append([gname, company1[0], company1[1], company2[0], company2[2]])

            calculate = compute(company1[2][1], company2[1][1])
            if calculate < 1:
                arb_ops.append([gname, company1[0], company1[2], company2[0], company2[1]])

#----------------------------------------------
amt_for_lowest_odds = 50
#----------------------------------------------

result = []

for opp in arb_ops:
    if opp[2][1] < opp[4][1]:
        amt_for_higher_odds = amt_for_lowest_odds * (opp[2][1] / opp[4][1])
        result.append([opp[1], opp[2][0], amt_for_lowest_odds, opp[3], opp[4][0], amt_for_higher_odds])
    else:
        amt_for_higher_odds = amt_for_higher_odds * (opp[4][1] / opp[2][1])
        result.append([opp[3], opp[4][0], amt_for_higher_odds, opp[1], opp[2][0], amt_for_lowest_odds])

print("\n\n")
print(result)
print("\n\n")