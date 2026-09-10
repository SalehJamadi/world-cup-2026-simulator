import csv
import random
import time


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

        self.match_events = []


    # Calculate attack and defense power based on tactic
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


    # Choose a player who scores the goal
    def choose_goal_scorer(self, team):

        attackers = []
        midfielders = []
        defenders = []

        for player in team.players:

            if player.position_group == "ATT":
                attackers.append(player)

            elif player.position_group == "MID":
                midfielders.append(player)

            elif player.position_group == "DEF":
                defenders.append(player)


        # 70% attackers
        # 20% midfielders
        # 10% defenders
        position_choice = random.choices(
            ["ATT", "MID", "DEF"],
            weights=[70, 20, 10],
            k=1
        )[0]


        # Choose a player from the selected position
        if position_choice == "ATT" and attackers:
            return random.choice(attackers)

        elif position_choice == "MID" and midfielders:
            return random.choice(midfielders)

        elif position_choice == "DEF" and defenders:
            return random.choice(defenders)


        # Fallback
        return random.choice(team.players)


    # Calculate how likely a team is to create a goal
    def calculate_goal_chance(self, attack_power, defense_power):

        power_difference = attack_power - defense_power

        # Base chance
        chance = 10

        # Strength difference
        chance += power_difference * 0.7

        # Random luck
        chance += random.uniform(-4, 4)

        # Keep chance inside a reasonable range
        if chance < 3:
            chance = 3

        if chance > 25:
            chance = 25

        return chance


    # Play the match
    def play_match(self):

        print()
        print("========================================")
        print("MATCH START")
        print("========================================")

        print(
            self.home_team.team_name,
            "vs",
            self.away_team.team_name
        )

        print()

        print(
            self.home_team.team_name,
            "Strength:",
            self.home_team.strength,
            "| Tactic:",
            self.home_team.tactic
        )

        print(
            self.away_team.team_name,
            "Strength:",
            self.away_team.strength,
            "| Tactic:",
            self.away_team.tactic
        )

        print()
        print("----------------------------------------")
        print("Match Events")
        print("----------------------------------------")


        # Calculate team powers
        self.home_attack, self.home_defense = self.calculate_team_power(
            self.home_team
        )

        self.away_attack, self.away_defense = self.calculate_team_power(
            self.away_team
        )


        # Calculate goal chances
        home_goal_chance = self.calculate_goal_chance(
            self.home_attack,
            self.away_defense
        )

        away_goal_chance = self.calculate_goal_chance(
            self.away_attack,
            self.home_defense
        )


        # Simulate minutes 0 to 90
        for minute in range(0, 91):

            # Create progress bar
            progress_length = 30

            progress = int(
                (minute / 90) * progress_length
            )

            bar = (
                "█" * progress
                + "-" * (progress_length - progress)
            )

            print(
                f"\r{minute:02d}' [{bar}]",
                end="",
                flush=True
            )


            # Chance of creating an event
            event_chance = random.randint(1, 100)


            # Check if a goal happens
            if event_chance <= 4:

                # Home team chance
                if random.uniform(0, 100) < home_goal_chance:

                    # Limit maximum goals
                    if self.home_score < 5:

                        scorer = self.choose_goal_scorer(
                            self.home_team
                        )

                        self.home_score += 1

                        event = (
                            f"\n{minute}' GOAL! "
                            f"{self.home_team.team_name} - "
                            f"{scorer.player_name}"
                        )

                        print(event)

                        self.match_events.append(event)


                # Away team chance
                elif random.uniform(0, 100) < away_goal_chance:

                    # Limit maximum goals
                    if self.away_score < 5:

                        scorer = self.choose_goal_scorer(
                            self.away_team
                        )

                        self.away_score += 1

                        event = (
                            f"\n{minute}' GOAL! "
                            f"{self.away_team.team_name} - "
                            f"{scorer.player_name}"
                        )

                        print(event)

                        self.match_events.append(event)


            # Match animation delay
            time.sleep(0.2)


        print()
        print()
        print("----------------------------------------")
        print("FULL TIME")
        print("----------------------------------------")

        print(
            self.home_team.team_name,
            self.home_score,
            "-",
            self.away_score,
            self.away_team.team_name
        )

        print("----------------------------------------")


        # Return final score
        return self.home_score, self.away_score


# ==================================================
# GROUP STAGE
# ==================================================

# Create groups
groups = {}

for team in teams:

    if team.group_name not in groups:
        groups[team.group_name] = []

    groups[team.group_name].append(team)


# Sort groups alphabetically
groups = dict(sorted(groups.items()))


# Show all groups
print()
print("========================================")
print("WORLD CUP 2026 GROUPS")
print("========================================")

for group_name, group_teams in groups.items():

    print()
    print("GROUP", group_name)

    for team in group_teams:
        print(
            team.team_id,
            "-",
            team.team_name
        )


print()
print("========================================")
print("GROUP STAGE MATCHES")
print("========================================")


# Create six matches for every group
group_matches = {}

for group_name, group_teams in groups.items():

    matches = []

    for i in range(len(group_teams)):

        for j in range(i + 1, len(group_teams)):

            home_team = group_teams[i]
            away_team = group_teams[j]

            matches.append(
                (
                    home_team,
                    away_team
                )
            )


    group_matches[group_name] = matches


# Show all group matches
for group_name, matches in group_matches.items():

    print()
    print("GROUP", group_name)

    for match_number, match in enumerate(matches, start=1):

        home_team = match[0]
        away_team = match[1]

        print(
            match_number,
            ".",
            home_team.team_name,
            "vs",
            away_team.team_name
        )


# Check the number of groups
print()
print("========================================")
print("GROUP STAGE INFORMATION")
print("========================================")

print(
    "Number of groups:",
    len(groups)
)

print(
    "Number of group matches:",
    sum(len(matches) for matches in group_matches.values())
)

print("========================================")


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
    print(
        team.team_id,
        "-",
        team.team_name
    )


user_team_id = int(
    input("Choose your team ID: ")
)


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

    tactic_choice = int(
        input("Choose your tactic: ")
    )


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


        opponent_team = random.choice(
            possible_opponents
        )


        # Computer chooses a random tactic
        opponent_team.tactic = random.choice(
            tactics
        )


        # Show match information
        print()
        print("========================================")
        print("MATCH INFORMATION")
        print("========================================")

        print(
            "Your team:",
            user_team.team_name
        )

        print(
            "Your strength:",
            user_team.strength
        )

        print(
            "Your tactic:",
            user_team.tactic
        )

        print()

        print(
            "Opponent:",
            opponent_team.team_name
        )

        print(
            "Opponent strength:",
            opponent_team.strength
        )

        print(
            "Opponent tactic:",
            opponent_team.tactic
        )

        print("========================================")


        # Create the match
        match = MatchEngine(
            user_team,
            opponent_team
        )


        # Play the match
        match.play_match()