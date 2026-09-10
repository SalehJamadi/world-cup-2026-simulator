import csv
import random
import time


# =========================
# Load CSV data
# =========================

teams = []
players = []

with open("world_cup_2026_teams.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        teams.append(row)


with open("world_cup_2026_players.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        players.append(row)


# =========================
# Team class
# =========================

class Team:

    def __init__(self, team_id, team_name, country_code, group_name):

        self.team_id = int(team_id)
        self.team_name = team_name
        self.country_code = country_code
        self.group_name = group_name

        self.players = []

        self.strength = 0
        self.attack_strength = 0
        self.midfield_strength = 0
        self.defense_strength = 0


# =========================
# Player class
# =========================

class Player:

    def __init__(
        self,
        player_id,
        team_id,
        player_name,
        position_group,
        rating
    ):

        self.player_id = int(player_id)
        self.team_id = int(team_id)
        self.player_name = player_name
        self.position_group = position_group
        self.rating = int(rating)

        # Tournament statistics

        self.matches = 0
        self.goals = 0
        self.assists = 0
        self.player_of_match = 0
        self.yellow_cards = 0

        # Match ratings

        self.match_ratings = []
        self.average_rating = 0


# =========================
# Create team objects
# =========================

team_objects = []

for team_data in teams:

    team = Team(
        team_data["team_id"],
        team_data["team_name"],
        team_data["country_code"],
        team_data["group_name"]
    )

    team_objects.append(team)


# =========================
# Create player objects
# =========================

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


# =========================
# Connect players to teams
# =========================

for team in team_objects:

    for player in player_objects:

        if player.team_id == team.team_id:

            team.players.append(player)


# =========================
# Calculate team strengths
# =========================

for team in team_objects:

    if not team.players:
        continue

    total_rating = sum(
        player.rating
        for player in team.players
    )

    team.strength = round(
        total_rating / len(team.players)
    )

    defenders = [
        player.rating
        for player in team.players
        if player.position_group == "DEF"
    ]

    midfielders = [
        player.rating
        for player in team.players
        if player.position_group == "MID"
    ]

    attackers = [
        player.rating
        for player in team.players
        if player.position_group == "ATT"
    ]

    if defenders:

        team.defense_strength = round(
            sum(defenders) / len(defenders)
        )

    if midfielders:

        team.midfield_strength = round(
            sum(midfielders) / len(midfielders)
        )

    if attackers:

        team.attack_strength = round(
            sum(attackers) / len(attackers)
        )


# =========================
# Match History
# =========================

match_history = []


# =========================
# Match Engine
# =========================

class MatchEngine:

    def __init__(self, home_team, away_team):

        self.home_team = home_team
        self.away_team = away_team

        self.home_score = 0
        self.away_score = 0

        self.home_tactic = "Control"
        self.away_tactic = "Control"

        self.home_goal_scorers = []
        self.away_goal_scorers = []

        self.home_assists = []
        self.away_assists = []

        self.home_stats = {
            "possession": 50,
            "shots": 0,
            "shots_on_target": 0,
            "corners": 0,
            "fouls": 0,
            "yellow_cards": 0
        }

        self.away_stats = {
            "possession": 50,
            "shots": 0,
            "shots_on_target": 0,
            "corners": 0,
            "fouls": 0,
            "yellow_cards": 0
        }

        self.match_events = []

        self.extra_time = False
        self.penalty_shootout = False
        self.penalty_winner = None

        self.player_match_ratings = {}

    # =========================
    # Tactic settings
    # =========================

    def get_tactic_modifiers(self, tactic):

        if tactic == "Attacking":

            return {
                "attack": 8,
                "defense": -5,
                "possession": -2,
                "shots": 5
            }

        if tactic == "Defensive":

            return {
                "attack": -5,
                "defense": 8,
                "possession": 2,
                "shots": -2
            }

        return {
            "attack": 2,
            "defense": 2,
            "possession": 4,
            "shots": 1
        }

    # =========================
    # Automatic CPU tactic
    # =========================

    def choose_cpu_tactic(self, team, opponent):

        difference = (
            team.strength
            - opponent.strength
        )

        if difference >= 8:

            return random.choices(
                [
                    "Attacking",
                    "Control",
                    "Defensive"
                ],
                weights=[60, 35, 5]
            )[0]

        if difference <= -8:

            return random.choices(
                [
                    "Attacking",
                    "Control",
                    "Defensive"
                ],
                weights=[10, 40, 50]
            )[0]

        return random.choices(
            [
                "Attacking",
                "Control",
                "Defensive"
            ],
            weights=[25, 55, 20]
        )[0]

    # =========================
    # User tactic selection
    # =========================

    def choose_user_tactic(self):

        if self.home_team == user_team:

            opponent = self.away_team

        else:

            opponent = self.home_team

        print()
        print("=" * 50)
        print("TACTICAL DECISION")
        print("=" * 50)

        print(
            f"Your team: {user_team.team_name}"
        )

        print(
            f"Your strength: {user_team.strength}"
        )

        print(
            f"Opponent: {opponent.team_name}"
        )

        print(
            f"Opponent strength: {opponent.strength}"
        )

        difference = (
            user_team.strength
            - opponent.strength
        )

        if difference >= 8:

            print("Opponent level: WEAKER")

        elif difference <= -8:

            print("Opponent level: STRONGER")

        else:

            print("Opponent level: SIMILAR")

        print()
        print("1. Attacking")
        print("2. Control")
        print("3. Defensive")

        while True:

            choice = input(
                "Choose your tactic: "
            )

            if choice == "1":
                return "Attacking"

            if choice == "2":
                return "Control"

            if choice == "3":
                return "Defensive"

            print(
                "Invalid choice. Please try again."
            )

    # =========================
    # Prepare match
    # =========================

    def prepare_match(self):

        home_modifiers = (
            self.get_tactic_modifiers(
                self.home_tactic
            )
        )

        away_modifiers = (
            self.get_tactic_modifiers(
                self.away_tactic
            )
        )

        home_attack = (
            self.home_team.attack_strength
            + home_modifiers["attack"]
        )

        away_attack = (
            self.away_team.attack_strength
            + away_modifiers["attack"]
        )

        home_defense = (
            self.home_team.defense_strength
            + home_modifiers["defense"]
        )

        away_defense = (
            self.away_team.defense_strength
            + away_modifiers["defense"]
        )

        home_midfield = (
            self.home_team.midfield_strength
        )

        away_midfield = (
            self.away_team.midfield_strength
        )

        home_attack_power = (
            home_attack * 0.55
            + home_midfield * 0.25
            + self.home_team.strength * 0.20
        )

        away_attack_power = (
            away_attack * 0.55
            + away_midfield * 0.25
            + self.away_team.strength * 0.20
        )

        home_goal_chance = (
            0.018
            + (
                home_attack_power
                - away_defense
            ) * 0.0012
        )

        away_goal_chance = (
            0.018
            + (
                away_attack_power
                - home_defense
            ) * 0.0012
        )

        home_goal_chance = max(
            0.006,
            min(0.075, home_goal_chance)
        )

        away_goal_chance = max(
            0.006,
            min(0.075, away_goal_chance)
        )

        home_possession = (
            50
            + (
                home_midfield
                - away_midfield
            ) * 0.7
            + home_modifiers["possession"]
            - away_modifiers["possession"]
        )

        home_possession = max(
            30,
            min(70, home_possession)
        )

        away_possession = (
            100 - home_possession
        )

        self.home_stats["possession"] = round(
            home_possession
        )

        self.away_stats["possession"] = round(
            away_possession
        )

        return (
            home_goal_chance,
            away_goal_chance
        )

    # =========================
    # Choose weighted player
    # =========================

    def choose_weighted_player(
        self,
        players_list
    ):

        if not players_list:

            return None

        weights = []

        for player in players_list:

            # Rating has a direct effect
            # on the probability of selection.

            weight = max(
                1,
                player.rating - 45
            )

            weights.append(weight)

        return random.choices(
            players_list,
            weights=weights,
            k=1
        )[0]

    # =========================
    # Choose goal scorer
    # =========================

    def choose_goal_scorer(self, team):

        attackers = [
            player
            for player in team.players
            if player.position_group == "ATT"
        ]

        midfielders = [
            player
            for player in team.players
            if player.position_group == "MID"
        ]

        defenders = [
            player
            for player in team.players
            if player.position_group == "DEF"
        ]

        # Stronger players have a higher
        # chance to be selected.

        position = random.choices(
            ["ATT", "MID", "DEF"],
            weights=[70, 20, 10]
        )[0]

        if position == "ATT" and attackers:

            return self.choose_weighted_player(
                attackers
            )

        if position == "MID" and midfielders:

            return self.choose_weighted_player(
                midfielders
            )

        if defenders:

            return self.choose_weighted_player(
                defenders
            )

        return self.choose_weighted_player(
            team.players
        )

    # =========================
    # Choose assist player
    # =========================

    def choose_assist_player(
        self,
        team,
        scorer
    ):

        possible_players = [
            player
            for player in team.players
            if player != scorer
        ]

        if not possible_players:

            return None

        # Midfielders and attackers are more
        # likely to provide assists.

        weighted_players = []

        for player in possible_players:

            weight = max(
                1,
                player.rating - 45
            )

            if player.position_group == "MID":

                weight *= 1.5

            elif player.position_group == "ATT":

                weight *= 1.25

            else:

                weight *= 0.65

            weighted_players.append(
                weight
            )

        return random.choices(
            possible_players,
            weights=weighted_players,
            k=1
        )[0]

    # =========================
    # Simulate match minute
    # =========================

    def simulate_minute(
        self,
        minute,
        home_goal_chance,
        away_goal_chance,
        show_events=True
    ):

        # =========================
        # Tactic modifiers
        # =========================

        home_modifiers = (
            self.get_tactic_modifiers(
                self.home_tactic
            )
        )

        away_modifiers = (
            self.get_tactic_modifiers(
                self.away_tactic
            )

        # =========================
        # Shots
        # =========================

        home_shot_chance = (
            0.14
            + home_modifiers["shots"] * 0.01
        )

        away_shot_chance = (
            0.13
            + away_modifiers["shots"] * 0.01
        )

        home_shot_chance = max(
            0.04,
            min(0.30, home_shot_chance)
        )

        away_shot_chance = max(
            0.04,
            min(0.30, away_shot_chance)
        )

        if random.random() < home_shot_chance:

            self.home_stats["shots"] += 1

            if random.random() < 0.38:

                self.home_stats[
                    "shots_on_target"
                ] += 1

        if random.random() < away_shot_chance:

            self.away_stats["shots"] += 1

            if random.random() < 0.37:

                self.away_stats[
                    "shots_on_target"
                ] += 1

        # =========================
        # Corners
        # =========================

        if random.random() < 0.035:

            self.home_stats[
                "corners"
            ] += 1

        if random.random() < 0.033:

            self.away_stats[
                "corners"
            ] += 1

        # =========================
        # Fouls
        # =========================

        if random.random() < 0.08:

            self.home_stats[
                "fouls"
            ] += 1

        if random.random() < 0.08:

            self.away_stats[
                "fouls"
            ] += 1

        # =========================
        # Yellow cards
        # =========================

        if random.random() < 0.012:

            self.home_stats[
                "yellow_cards"
            ] += 1

            yellow_player = random.choice(
                self.home_team.players
            )

            yellow_player.yellow_cards += 1

            event = (
                f"{minute:02d}' Yellow card - "
                f"{yellow_player.player_name} "
                f"({self.home_team.team_name})"
            )

            self.match_events.append(
                event
            )

            if show_events:

                print()
                print(event)

        if random.random() < 0.012:

            self.away_stats[
                "yellow_cards"
            ] += 1

            yellow_player = random.choice(
                self.away_team.players
            )

            yellow_player.yellow_cards += 1

            event = (
                f"{minute:02d}' Yellow card - "
                f"{yellow_player.player_name} "
                f"({self.away_team.team_name})"
            )

            self.match_events.append(
                event
            )

            if show_events:

                print()
                print(event)

        # =========================
        # Home goal
        # =========================

        if random.random() < home_goal_chance:

            if self.home_score < 5:

                self.home_score += 1

                scorer = (
                    self.choose_goal_scorer(
                        self.home_team
                    )
                )

                scorer.goals += 1

                self.home_goal_scorers.append(
                    scorer
                )

                assist_player = (
                    self.choose_assist_player(
                        self.home_team,
                        scorer
                    )
                )

                if assist_player:

                    assist_player.assists += 1

                    self.home_assists.append(
                        assist_player
                    )

                event = (
                    f"{minute:02d}' GOAL! "
                    f"{self.home_team.team_name} - "
                    f"{scorer.player_name}"
                )

                self.match_events.append(
                    event
                )

                if show_events:

                    print()
                    print(event)

                    if assist_player:

                        print(
                            f"Assist: "
                            f"{assist_player.player_name}"
                        )

        # =========================
        # Away goal
        # =========================

        elif random.random() < away_goal_chance:

            if self.away_score < 5:

                self.away_score += 1

                scorer = (
                    self.choose_goal_scorer(
                        self.away_team
                    )
                )

                scorer.goals += 1

                self.away_goal_scorers.append(
                    scorer
                )

                assist_player = (
                    self.choose_assist_player(
                        self.away_team,
                        scorer
                    )
                )

                if assist_player:

                    assist_player.assists += 1

                    self.away_assists.append(
                        assist_player
                    )

                event = (
                    f"{minute:02d}' GOAL! "
                    f"{self.away_team.team_name} - "
                    f"{scorer.player_name}"
                )

                self.match_events.append(
                    event
                )

                if show_events:

                    print()
                    print(event)

                    if assist_player:

                        print(
                            f"Assist: "
                            f"{assist_player.player_name}"
                        )

    # =========================
    # Update player appearances
    # =========================

    def update_player_appearances(self):

        for player in self.home_team.players:

            player.matches += 1

        for player in self.away_team.players:

            player.matches += 1

    # =========================
    # Calculate Player Rating
    # =========================

    def calculate_player_ratings(self):

        all_players = (
            self.home_team.players
            + self.away_team.players
        )

        for player in all_players:

            rating = 6.0

            # Individual quality

            rating += (
                player.rating - 75
            ) * 0.025

            # Goals

            if player in self.home_goal_scorers:

                goals = (
                    self.home_goal_scorers.count(
                        player
                    )
                )

                rating += goals * 1.4

            if player in self.away_goal_scorers:

                goals = (
                    self.away_goal_scorers.count(
                        player
                    )
                )

                rating += goals * 1.4

            # Assists

            if player in self.home_assists:

                assists = (
                    self.home_assists.count(
                        player
                    )
                )

                rating += assists * 0.9

            if player in self.away_assists:

                assists = (
                    self.away_assists.count(
                        player
                    )
                )

                rating += assists * 0.9

            # Winning bonus

            if (
                self.home_score
                > self.away_score
                and player.team_id
                == self.home_team.team_id
            ):

                rating += 0.5

            elif (
                self.away_score
                > self.home_score
                and player.team_id
                == self.away_team.team_id
            ):

                rating += 0.5

            # Yellow card penalty

            if player in self.home_team.players:

                if player in [
                    p
                    for p in self.home_team.players
                    if p.yellow_cards > 0
                ]:

                    rating -= 0.3

            if player in self.away_team.players:

                if player in [
                    p
                    for p in self.away_team.players
                    if p.yellow_cards > 0
                ]:

                    rating -= 0.3

            # Random performance factor

            rating += random.uniform(
                -0.6,
                0.6
            )

            # Keep rating between 4.5 and 10

            rating = max(
                4.5,
                min(10.0, rating)
            )

            rating = round(
                rating,
                1
            )

            self.player_match_ratings[
                player.player_id
            ] = rating

            player.match_ratings.append(
                rating
            )

            player.average_rating = round(
                sum(player.match_ratings)
                / len(player.match_ratings),
                1
            )

    # =========================
    # Calculate Player of Match
    # =========================

    def calculate_player_of_match(self):

        all_players = (
            self.home_team.players
            + self.away_team.players
        )

        best_player = None
        best_score = -999

        for player in all_players:

            score = (
                self.player_match_ratings.get(
                    player.player_id,
                    6.0
                )
            )

            # Extra weight for goals and assists

            if player in self.home_goal_scorers:

                score += (
                    self.home_goal_scorers.count(
                        player
                    ) * 0.8
                )

            if player in self.away_goal_scorers:

                score += (
                    self.away_goal_scorers.count(
                        player
                    ) * 0.8
                )

            if player in self.home_assists:

                score += (
                    self.home_assists.count(
                        player
                    ) * 0.4
                )

            if player in self.away_assists:

                score += (
                    self.away_assists.count(
                        player
                    ) * 0.4
                )

            score += random.uniform(
                0,
                0.4
            )

            if score > best_score:

                best_score = score
                best_player = player

        if best_player:

            best_player.player_of_match += 1

        return best_player

    # =========================
    # Display player ratings
    # =========================

    def show_player_ratings(self):

        print()
        print("=" * 75)
        print("PLAYER RATINGS")
        print("=" * 75)

        print(
            f"{'Player':<30}"
            f"{'Team':<25}"
            f"{'Rating':<10}"
        )

        print("-" * 75)

        all_players = (
            self.home_team.players
            + self.away_team.players
        )

        sorted_players = sorted(
            all_players,
            key=lambda player:
                self.player_match_ratings.get(
                    player.player_id,
                    0
                ),
            reverse=True
        )

        for player in sorted_players:

            if player.team_id == self.home_team.team_id:

                team_name = (
                    self.home_team.team_name
                )

            else:

                team_name = (
                    self.away_team.team_name
                )

            match_rating = (
                self.player_match_ratings.get(
                    player.player_id,
                    0
                )
            )

            print(
                f"{player.player_name:<30}"
                f"{team_name:<25}"
                f"{match_rating:<10.1f}"
            )

        print("=" * 75)

    # =========================
    # Display match statistics
    # =========================

    def show_match_statistics(
        self,
        player_of_match
    ):

        print()
        print("=" * 60)
        print("MATCH STATISTICS")
        print("=" * 60)

        print(
            f"{'Statistic':<20}"
            f"{self.home_team.team_name:<20}"
            f"{self.away_team.team_name:<20}"
        )

        print(
            f"{'Possession':<20}"
            f"{str(self.home_stats['possession']) + '%':<20}"
            f"{str(self.away_stats['possession']) + '%':<20}"
        )

        print(
            f"{'Shots':<20}"
            f"{self.home_stats['shots']:<20}"
            f"{self.away_stats['shots']:<20}"
        )

        print(
            f"{'Shots on Target':<20}"
            f"{self.home_stats['shots_on_target']:<20}"
            f"{self.away_stats['shots_on_target']:<20}"
        )

        print(
            f"{'Corners':<20}"
            f"{self.home_stats['corners']:<20}"
            f"{self.away_stats['corners']:<20}"
        )

        print(
            f"{'Fouls':<20}"
            f"{self.home_stats['fouls']:<20}"
            f"{self.away_stats['fouls']:<20}"
        )

        print(
            f"{'Yellow Cards':<20}"
            f"{self.home_stats['yellow_cards']:<20}"
            f"{self.away_stats['yellow_cards']:<20}"
        )

        print()

        if self.home_goal_scorers:

            print("Home goal scorers:")

            for index, player in enumerate(
                self.home_goal_scorers,
                start=1
            ):

                assist = None

                if index <= len(
                    self.home_assists
                ):

                    assist = (
                        self.home_assists[index - 1]
                    )

                if assist:

                    print(
                        f"- {player.player_name} "
                        f"(Assist: "
                        f"{assist.player_name})"
                    )

                else:

                    print(
                        f"- {player.player_name}"
                    )

        if self.away_goal_scorers:

            print()
            print("Away goal scorers:")

            for index, player in enumerate(
                self.away_goal_scorers,
                start=1
            ):

                assist = None

                if index <= len(
                    self.away_assists
                ):

                    assist = (
                        self.away_assists[index - 1]
                    )

                if assist:

                    print(
                        f"- {player.player_name} "
                        f"(Assist: "
                        f"{assist.player_name})"
                    )

                else:

                    print(
                        f"- {player.player_name}"
                    )

        print()

        if player_of_match:

            potm_rating = (
                self.player_match_ratings.get(
                    player_of_match.player_id,
                    0
                )
            )

            print(
                f"PLAYER OF THE MATCH: "
                f"{player_of_match.player_name} "
                f"({potm_rating:.1f})"
            )

        print("=" * 60)

    # =========================
    # Play user's match
    # =========================

    def play_match(self):

        (
            home_goal_chance,
            away_goal_chance
        ) = self.prepare_match()

        self.update_player_appearances()

        print()
        print(
            f"{self.home_team.team_name} "
            f"vs "
            f"{self.away_team.team_name}"
        )

        print(
            f"Tactics: "
            f"{self.home_team.team_name} = "
            f"{self.home_tactic}"
        )

        print(
            f"Tactics: "
            f"{self.away_team.team_name} = "
            f"{self.away_tactic}"
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

        self.calculate_player_ratings()

        player_of_match = (
            self.calculate_player_of_match()
        )

        self.show_match_statistics(
            player_of_match
        )

        self.show_player_ratings()

        return (
            self.home_score,
            self.away_score,
            player_of_match
        )

    # =========================
    # Quick CPU match
    # =========================

    def quick_match(self):

        self.home_tactic = (
            self.choose_cpu_tactic(
                self.home_team,
                self.away_team
            )
        )

        self.away_tactic = (
            self.choose_cpu_tactic(
                self.away_team,
                self.home_team
            )
        )

        (
            home_goal_chance,
            away_goal_chance
        ) = self.prepare_match()

        self.update_player_appearances()

        for minute in range(0, 91):

            self.simulate_minute(
                minute,
                home_goal_chance,
                away_goal_chance,
                show_events=False
            )

        self.calculate_player_ratings()

        player_of_match = (
            self.calculate_player_of_match()
        )

        return (
            self.home_score,
            self.away_score,
            player_of_match
        )

    # =========================
    # Extra time
    # =========================

    def play_extra_time(
        self,
        show_events=True
    ):

        self.extra_time = True

        print()
        print("=" * 50)
        print("EXTRA TIME")
        print("=" * 50)

        (
            home_goal_chance,
            away_goal_chance
        ) = self.prepare_match()

        home_goal_chance *= 0.70
        away_goal_chance *= 0.70

        for minute in range(91, 121):

            self.simulate_minute(
                minute,
                home_goal_chance,
                away_goal_chance,
                show_events=show_events
            )

            if show_events:

                time.sleep(0.15)

        print()

        print(
            f"AFTER EXTRA TIME: "
            f"{self.home_team.team_name} "
            f"{self.home_score} - "
            f"{self.away_score} "
            f"{self.away_team.team_name}"
        )

        self.calculate_player_ratings()

    # =========================
    # CPU penalty kick
    # =========================

    def cpu_penalty_kick(self):

        directions = [
            "Left",
            "Center",
            "Right"
        ]

        shot_direction = random.choice(
            directions
        )

        goalkeeper_direction = random.choice(
            directions
        )

        if (
            shot_direction
            == goalkeeper_direction
        ):

            return (
                False,
                shot_direction,
                goalkeeper_direction
            )

        return (
            True,
            shot_direction,
            goalkeeper_direction
        )

    # =========================
    # User penalty kick
    # =========================

    def user_penalty_kick(
        self,
        player
    ):

        directions = {
            "1": "Left",
            "2": "Center",
            "3": "Right"
        }

        print()
        print(
            f"Penalty taker: "
            f"{player.player_name}"
        )

        print()
        print("Choose your shot direction:")
        print("1. Left")
        print("2. Center")
        print("3. Right")

        while True:

            choice = input(
                "Your choice: "
            )

            if choice in directions:

                shot_direction = (
                    directions[choice]
                )

                break

            print(
                "Invalid choice."
            )

        goalkeeper_direction = random.choice(
            [
                "Left",
                "Center",
                "Right"
            ]
        )

        print()
        print(
            f"You shot: "
            f"{shot_direction}"
        )

        print(
            f"Goalkeeper dived: "
            f"{goalkeeper_direction}"
        )

        if (
            shot_direction
            == goalkeeper_direction
        ):

            print()
            print("SAVED!")

            return False

        print()
        print("GOAL!")

        return True

    # =========================
    # Select penalty takers
    # =========================

    def get_penalty_takers(
        self,
        team
    ):

        players = team.players.copy()

        players.sort(
            key=lambda player: player.rating,
            reverse=True
        )

        return players

    # =========================
    # Penalty shootout
    # =========================

    def play_penalty_shootout(self):

        self.penalty_shootout = True

        print()
        print("=" * 50)
        print("PENALTY SHOOTOUT")
        print("=" * 50)

        home_takers = (
            self.get_penalty_takers(
                self.home_team
            )
        )

        away_takers = (
            self.get_penalty_takers(
                self.away_team
            )
        )

        home_penalty_score = 0
        away_penalty_score = 0

        # First five penalties

        for round_number in range(5):

            print()
            print(
                f"Penalty round "
                f"{round_number + 1}"
            )

            # Home team

            home_player = home_takers[
                round_number
                % len(home_takers)
            ]

            if self.home_team == user_team:

                home_scored = (
                    self.user_penalty_kick(
                        home_player
                    )
                )

            else:

                (
                    home_scored,
                    shot_direction,
                    goalkeeper_direction
                ) = self.cpu_penalty_kick()

                print(
                    f"{home_player.player_name}: "
                    f"{shot_direction}"
                )

                print(
                    f"Goalkeeper: "
                    f"{goalkeeper_direction}"
                )

                print(
                    "GOAL!"
                    if home_scored
                    else "SAVED!"
                )

            if home_scored:

                home_penalty_score += 1

            # Away team

            away_player = away_takers[
                round_number
                % len(away_takers)
            ]

            if self.away_team == user_team:

                away_scored = (
                    self.user_penalty_kick(
                        away_player
                    )
                )

            else:

                (
                    away_scored,
                    shot_direction,
                    goalkeeper_direction
                ) = self.cpu_penalty_kick()

                print(
                    f"{away_player.player_name}: "
                    f"{shot_direction}"
                )

                print(
                    f"Goalkeeper: "
                    f"{goalkeeper_direction}"
                )

                print(
                    "GOAL!"
                    if away_scored
                    else "SAVED!"
                )

            if away_scored:

                away_penalty_score += 1

            print()
            print(
                f"Penalty score: "
                f"{home_penalty_score} - "
                f"{away_penalty_score}"
            )

            remaining = (
                4 - round_number
            )

            if (
                home_penalty_score
                > away_penalty_score
                + remaining
            ):

                break

            if (
                away_penalty_score
                > home_penalty_score
                + remaining
            ):

                break

        # Sudden death

        sudden_death_round = 1

        while (
            home_penalty_score
            == away_penalty_score
        ):

            print()
            print(
                f"SUDDEN DEATH "
                f"ROUND "
                f"{sudden_death_round}"
            )

            home_player = home_takers[
                (
                    5
                    + sudden_death_round
                    - 1
                )
                % len(home_takers)
            ]

            away_player = away_takers[
                (
                    5
                    + sudden_death_round
                    - 1
                )
                % len(away_takers)
            ]

            # Home team

            if self.home_team == user_team:

                home_scored = (
                    self.user_penalty_kick(
                        home_player
                    )
                )

            else:

                (
                    home_scored,
                    shot_direction,
                    goalkeeper_direction
                ) = self.cpu_penalty_kick()

                print(
                    f"{home_player.player_name}: "
                    f"{shot_direction}"
                )

                print(
                    f"Goalkeeper: "
                    f"{goalkeeper_direction}"
                )

                print(
                    "GOAL!"
                    if home_scored
                    else "SAVED!"
                )

            # Away team

            if self.away_team == user_team:

                away_scored = (
                    self.user_penalty_kick(
                        away_player
                    )
                )

            else:

                (
                    away_scored,
                    shot_direction,
                    goalkeeper_direction
                ) = self.cpu_penalty_kick()

                print(
                    f"{away_player.player_name}: "
                    f"{shot_direction}"
                )

                print(
                    f"Goalkeeper: "
                    f"{goalkeeper_direction}"
                )

                print(
                    "GOAL!"
                    if away_scored
                    else "SAVED!"
                )

            if home_scored:

                home_penalty_score += 1

            if away_scored:

                away_penalty_score += 1

            if (
                home_scored
                and not away_scored
            ):

                break

            if (
                away_scored
                and not home_scored
            ):

                break

            sudden_death_round += 1

        print()
        print("=" * 50)
        print(
            f"PENALTY SCORE: "
            f"{home_penalty_score} - "
            f"{away_penalty_score}"
        )
        print("=" * 50)

        if (
            home_penalty_score
            > away_penalty_score
        ):

            self.penalty_winner = (
                self.home_team
            )

        else:

            self.penalty_winner = (
                self.away_team
            )

        print()
        print(
            f"Penalty winner: "
            f"{self.penalty_winner.team_name}"
        )

        return self.penalty_winner


# =========================
# Groups
# =========================

groups = {}

for team in team_objects:

    if team.group_name not in groups:

        groups[team.group_name] = []

    groups[team.group_name].append(
        team
    )


# =========================
# Create group matches
# =========================

group_matches = {}

for group_name, group_teams in groups.items():

    matches = []

    for i in range(
        len(group_teams)
    ):

        for j in range(
            i + 1,
            len(group_teams)
        ):

            matches.append(
                (
                    group_teams[i],
                    group_teams[j]
                )
            )

    group_matches[group_name] = matches


# =========================
# Group tables
# =========================

group_tables = {}

for group_name, group_teams in groups.items():

    group_tables[group_name] = {}

    for team in group_teams:

        group_tables[
            group_name
        ][team.team_id] = {

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


# =========================
# Update group table
# =========================

def update_group_table(
    group_name,
    home_team,
    away_team,
    home_score,
    away_score
):

    home_data = (
        group_tables[group_name]
        [home_team.team_id]
    )

    away_data = (
        group_tables[group_name]
        [away_team.team_id]
    )

    home_data["played"] += 1
    away_data["played"] += 1

    home_data["goals_for"] += (
        home_score
    )

    home_data["goals_against"] += (
        away_score
    )

    away_data["goals_for"] += (
        away_score
    )

    away_data["goals_against"] += (
        home_score
    )

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
        home_data["points"] += 3

        away_data["losses"] += 1

    elif away_score > home_score:

        away_data["wins"] += 1
        away_data["points"] += 3

        home_data["losses"] += 1

    else:

        home_data["draws"] += 1
        away_data["draws"] += 1

        home_data["points"] += 1
        away_data["points"] += 1


# =========================
# Sort group table
# =========================

def sort_group_table(group_name):

    table = list(
        group_tables[
            group_name
        ].values()
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


# =========================
# Show group table
# =========================

def show_group_table(group_name):

    table = sort_group_table(
        group_name
    )

    print()
    print("=" * 75)
    print(
        f"GROUP {group_name}"
    )
    print("=" * 75)

    print(
        f"{'Team':<25}"
        f"{'P':<5}"
        f"{'W':<5}"
        f"{'D':<5}"
        f"{'L':<5}"
        f"{'GF':<5}"
        f"{'GA':<5}"
        f"{'GD':<5}"
        f"{'PTS':<5}"
    )

    print("-" * 75)

    for team_data in table:

        team = team_data["team"]

        print(
            f"{team.team_name:<25}"
            f"{team_data['played']:<5}"
            f"{team_data['wins']:<5}"
            f"{team_data['draws']:<5}"
            f"{team_data['losses']:<5}"
            f"{team_data['goals_for']:<5}"
            f"{team_data['goals_against']:<5}"
            f"{team_data['goal_difference']:<5}"
            f"{team_data['points']:<5}"
        )

    print("=" * 75)


# =========================
# Record match history
# =========================

def record_match_history(
    stage,
    home_team,
    away_team,
    home_score,
    away_score,
    winner=None,
    penalty=False
):

    match_history.append({

        "stage": stage,

        "home_team": home_team.team_name,

        "away_team": away_team.team_name,

        "home_score": home_score,

        "away_score": away_score,

        "winner": (
            winner.team_name
            if winner
            else None
        ),

        "penalty": penalty
    })


# =========================
# Show match history
# =========================

def show_match_history():

    print()
    print("=" * 70)
    print("MATCH HISTORY")
    print("=" * 70)

    if not match_history:

        print(
            "No matches recorded."
        )

        return

    for index, match in enumerate(
        match_history,
        start=1
    ):

        result = (
            f"{match['home_team']} "
            f"{match['home_score']} - "
            f"{match['away_score']} "
            f"{match['away_team']}"
        )

        print(
            f"{index:02d}. "
            f"[{match['stage']}] "
            f"{result}"
        )

        if match["penalty"]:

            print(
                f"    Winner on penalties: "
                f"{match['winner']}"
            )

    print("=" * 70)


# =========================
# Choose user's team
# =========================

print()
print("=" * 50)
print("WORLD CUP 2026 SIMULATOR")
print("=" * 50)

print()

for team in team_objects:

    print(
        f"{team.team_id:02d}. "
        f"{team.team_name} "
        f"(Group {team.group_name}) "
        f"[Strength: {team.strength}]"
    )

print()

while True:

    try:

        selected_team_id = int(
            input(
                "Choose your team ID: "
            )
        )

        selected_team = next(
            (
                team
                for team in team_objects
                if team.team_id
                == selected_team_id
            ),
            None
        )

        if selected_team:

            user_team = selected_team

            break

        print(
            "Invalid team ID."
        )

    except ValueError:

        print(
            "Please enter a valid number."
        )


print()
print(
    f"You selected: "
    f"{user_team.team_name}"
)

print(
    f"Your team strength: "
    f"{user_team.strength}"
)


# =========================
# Group Stage
# =========================

print()
print("=" * 50)
print("GROUP STAGE")
print("=" * 50)

for group_name in sorted(
    group_matches.keys()
):

    print()
    print(
        f"Starting Group "
        f"{group_name}"
    )

    for home_team, away_team in (
        group_matches[group_name]
    ):

        match_engine = MatchEngine(
            home_team,
            away_team
        )

        # User match

        if (
            home_team == user_team
            or away_team == user_team
        ):

            if home_team == user_team:

                match_engine.home_tactic = (
                    match_engine.choose_user_tactic()
                )

                match_engine.away_tactic = (
                    match_engine.choose_cpu_tactic(
                        away_team,
                        home_team
                    )
                )

            else:

                match_engine.away_tactic = (
                    match_engine.choose_user_tactic()
                )

                match_engine.home_tactic = (
                    match_engine.choose_cpu_tactic(
                        home_team,
                        away_team
                    )
                )

            (
                home_score,
                away_score,
                player_of_match
            ) = match_engine.play_match()

            record_match_history(
                "Group Stage",
                home_team,
                away_team,
                home_score,
                away_score
            )

        # CPU match

        else:

            (
                home_score,
                away_score,
                player_of_match
            ) = match_engine.quick_match()

            print(
                f"{home_team.team_name} "
                f"{home_score} - "
                f"{away_score} "
                f"{away_team.team_name}"
            )

            print(
                f"Player of the Match: "
                f"{player_of_match.player_name}"
            )

            print(
                f"Player of the Match Rating: "
                f"{match_engine.player_match_ratings.get(player_of_match.player_id, 0):.1f}"
            )

            record_match_history(
                "Group Stage",
                home_team,
                away_team,
                home_score,
                away_score
            )

        update_group_table(
            group_name,
            home_team,
            away_team,
            home_score,
            away_score
        )

    show_group_table(
        group_name
    )


# =========================
# Group Stage Complete
# =========================

print()
print("=" * 50)
print("GROUP STAGE COMPLETE")
print("=" * 50)

print()
print(
    f"Your team: "
    f"{user_team.team_name}"
)

show_group_table(
    user_team.group_name
)


# =========================
# Qualification
# =========================

qualified_teams = []

third_place_teams = []

for group_name in group_tables:

    table = sort_group_table(
        group_name
    )

    qualified_teams.append(
        table[0]["team"]
    )

    qualified_teams.append(
        table[1]["team"]
    )

    third_place_teams.append(
        table[2]
    )


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


for team_data in (
    best_third_place_teams
):

    qualified_teams.append(
        team_data["team"]
    )


print()
print("=" * 50)
print("QUALIFIED TEAMS")
print("=" * 50)

for index, team in enumerate(
    qualified_teams,
    start=1
):

    print(
        f"{index:02d}. "
        f"{team.team_name}"
    )


print()
print(
    f"Total qualified teams: "
    f"{len(qualified_teams)}"
)


# =========================
# Knockout Stage
# =========================

knockout_teams = (
    qualified_teams.copy()
)

random.shuffle(
    knockout_teams
)


# =========================
# Knockout match
# =========================

def play_knockout_match(
    home_team,
    away_team,
    stage
):

    match_engine = MatchEngine(
        home_team,
        away_team
    )

    # User match

    if (
        home_team == user_team
        or away_team == user_team
    ):

        if home_team == user_team:

            match_engine.home_tactic = (
                match_engine.choose_user_tactic()
            )

            match_engine.away_tactic = (
                match_engine.choose_cpu_tactic(
                    away_team,
                    home_team
                )
            )

        else:

            match_engine.away_tactic = (
                match_engine.choose_user_tactic()
            )

            match_engine.home_tactic = (
                match_engine.choose_cpu_tactic(
                    home_team,
                    away_team
                )
            )

        (
            home_score,
            away_score,
            player_of_match
        ) = match_engine.play_match()

    # CPU match

    else:

        (
            home_score,
            away_score,
            player_of_match
        ) = match_engine.quick_match()

        print()
        print(
            f"{home_team.team_name} "
            f"{home_score} - "
            f"{away_score} "
            f"{away_team.team_name}"
        )

        print(
            f"Player of the Match: "
            f"{player_of_match.player_name}"
        )

        print(
            f"Rating: "
            f"{match_engine.player_match_ratings.get(player_of_match.player_id, 0):.1f}"
        )

    # Normal winner

    if home_score > away_score:

        winner = home_team

        record_match_history(
            stage,
            home_team,
            away_team,
            home_score,
            away_score,
            winner
        )

        return winner

    if away_score > home_score:

        winner = away_team

        record_match_history(
            stage,
            home_team,
            away_team,
            home_score,
            away_score,
            winner
        )

        return winner

    # =========================
    # Extra Time
    # =========================

    match_engine.play_extra_time(
        show_events=(
            home_team == user_team
            or away_team == user_team
        )
    )

    home_score = (
        match_engine.home_score
    )

    away_score = (
        match_engine.away_score
    )

    if home_score > away_score:

        winner = home_team

        record_match_history(
            stage,
            home_team,
            away_team,
            home_score,
            away_score,
            winner
        )

        print(
            f"Winner after extra time: "
            f"{winner.team_name}"
        )

        return winner

    if away_score > home_score:

        winner = away_team

        record_match_history(
            stage,
            home_team,
            away_team,
            home_score,
            away_score,
            winner
        )

        print(
            f"Winner after extra time: "
            f"{winner.team_name}"
        )

        return winner

    # =========================
    # Penalty Shootout
    # =========================

    winner = (
        match_engine.play_penalty_shootout()
    )

    record_match_history(
        stage,
        home_team,
        away_team,
        home_score,
        away_score,
        winner,
        penalty=True
    )

    return winner


# =========================
# Round of 32
# =========================

print()
print("=" * 50)
print("ROUND OF 32")
print("=" * 50)

round_of_32_winners = []

for i in range(
    0,
    32,
    2
):

    winner = play_knockout_match(
        knockout_teams[i],
        knockout_teams[i + 1],
        "Round of 32"
    )

    round_of_32_winners.append(
        winner
    )


# =========================
# Round of 16
# =========================

print()
print("=" * 50)
print("ROUND OF 16")
print("=" * 50)

round_of_16_winners = []

for i in range(
    0,
    len(round_of_32_winners),
    2
):

    winner = play_knockout_match(
        round_of_32_winners[i],
        round_of_32_winners[i + 1],
        "Round of 16"
    )

    round_of_16_winners.append(
        winner
    )


# =========================
# Quarter-finals
# =========================

print()
print("=" * 50)
print("QUARTER-FINALS")
print("=" * 50)

quarter_final_winners = []

for i in range(
    0,
    len(round_of_16_winners),
    2
):

    winner = play_knockout_match(
        round_of_16_winners[i],
        round_of_16_winners[i + 1],
        "Quarter-final"
    )

    quarter_final_winners.append(
        winner
    )


# =========================
# Semi-finals
# =========================

print()
print("=" * 50)
print("SEMI-FINALS")
print("=" * 50)

semi_final_winners = []

for i in range(
    0,
    len(quarter_final_winners),
    2
):

    winner = play_knockout_match(
        quarter_final_winners[i],
        quarter_final_winners[i + 1],
        "Semi-final"
    )

    semi_final_winners.append(
        winner
    )


# =========================
# Final
# =========================

print()
print("=" * 50)
print("FINAL")
print("=" * 50)

final_home_team = (
    semi_final_winners[0]
)

final_away_team = (
    semi_final_winners[1]
)

champion = play_knockout_match(
    final_home_team,
    final_away_team,
    "Final"
)


# =========================
# Tournament Statistics
# =========================

print()
print("=" * 60)
print("TOURNAMENT STATISTICS")
print("=" * 60)


# =========================
# Top Scorers
# =========================

sorted_scorers = sorted(
    player_objects,
    key=lambda player: (
        player.goals,
        player.assists,
        player.average_rating,
        player.player_of_match,
        player.rating
    ),
    reverse=True
)

top_scorers = [
    player
    for player in sorted_scorers
    if player.goals > 0
]


print()
print("TOP SCORERS")
print("-" * 60)

if top_scorers:

    for index, player in enumerate(
        top_scorers[:10],
        start=1
    ):

        team = next(
            (
                team
                for team in team_objects
                if team.team_id
                == player.team_id
            ),
            None
        )

        print(
            f"{index}. "
            f"{player.player_name} - "
            f"{player.goals} goals - "
            f"{team.team_name}"
        )

else:

    print(
        "No goals recorded."
    )


# =========================
# Most Player of the Match
# =========================

sorted_potm = sorted(
    player_objects,
    key=lambda player: (
        player.player_of_match,
        player.average_rating,
        player.goals,
        player.rating
    ),
    reverse=True
)

top_potm_players = [
    player
    for player in sorted_potm
    if player.player_of_match > 0
]


print()
print(
    "MOST PLAYER OF THE MATCH AWARDS"
)

print("-" * 60)

if top_potm_players:

    for index, player in enumerate(
        top_potm_players[:10],
        start=1
    ):

        team = next(
            (
                team
                for team in team_objects
                if team.team_id
                == player.team_id
            ),
            None
        )

        print(
            f"{index}. "
            f"{player.player_name} - "
            f"{player.player_of_match} awards - "
            f"{team.team_name}"
        )

else:

    print(
        "No Player of the Match awards recorded."
    )


# =========================
# Most Assists
# =========================

sorted_assists = sorted(
    player_objects,
    key=lambda player: (
        player.assists,
        player.goals,
        player.average_rating,
        player.rating
    ),
    reverse=True
)

top_assists = [
    player
    for player in sorted_assists
    if player.assists > 0
]


print()
print("MOST ASSISTS")
print("-" * 60)

if top_assists:

    for index, player in enumerate(
        top_assists[:10],
        start=1
    ):

        team = next(
            (
                team
                for team in team_objects
                if team.team_id
                == player.team_id
            ),
            None
        )

        print(
            f"{index}. "
            f"{player.player_name} - "
            f"{player.assists} assists - "
            f"{team.team_name}"
        )

else:

    print(
        "No assists recorded."
    )


# =========================
# Best Player Ratings
# =========================

players_with_ratings = [
    player
    for player in player_objects
    if player.matches > 0
]

players_with_ratings.sort(
    key=lambda player: (
        player.average_rating,
        player.goals,
        player.assists,
        player.player_of_match
    ),
    reverse=True
)

print()
print("BEST PLAYER RATINGS")
print("-" * 70)

print(
    f"{'Player':<30}"
    f"{'Matches':<10}"
    f"{'Avg Rating':<12}"
    f"{'Goals':<10}"
    f"{'Assists':<10}"
)

print("-" * 70)

for player in players_with_ratings[:10]:

    print(
        f"{player.player_name:<30}"
        f"{player.matches:<10}"
        f"{player.average_rating:<12.1f}"
        f"{player.goals:<10}"
        f"{player.assists:<10}"
    )


# =========================
# Champion
# =========================

print()
print("=" * 60)
print(
    f"CHAMPION: "
    f"{champion.team_name}"
)
print("=" * 60)


# =========================
# User Match History
# =========================

print()
print("=" * 60)
print("YOUR MATCH HISTORY")
print("=" * 60)

user_matches = [
    match
    for match in match_history
    if (
        match["home_team"]
        == user_team.team_name
        or
        match["away_team"]
        == user_team.team_name
    )
]

if user_matches:

    for match in user_matches:

        print()

        print(
            f"[{match['stage']}]"
        )

        print(
            f"{match['home_team']} "
            f"{match['home_score']} - "
            f"{match['away_score']} "
            f"{match['away_team']}"
        )

        if match["penalty"]:

            print(
                f"Winner on penalties: "
                f"{match['winner']}"
            )

else:

    print(
        "No matches found."
    )


# =========================
# User Tournament Summary
# =========================

print()
print("=" * 60)
print("YOUR TOURNAMENT SUMMARY")
print("=" * 60)

user_players = sorted(
    user_team.players,
    key=lambda player: (
        player.goals,
        player.assists,
        player.average_rating,
        player.player_of_match,
        player.rating
    ),
    reverse=True
)

print()
print(
    f"Team: "
    f"{user_team.team_name}"
)

print()
print("Player Performance")

print(
    f"{'Player':<30}"
    f"{'Matches':<10}"
    f"{'Goals':<10}"
    f"{'Assists':<10}"
    f"{'POTM':<10}"
    f"{'Avg Rating':<12}"
)

print("-" * 82)

for player in user_players:

    print(
        f"{player.player_name:<30}"
        f"{player.matches:<10}"
        f"{player.goals:<10}"
        f"{player.assists:<10}"
        f"{player.player_of_match:<10}"
        f"{player.average_rating:<12.1f}"
    )


# =========================
# Full Match History
# =========================

show_match_history()


# =========================
# Tournament Complete
# =========================

print()
print("=" * 60)
print("TOURNAMENT COMPLETE")
print("=" * 60)