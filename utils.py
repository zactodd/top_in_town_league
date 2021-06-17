from trueskill import Rating, rate, TrueSkill
TrueSkill(mu=25, sigma=8.333, draw_probability=0).make_as_global()

HISTORY_PATH = "games.json"


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
    # rankings = [max(0, 10 - t["score"]) for t in sorted_teams]

    # Win/loss only rankings
    rankings = [t["score"] < 10 for t in sorted_teams]

    current_rankings = rate(previous_ranking, weights=weights, ranks=rankings)
    return {p: r for team_rankings in zip(current_rankings, teams) for r, p in zip(*team_rankings)}


def update_rankings_from_matches(previous_ranking_info, matches_info):
    rankings = previous_ranking_info.copy()
    for m in matches_info:
        rankings.update(update_rankings_from_match(rankings, m))
    return rankings
