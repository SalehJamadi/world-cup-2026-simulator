import csv
import random
import time


# ==================================================
# LOAD TEAMS
# ==================================================

teams = []

with open("world_cup_2026_teams.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        teams.append(
            {
                "team_id": int(row["team_id"]),
                "team_name": row["team_name"],
                "country_code": row["country_code"],
                "group_name": row["group_name"]
            }
        )


# ==================================================
# LOAD PLAYERS
# ==================================================

players = []

with open("world_cup_2026_players.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        players.append(
            {
                "player_id": int(row["player_id"]),
                "team_id": int(row["team_id"]),
                "player_name": row["player_name"],
                "position_group": row["position_group"],
                "rating": int(row["rating"])
            }
        )


# ==================================================
# TEAM CLASS
# ==================================================

class Team:

    def __init__(
        self,
        team_id,
        team_name,
        country_code,
        group_name
    ):

        self.team_id = team_id
        self.team_name = team_name
        self.country_code = country_code
        self.group_name = group_name

        self.players = []

        self.strength = 0


# ==================================================
# PLAYER CLASS
# ==================================================

class Player:

    def __init__(
        self,
        player_id,
        team_id,
        player_name,
        position_group,
        rating
    ):

        self.player_id = player_id
        self.team_id = team_id
        self.player_name = player_name
        self.position_group = position_group
        self.rating = rating


# ==================================================
# CREATE TEAM OBJECTS
# ==================================================

team_objects = []

for team_data in teams:

    team = Team(
        team_data["team_id"],
        team_data["team_name"],
        team_data["country_code"],
        team_data["group_name"]
    )

    team_objects.append(team)


# ==================================================
# CREATE PLAYER OBJECTS
# ==================================================

player_objects = []

for player_data in players:

    player = Player(
        player_data["player_id"],
        player_data["team_id"],
        player_data["player_name"],
        player_data["position_group"],
        player_data["rating"]
    )

    player_objects.append(player)


# ==================================================
# CONNECT PLAYERS TO THEIR TEAMS
# ==================================================

for player in player_objects:

    for team in team_objects:

        if player.team_id == team.team_id:

            team.players.append(player)

            break


# ==================================================
# CALCULATE TEAM STRENGTH
# ==================================================

for team in team_objects:

    total_rating = 0

    for player in team.players:

        total_rating += player.rating

    if len(team.players) > 0:

        team.strength = round(
            total_rating / len(team.players)
        )


# ==================================================
# MATCH ENGINE
# ==================================================

class MatchEngine:

    def __init__(self, home_team, away_team):

        self.home_team = home_team
        self.away_team = away_team

        self.home_score = 0
        self.away_score = 0


    # ==================================================
    # CHOOSE GOAL SCORER
    # ==================================================

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


        position_choice = random.random()


        if position_choice < 0.70 and attackers:

            selected_group = attackers

        elif position_choice < 0.90 and midfielders:

            selected_group = midfielders

        elif defenders:

            selected_group = defenders

        elif attackers:

            selected_group = attackers

        elif midfielders:

            selected_group = midfielders

        else:

            selected_group = team.players


        return random.choice(selected_group)


    # ==================================================
    # CALCULATE GOAL CHANCE
    # ==================================================

    def calculate_goal_chance(
        self,
        attacking_team,
        defending_team,
        attacking_modifier,
        defending_modifier
    ):

        attack_power = (
            attacking_team.strength
            + attacking_modifier
        )

        defense_power = (
            defending_team.strength
            + defending_modifier
        )


        difference = attack_power - defense_power


        base_chance = 0.035


        chance = (
            base_chance
            + difference * 0.001
        )


        if chance < 0.01:

            chance = 0.01


        if chance > 0.08:

            chance = 0.08


        return chance


    # ==================================================
    # PREPARE MATCH
    # ==================================================

    def prepare_match(self):

        tactics = {

            "Attacking": {
                "attack": 8,
                "defense": -5
            },

            "Control": {
                "attack": 2,
                "defense": 2
            },

            "Defensive": {
                "attack": -5,
                "defense": 8
            }

        }


        home_tactic = getattr(
            self.home_team,
            "tactic",
            "Control"
        )

        away_tactic = getattr(
            self.away_team,
            "tactic",
            "Control"
        )


        home_attack_modifier = tactics[home_tactic]["attack"]

        home_defense_modifier = tactics[home_tactic]["defense"]

        away_attack_modifier = tactics[away_tactic]["attack"]

        away_defense_modifier = tactics[away_tactic]["defense"]


        home_goal_chance = self.calculate_goal_chance(
            self.home_team,
            self.away_team,
            home_attack_modifier,
            away_defense_modifier
        )


        away_goal_chance = self.calculate_goal_chance(
            self.away_team,
            self.home_team,
            away_attack_modifier,
            home_defense_modifier
        )


        return home_goal_chance, away_goal_chance


    # ==================================================
    # SIMULATE ONE MINUTE
    # ==================================================

    def simulate_minute(
        self,
        minute,
        home_goal_chance,
        away_goal_chance,
        show_events=True
    ):

        # Home team goal attempt

        if random.random() < home_goal_chance:

            if self.home_score < 5:

                scorer = self.choose_goal_scorer(
                    self.home_team
                )

                self.home_score += 1


                if show_events:

                    print()

                    print(
                        f"GOAL! {self.home_team.team_name}"
                    )

                    print(
                        f"Scorer: {scorer.player_name}"
                    )

                    print(
                        f"Minute: {minute}'"
                    )


        # Away team goal attempt

        elif random.random() < away_goal_chance:

            if self.away_score < 5:

                scorer = self.choose_goal_scorer(
                    self.away_team
                )

                self.away_score += 1


                if show_events:

                    print()

                    print(
                        f"GOAL! {self.away_team.team_name}"
                    )

                    print(
                        f"Scorer: {scorer.player_name}"
                    )

                    print(
                        f"Minute: {minute}'"
                    )


    # ==================================================
    # PLAY MATCH
    # ==================================================

    def play_match(self):

        home_goal_chance, away_goal_chance = (
            self.prepare_match()
        )


        print()

        print(
            f"{self.home_team.team_name} "
            f"vs "
            f"{self.away_team.team_name}"
        )

        print()


        for minute in range(0, 91):

            progress_length = 30


            progress = int(
                (minute / 90)
                * progress_length
            )


            bar = (
                "█" * progress
                + "-" * (
                    progress_length - progress
                )
            )


            print(
                f"\r{minute:02d}' [{bar}]",
                end="",
                flush=True
            )


            self.simulate_minute(
                minute,
                home_goal_chance,
                away_goal_chance,
                show_events=True
            )


            time.sleep(0.2)


        print()

        print()

        print(
            f"FINAL SCORE: "
            f"{self.home_team.team_name} "
            f"{self.home_score} - "
            f"{self.away_score} "
            f"{self.away_team.team_name}"
        )

        print()


        return self.home_score, self.away_score


    # ==================================================
    # QUICK MATCH
    # ==================================================

    def quick_match(self):

        home_goal_chance, away_goal_chance = (
            self.prepare_match()
        )


        for minute in range(0, 91):

            self.simulate_minute(
                minute,
                home_goal_chance,
                away_goal_chance,
                show_events=False
            )


        return self.home_score, self.away_score


# ==================================================
# CREATE GROUPS
# ==================================================

groups = {}


for team in team_objects:

    if team.group_name not in groups:

        groups[team.group_name] = []


    groups[team.group_name].append(team)


# ==================================================
# CREATE GROUP MATCHES
# ==================================================

group_matches = []


for group_name in groups:

    group_teams = groups[group_name]


    for i in range(len(group_teams)):

        for j in range(i + 1, len(group_teams)):

            home_team = group_teams[i]

            away_team = group_teams[j]


            group_matches.append(
                (
                    group_name,
                    home_team,
                    away_team
                )
            )


# ==================================================
# CREATE GROUP TABLES
# ==================================================

group_tables = {}


for group_name in groups:

    group_tables[group_name] = {}


    for team in groups[group_name]:

        group_tables[group_name][team.team_id] = {

            "team": team,

            "played": 0,

            "wins": 0,

            "draws": 0,

            "losses": 0,

            "goals_for": 0,

            "goals_against": 0,

            "goal_difference": 0,

            "points": 0
        }


# ==================================================
# UPDATE GROUP TABLE
# ==================================================

def update_group_table(
    group_name,
    home_team,
    away_team,
    home_score,
    away_score
):

    home_data = group_tables[
        group_name
    ][
        home_team.team_id
    ]


    away_data = group_tables[
        group_name
    ][
        away_team.team_id
    ]


    home_data["played"] += 1

    away_data["played"] += 1


    home_data["goals_for"] += home_score

    home_data["goals_against"] += away_score


    away_data["goals_for"] += away_score

    away_data["goals_against"] += home_score


    home_data["goal_difference"] = (
        home_data["goals_for"]
        - home_data["goals_against"]
    )


    away_data["goal_difference"] = (
        away_data["goals_for"]
        - away_data["goals_against"]
    )


    if home_score > away_score:

        home_data["wins"] += 1

        away_data["losses"] += 1

        home_data["points"] += 3


    elif away_score > home_score:

        away_data["wins"] += 1

        home_data["losses"] += 1

        away_data["points"] += 3


    else:

        home_data["draws"] += 1

        away_data["draws"] += 1

        home_data["points"] += 1

        away_data["points"] += 1


# ==================================================
# SORT GROUP TABLE
# ==================================================

def sort_group_table(group_name):

    table = list(
        group_tables[group_name].values()
    )


    table.sort(

        key=lambda team_data: (

            team_data["points"],

            team_data["goal_difference"],

            team_data["goals_for"]

        ),

        reverse=True
    )


    return table


# ==================================================
# SHOW GROUP TABLE
# ==================================================

def show_group_table(group_name):

    table = sort_group_table(
        group_name
    )


    print()

    print(
        "========================================"
    )

    print(
        f"GROUP {group_name}"
    )

    print(
        "========================================"
    )


    print(
        f"{'Team':25}"
        f"{'P':>3}"
        f"{'W':>3}"
        f"{'D':>3}"
        f"{'L':>3}"
        f"{'GF':>4}"
        f"{'GA':>4}"
        f"{'GD':>4}"
        f"{'PTS':>5}"
    )


    print(
        "----------------------------------------"
    )


    for team_data in table:

        team = team_data["team"]


        print(

            f"{team.team_name:25}"

            f"{team_data['played']:>3}"

            f"{team_data['wins']:>3}"

            f"{team_data['draws']:>3}"

            f"{team_data['losses']:>3}"

            f"{team_data['goals_for']:>4}"

            f"{team_data['goals_against']:>4}"

            f"{team_data['goal_difference']:>4}"

            f"{team_data['points']:>5}"

        )


    print()


# ==================================================
# SELECT USER TEAM
# ==================================================

print()

print(
    "========================================"
)

print(
    "WORLD CUP 2026 SIMULATOR"
)

print(
    "========================================"
)

print()


print("Available teams:")

print()


for team in team_objects:

    print(
        team.team_id,
        "-",
        team.team_name,
        "| Group:",
        team.group_name,
        "| Strength:",
        team.strength
    )


print()


user_team_id = int(
    input("Enter your team ID: ")
)


user_team = None


for team in team_objects:

    if team.team_id == user_team_id:

        user_team = team

        break


if user_team is None:

    print("Invalid team ID.")

    exit()


# ==================================================
# SELECT TACTIC
# ==================================================

print()

print(
    "Choose your tactic:"
)

print(
    "1 - Attacking"
)

print(
    "2 - Control"
)

print(
    "3 - Defensive"
)


tactic_choice = input(
    "Enter choice: "
)


if tactic_choice == "1":

    user_tactic = "Attacking"


elif tactic_choice == "2":

    user_tactic = "Control"


elif tactic_choice == "3":

    user_tactic = "Defensive"


else:

    user_tactic = "Control"


user_team.tactic = user_tactic


print()

print(
    f"You selected: "
    f"{user_team.team_name}"
)

print(
    f"Tactic: {user_team.tactic}"
)

print(
    f"Team Strength: {user_team.strength}"
)


# ==================================================
# SET DEFAULT TACTIC FOR CPU TEAMS
# ==================================================

for team in team_objects:

    if team != user_team:

        team.tactic = random.choice(
            [
                "Attacking",
                "Control",
                "Defensive"
            ]
        )


# ==================================================
# GROUP STAGE
# ==================================================

print()

print(
    "========================================"
)

print(
    "GROUP STAGE START"
)

print(
    "========================================"
)

print()


current_group = None


for match in group_matches:

    group_name = match[0]

    home_team = match[1]

    away_team = match[2]


    if group_name != current_group:

        current_group = group_name

        print()

        print(
            "########################################"
        )

        print(
            f"GROUP {group_name}"
        )

        print(
            "########################################"
        )

        print()


    # User match

    if (
        home_team == user_team
        or away_team == user_team
    ):

        match_engine = MatchEngine(
            home_team,
            away_team
        )


        home_score, away_score = (
            match_engine.play_match()
        )


    # CPU match

    else:

        match_engine = MatchEngine(
            home_team,
            away_team
        )


        home_score, away_score = (
            match_engine.quick_match()
        )


        print(
            f"{home_team.team_name} "
            f"{home_score} - "
            f"{away_score} "
            f"{away_team.team_name}"
        )


    update_group_table(
        group_name,
        home_team,
        away_team,
        home_score,
        away_score
    )


    group_match_list = [
        m for m in group_matches
        if m[0] == group_name
    ]


    if match == group_match_list[-1]:

        show_group_table(
            group_name
        )


# ==================================================
# GROUP STAGE COMPLETE
# ==================================================

print()

print(
    "========================================"
)

print(
    "GROUP STAGE COMPLETE"
)

print(
    "========================================"
)

print()


print(
    f"Your team: {user_team.team_name}"
)

print(
    f"Group: {user_team.group_name}"
)


show_group_table(
    user_team.group_name
)


# ==================================================
# QUALIFIED TEAMS
# ==================================================

qualified_teams = []

third_place_teams = []


# Get the top two teams from every group

for group_name in group_tables:

    table = sort_group_table(
        group_name
    )


    # First place

    first_place = table[0]["team"]

    qualified_teams.append(
        first_place
    )


    # Second place

    second_place = table[1]["team"]

    qualified_teams.append(
        second_place
    )


    # Third place

    third_place = table[2]

    third_place_teams.append(
        third_place
    )


# ==================================================
# BEST THIRD-PLACED TEAMS
# ==================================================

third_place_teams.sort(

    key=lambda team_data: (

        team_data["points"],

        team_data["goal_difference"],

        team_data["goals_for"]

    ),

    reverse=True
)


best_third_place_teams = (
    third_place_teams[:8]
)


# Add the eight best third-placed teams

for team_data in best_third_place_teams:

    qualified_teams.append(
        team_data["team"]
    )


# ==================================================
# SHOW QUALIFIED TEAMS
# ==================================================

print()

print(
    "########################################"
)

print(
    "TEAMS QUALIFIED FOR ROUND OF 32"
)

print(
    "########################################"
)


print()

print(
    "GROUP WINNERS + RUNNERS-UP"
)

print(
    "----------------------------------------"
)


for team in qualified_teams[:24]:

    print(
        team.team_name,
        "-",
        "Group",
        team.group_name
    )


print()

print(
    "BEST THIRD-PLACED TEAMS"
)

print(
    "----------------------------------------"
)


for team_data in best_third_place_teams:

    team = team_data["team"]


    print(

        team.team_name,

        "-",

        "Group",

        team.group_name,

        "| Points:",

        team_data["points"],

        "| GD:",

        team_data["goal_difference"],

        "| GF:",

        team_data["goals_for"]

    )


print()

print(
    "========================================"
)

print(
    "TOTAL QUALIFIED TEAMS:"
)

print(
    len(qualified_teams)
)

print(
    "========================================"
)


# ==================================================
# KNOCKOUT STAGE
# ==================================================

knockout_teams = qualified_teams.copy()


# Randomize the 32 qualified teams once

random.shuffle(
    knockout_teams
)


# ==================================================
# PLAY KNOCKOUT MATCH
# ==================================================

def play_knockout_match(
    home_team,
    away_team
):

    match_engine = MatchEngine(
        home_team,
        away_team
    )


    # User team match

    if (
        home_team == user_team
        or away_team == user_team
    ):

        home_score, away_score = (
            match_engine.play_match()
        )


    # CPU match

    else:

        home_score, away_score = (
            match_engine.quick_match()
        )


        print(
            f"{home_team.team_name} "
            f"{home_score} - "
            f"{away_score} "
            f"{away_team.team_name}"
        )


    # Handle draw

    if home_score == away_score:

        print()

        print(
            "Match is tied."
        )

        print(
            "Penalty shootout..."
        )


        winner = random.choice(
            [
                home_team,
                away_team
            ]
        )


        print(
            f"Winner: {winner.team_name}"
        )


        return winner


    # Normal winner

    if home_score > away_score:

        return home_team

    else:

        return away_team


# ==================================================
# SHOW RANDOMIZED ROUND OF 32
# ==================================================

print()

print(
    "########################################"
)

print(
    "KNOCKOUT STAGE"
)

print(
    "########################################"
)

print()

print(
    "The 32 qualified teams have been "
    "randomly placed into the bracket."
)

print()


for i in range(
    0,
    len(knockout_teams),
    2
):

    team_1 = knockout_teams[i]

    team_2 = knockout_teams[i + 1]


    print(
        f"Match {i // 2 + 1}: "
        f"{team_1.team_name} vs "
        f"{team_2.team_name}"
    )


# ==================================================
# ROUND OF 32
# ==================================================

print()

print(
    "========================================"
)

print(
    "ROUND OF 32"
)

print(
    "========================================"
)


round_of_32_winners = []


for i in range(
    0,
    32,
    2
):

    home_team = knockout_teams[i]

    away_team = knockout_teams[i + 1]


    print()

    print(
        "----------------------------------------"
    )

    print(
        f"ROUND OF 32 - MATCH {i // 2 + 1}"
    )

    print(
        f"{home_team.team_name} "
        f"vs "
        f"{away_team.team_name}"
    )

    print(
        "----------------------------------------"
    )


    winner = play_knockout_match(
        home_team,
        away_team
    )


    round_of_32_winners.append(
        winner
    )


print()

print(
    "ROUND OF 32 COMPLETE"
)

print()

print(
    "Teams remaining:",
    len(round_of_32_winners)
)


# ==================================================
# ROUND OF 16
# ==================================================

print()

print(
    "========================================"
)

print(
    "ROUND OF 16"
)

print(
    "========================================"
)


round_of_16_winners = []


for i in range(
    0,
    len(round_of_32_winners),
    2
):

    home_team = round_of_32_winners[i]

    away_team = round_of_32_winners[i + 1]


    print()

    print(
        "----------------------------------------"
    )

    print(
        f"ROUND OF 16 - MATCH {i // 2 + 1}"
    )

    print(
        f"{home_team.team_name} "
        f"vs "
        f"{away_team.team_name}"
    )

    print(
        "----------------------------------------"
    )


    winner = play_knockout_match(
        home_team,
        away_team
    )


    round_of_16_winners.append(
        winner
    )


print()

print(
    "ROUND OF 16 COMPLETE"
)

print()

print(
    "Teams remaining:",
    len(round_of_16_winners)
)


# ==================================================
# QUARTER-FINALS
# ==================================================

print()

print(
    "========================================"
)

print(
    "QUARTER-FINALS"
)

print(
    "========================================"
)


quarter_final_winners = []


for i in range(
    0,
    len(round_of_16_winners),
    2
):

    home_team = round_of_16_winners[i]

    away_team = round_of_16_winners[i + 1]


    print()

    print(
        "----------------------------------------"
    )

    print(
        f"QUARTER-FINAL - MATCH {i // 2 + 1}"
    )

    print(
        f"{home_team.team_name} "
        f"vs "
        f"{away_team.team_name}"
    )

    print(
        "----------------------------------------"
    )


    winner = play_knockout_match(
        home_team,
        away_team
    )


    quarter_final_winners.append(
        winner
    )


print()

print(
    "QUARTER-FINALS COMPLETE"
)

print()

print(
    "Teams remaining:",
    len(quarter_final_winners)
)


# ==================================================
# SEMI-FINALS
# ==================================================

print()

print(
    "========================================"
)

print(
    "SEMI-FINALS"
)

print(
    "========================================"
)


semi_final_winners = []


for i in range(
    0,
    len(quarter_final_winners),
    2
):

    home_team = quarter_final_winners[i]

    away_team = quarter_final_winners[i + 1]


    print()

    print(
        "----------------------------------------"
    )

    print(
        f"SEMI-FINAL - MATCH {i // 2 + 1}"
    )

    print(
        f"{home_team.team_name} "
        f"vs "
        f"{away_team.team_name}"
    )

    print(
        "----------------------------------------"
    )


    winner = play_knockout_match(
        home_team,
        away_team
    )


    semi_final_winners.append(
        winner
    )


print()

print(
    "SEMI-FINALS COMPLETE"
)

print()

print(
    "Teams remaining:",
    len(semi_final_winners)
)


# ==================================================
# FINAL
# ==================================================

print()

print(
    "########################################"
)

print(
    "WORLD CUP FINAL"
)

print(
    "########################################"
)


final_home_team = semi_final_winners[0]

final_away_team = semi_final_winners[1]


print()

print(
    f"{final_home_team.team_name} "
    f"vs "
    f"{final_away_team.team_name}"
)

print()


champion = play_knockout_match(
    final_home_team,
    final_away_team
)


# ==================================================
# WORLD CUP CHAMPION
# ==================================================

print()

print(
    "########################################"
)

print(
    "WORLD CUP CHAMPION"
)

print(
    "########################################"
)

print()

print(
    f"CHAMPION: {champion.team_name}"
)

print()

print(
    "########################################"
)