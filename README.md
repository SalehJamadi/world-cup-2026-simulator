# ⚽ World Cup 2026 Simulator

A command-line World Cup simulator built with Python.

The idea was simple: **choose a national team, make tactical decisions, and experience an entire World Cup while the rest of the tournament is simulated in the background.**

The project simulates **48 teams and 528 players**, from the group stage all the way to the final.

---

## 🚀 How to Run

Clone the repository:

```bash
git clone https://github.com/SalehJamadi/world-cup-2026-simulator.git
```

Enter the project folder:

```bash
cd world-cup-2026-simulator
```

Run the simulator:

```bash
python main.py
```

Make sure these files are in the same directory:

```text
main.py
world_cup_2026_teams.csv
world_cup_2026_players.csv
```

**Requirements:** Python 3.x — no external packages required.

---

## 🎮 Features

* Choose one of 48 national teams
* 12 groups with 4 teams each
* Full group-stage simulation
* Top 2 + 8 best third-place teams qualify
* Round of 32 → Final
* Extra time and penalty shootouts
* Attacking, Control and Defensive tactics
* CPU tactical decisions
* Team strength based on player ratings
* Player goals and assists
* Player match ratings
* Player of the Match
* Yellow cards
* Match history
* Group tables
* Top scorers
* Tournament statistics
* Interactive tournament menu
* Silent background simulation for CPU matches

---

## 🏆 Tournament Structure

```text
48 Teams
   ↓
12 Groups × 4
   ↓
Top 2 + 8 Best Third-Place
   ↓
32 Teams
   ↓
Round of 32
   ↓
Round of 16
   ↓
Quarter-finals
   ↓
Semi-finals
   ↓
Final
   ↓
🏆 Champion
```

---

## 🧠 How It Works

The simulator calculates team strength from individual player ratings.

Players are grouped into:

* DEF — Defenders
* MID — Midfielders
* ATT — Attackers

The Match Engine uses team strength, tactics and randomness to generate match outcomes.

Before your matches, you can choose:

**Attacking** — more attacking power with greater defensive risk.

**Control** — balanced approach.

**Defensive** — stronger defensive performance with reduced attacking output.

CPU teams choose their tactics automatically based partly on the strength difference between the teams.

---

## 👤 Player System

Players have individual tournament statistics, including:

* Matches
* Goals
* Assists
* Player of the Match awards
* Yellow cards
* Match ratings
* Average rating

Their performances can affect their match ratings throughout the tournament.

---

## 📊 Data

The project uses CSV files for its initial tournament data.

### `world_cup_2026_teams.csv`

Contains the 48 teams and their group information.

### `world_cup_2026_players.csv`

Contains 528 players, including their:

* ID
* Team
* Name
* Position
* Rating

The CSV data is loaded into Python objects when the program starts.

---

## 🧱 Project Structure

```text
World-Cup-2026-Simulator/
│
├── main.py
├── world_cup_2026_teams.csv
├── world_cup_2026_players.csv
└── README.md
```

The main simulation logic intentionally remains in a single Python file. The goal was to understand and build the complete system rather than hide the logic behind unnecessary complexity.

---

## 🐍 Built With

**Python**

Main concepts used:

* Object-Oriented Programming
* Classes and objects
* CSV data handling
* Lists and dictionaries
* Functions and loops
* Randomized simulation
* Sorting and data processing
* State management
* Command-line interfaces

Only Python's standard library is required.

---

## 🤖 AI-Assisted Development

AI tools were used during development as programming assistants, mainly for debugging, exploring implementation ideas, and solving specific coding problems.

The **project concept, architecture, tournament logic, simulation rules, feature planning, and overall development direction were designed by me.**

AI was used as a development tool and learning assistant, not to generate the project as a whole.

---

## 📌 Current Status

**Version: 0.1**

The core tournament simulation is working.

* [x] 48 teams
* [x] 528 players
* [x] Group stage
* [x] Qualification system
* [x] Knockout stages
* [x] Tactical system
* [x] Match Engine
* [x] Extra time
* [x] Penalty shootouts
* [x] Player statistics
* [x] Match history
* [x] Group tables
* [x] Top scorers
* [x] Tournament menu
* [x] Background CPU simulation

---

## ❤️ About the Project

This project started as a football idea and became a way for me to practice building a larger Python system.

Instead of making a small exercise, I wanted to work with **classes, structured data, simulation logic, state management, randomness and user interaction** in one project.

It's still evolving, but the core tournament engine is already playable.

**Pick a team. Make your decisions. Survive the tournament. Lift the trophy. 🏆**
