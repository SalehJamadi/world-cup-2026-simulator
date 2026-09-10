import csv


# Read teams from CSV
with open("world_cup_2026_teams.csv", "r", encoding="utf-8") as file:
    teams_data = list(csv.DictReader(file))


# Read players from CSV
with open("world_cup_2026_players.csv", "r", encoding="utf-8") as file:
    players_data = list(csv.DictReader(file))


# Check the loaded data
print("Number of teams:", len(teams_data))
print("Number of players:", len(players_data))


# Team class
class Team:
    def __init__(self, team_id, team_name, country_code, group_name):
        self.team_id = team_id
        self.team_name = team_name
        self.country_code = country_code
        self.group_name = group_name


# Player class
class Player:
    def __init__(self, player_id, team_id, player_name, position_group, rating):
        self.player_id = player_id
        self.team_id = team_id
        self.player_name = player_name
        self.position_group = position_group
        self.rating = rating


# Create Team objects
teams = []

for team_data in teams_data:
    team = Team(
        int(team_data["team_id"]),
        team_data["team_name"],
        team_data["country_code"],
        team_data["group_name"]
    )

    teams.append(team)


# Create Player objects
players = []

for player_data in players_data:
    player = Player(
        int(player_data["player_id"]),
        int(player_data["team_id"]),
        player_data["player_name"],
        player_data["position_group"],
        int(player_data["rating"])
    )

    players.append(player)


# Check the created objects
print("Created Team objects:", len(teams))
print("Created Player objects:", len(players))