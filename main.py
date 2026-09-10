import csv
import random


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
        self.players = []
        self.strength = 0
        self.tactic = "Control"


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


# Connect players to their teams
for team in teams:
    for player in players:
        if player.team_id == team.team_id:
            team.players.append(player)


# Calculate team strength
for team in teams:
    total_rating = 0

    for player in team.players:
        total_rating += player.rating

    team.strength = round(total_rating / len(team.players))


# Match Engine class
class MatchEngine:
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team

        self.home_score = 0
        self.away_score = 0

        self.home_attack = 0
        self.home_defense = 0

        self.away_attack = 0
        self.away_defense = 0

    def calculate_team_power(self, team):
        attack = team.strength
        defense = team.strength

        # Attacking tactic
        if team.tactic == "Attacking":
            attack += 8
            defense -= 5

        # Control tactic
        elif team.tactic == "Control":
            attack += 2
            defense += 2

        # Defensive tactic
        elif team.tactic == "Defensive":
            attack -= 5
            defense += 8

        return attack, defense

    def calculate_goals(self, attack_power, defense_power):
        power_difference = attack_power - defense_power

        # Base chance of creating a goal
        chance = 25

        # Team power difference
        chance += power_difference * 1.5

        # Random luck
        chance += random.uniform(-15, 15)

        # Keep chance inside a reasonable range
        if chance < 5:
            chance = 5

        if chance > 60:
            chance = 60

        # Number of chances created
        number_of_chances = random.randint(5, 15)

        goals = 0

        for i in range(number_of_chances):
            random_number = random.uniform(0, 100)

            if random_number < chance:
                goals += 1

        # Limit goals
        if goals > 5:
            goals = 5

        return goals

    def play_match(self):

        print()
        print("================================")
        print("MATCH START")
        print("================================")

        print(
            self.home_team.team_name,
            "vs",
            self.away_team.team_name
        )

        print()

        print(
            self.home_team.team_name,
            "tactic:",
            self.home_team.tactic
        )

        print(
            self.away_team.team_name,
            "tactic:",
            self.away_team.tactic
        )

        print()

        # Calculate tactical powers
        self.home_attack, self.home_defense = self.calculate_team_power(
            self.home_team
        )

        self.away_attack, self.away_defense = self.calculate_team_power(
            self.away_team
        )

        # Calculate goals
        self.home_score = self.calculate_goals(
            self.home_attack,
            self.away_defense
        )

        self.away_score = self.calculate_goals(
            self.away_attack,
            self.home_defense
        )

        # Show result
        print("Final Result:")
        print(
            self.home_team.team_name,
            self.home_score,
            "-",
            self.away_score,
            self.away_team.team_name
        )

        print("================================")

        return self.home_score, self.away_score


# Check the created objects
print("Created Team objects:", len(teams))
print("Created Player objects:", len(players))


# Available tactics
tactics = [
    "Attacking",
    "Control",
    "Defensive"
]


# User chooses a team
print()
print("Available teams:")

for team in teams:
    print(team.team_id, "-", team.team_name)


user_team_id = int(input("Choose your team ID: "))

user_team = None

for team in teams:
    if team.team_id == user_team_id:
        user_team = team
        break


# Check if the selected team exists
if user_team is None:

    print("Invalid team ID.")

else:

    # User chooses a tactic
    print()
    print("Choose your tactic:")
    print("1 - Attacking")
    print("2 - Control")
    print("3 - Defensive")

    tactic_choice = int(input("Choose your tactic: "))

    if tactic_choice == 1:
        user_team.tactic = "Attacking"

    elif tactic_choice == 2:
        user_team.tactic = "Control"

    elif tactic_choice == 3:
        user_team.tactic = "Defensive"

    else:
        print("Invalid tactic.")
        user_team = None


    if user_team is not None:

        # Choose a random opponent
        possible_opponents = []

        for team in teams:
            if team.team_id != user_team.team_id:
                possible_opponents.append(team)

        opponent_team = random.choice(possible_opponents)


        # Computer chooses a random tactic
        opponent_team.tactic = random.choice(tactics)


        # Show match information
        print()
        print("================================")
        print("MATCH INFORMATION")
        print("================================")

        print("Your team:", user_team.team_name)
        print("Your strength:", user_team.strength)
        print("Your tactic:", user_team.tactic)

        print()

        print("Opponent:", opponent_team.team_name)
        print("Opponent strength:", opponent_team.strength)
        print("Opponent tactic:", opponent_team.tactic)

        print("================================")


        # Create the match
        match = MatchEngine(user_team, opponent_team)


        # Play the match
        match.play_match()