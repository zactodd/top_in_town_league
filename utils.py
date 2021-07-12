from trueskill import Rating, rate, TrueSkill
import csv
from collections import defaultdict, Counter
import numpy as np
import random
TrueSkill(mu=25, sigma=8.333, draw_probability=0).make_as_global()


def load_init_rankings(starting_info):
    return {k: Rating(*v) for k, v in starting_info.items()}


def update_rankings_from_match(previous_ranking_info, match_info):
    sorted_teams = sorted(match_info, key=lambda x: x["score"], reverse=True)
    previous_ranking = []
    weights = []
    teams = []
    for t in sorted_teams:
        previous_ranking.append([previous_ranking_info[p] for p in t["team"]])
        weights.append(t["weights"])
        teams.append(t["team"])

    # Score base rankings
    rankings = [max(0, 10 - t["score"]) for t in sorted_teams]

    # Win/loss only rankings
    # rankings = [t["score"] < 10 for t in sorted_teams]

    current_rankings = rate(previous_ranking, weights=weights, ranks=rankings)
    return {p: r for team_rankings in zip(current_rankings, teams) for r, p in zip(*team_rankings)}


def update_rankings_from_matches(previous_ranking_info, matches_info):
    rankings = previous_ranking_info.copy()
    for m in matches_info:
        rankings.update(update_rankings_from_match(rankings, m))
    return rankings


def csv_to_game_record(file):
    with open(file) as f:
        reader = list(csv.DictReader(f))
    num_matches = int(len(reader[0]) / 2)
    match_info = []
    for g in range(1, num_matches + 1):
        match_dict = defaultdict(lambda: {"team": []})
        for r in reader:
            team = r[f"G{g}Team"]
            if team != "":
                match_dict[team]["team"].append(r["Players"])
                match_dict[team]["score"] = int(r[f"G{g}Score"])
        for k, v in match_dict.items():
            team_size = len(match_dict[k]["team"])
            match_dict[k]["weights"] = [1 / team_size] * team_size
        match_info.append(list(match_dict.values()))
    initial_rankings = {r["Players"]: Rating() for r in reader}
    return initial_rankings, match_info


def players_with_min_matches(matches_info, min_matches):
    played = Counter()
    for m in matches_info:
        for t in m:
            for p in t["team"]:
                played[p] += 1
    return {k for k, v in played.items() if v >= min_matches}


def determine_winner(matches_info):
    m = random.choice(matches_info)
    weights = []
    players = []
    total = 0
    for t in m:
        score = int(t["score"])
        if score >= 10:
            score += 10
        for p in t["team"]:
            players.append(p)
            weights.append(score)
            total += score
    return np.random.choice(players, 1, p=[w / total for w in weights])
