from utils import update_rankings_from_match
from collections import defaultdict
from matplotlib import pyplot as plt
from itertools import accumulate


def pprint_rankings_history(previous_ranking_info, matches_info):
    order_players = sorted(previous_ranking_info.keys())

    rankings = previous_ranking_info.copy()
    other_metrics = defaultdict(lambda: {"scores": [], "wins": 0, "played": 0})
    num_players = len(previous_ranking_info)
    format_row = " {:<15}|" * (num_players + 1)
    score_row = " {:<15}|" + " {:>15}|" * num_players
    line = "-" * len(format_row.format(*tuple([""] * (num_players + 1))))

    double_line = f"{line}\n{line}"

    print(format_row.format("players", *sorted(previous_ranking_info.keys())))
    print(line)
    print(score_row.format("mu", *(f'{previous_ranking_info[p].mu:.2f}' for p in order_players)))
    print(double_line)

    for game_idx, m in enumerate(matches_info, 1):
        teams = {}
        scores = {}
        for i, t in enumerate(m, 1):
            for p in t["team"]:
                score = t["score"]
                teams[p] = "-".join(t["team"])
                scores[p] = score
                other_metrics[p]["scores"].append(score)
                other_metrics[p]["played"] += 1
                if score >= 10:
                    other_metrics[p]["wins"] += 1
        rankings.update(update_rankings_from_match(rankings, m))
        game_prints = pteam, pscore = [], []
        post_prints = pmu, pwins, pwinrate, ptotal, pavg = [], [], [], [], []
        for p in order_players:
            pmu.append(f'{rankings[p].mu:.2f}')
            if p in teams:
                pteam.append(teams[p])
                pscore.append(scores[p])
            else:
                pteam.append("-")
                pscore.append("-")
            if p in other_metrics:
                pwins.append(other_metrics[p]["wins"])
                pwinrate.append(f'{other_metrics[p]["wins"] / other_metrics[p]["played"]:.2f}')
                ptotal.append(sum(other_metrics[p]["scores"]))
                pavg.append(f'{sum(other_metrics[p]["scores"]) / other_metrics[p]["played"]:.2f}')
            else:
                pwins.append("-")
                pwinrate.append("-")
                ptotal.append("-")
                pavg.append("-")
        print("\n".join(score_row.format(n, *s) for n, s in zip(("team", "score"), game_prints)))
        print(line)
        print("\n".join(score_row.format(n, *s)
                        for n, s in zip(("mu", "wins", "win rate", "total score", "avg score"), post_prints)))
        print(double_line)

    prints = pmu, pplayed, pwins, pwinrate, ptotal, pavg = [], [], [], [], [], []
    for p in order_players:
        pmu.append(f'{rankings[p].mu:.2f}')
        pplayed.append(other_metrics[p]["played"])
        pwins.append(other_metrics[p]["wins"])
        pwinrate.append(f'{other_metrics[p]["wins"] / other_metrics[p]["played"]:.2f}')
        ptotal.append(sum(other_metrics[p]["scores"]))
        pavg.append(f'{sum(other_metrics[p]["scores"]) / other_metrics[p]["played"]:.2f}')
    print("\n")
    print(line)
    print(format_row.format("players", *sorted(previous_ranking_info.keys())))
    print(line)
    print("\n".join(score_row.format(n, *s)
                    for n, s in zip(("mu", "played", "wins", "win rate", "total score", "avg score"), prints)))
    print(line)


def plot_mu_over_games(previous_ranking_info, matches_info):
    rankings = previous_ranking_info.copy()
    mu_per_game = {p: [r.mu] for p, r in rankings.items()}

    for game_idx, m in enumerate(matches_info, 1):
        rankings.update(update_rankings_from_match(rankings, m))
        for p, r in rankings.items():
            mu_per_game[p].append(r.mu)

    for x in mu_per_game.values():
        plt.plot(range(1, len(x) + 1), x)
    plt.show()


def plot_delta_mu_over_games(previous_ranking_info, matches_info):
    rankings = previous_ranking_info.copy()
    mu_per_game = {p: [r.mu] for p, r in rankings.items()}

    for game_idx, m in enumerate(matches_info, 1):
        rankings.update(update_rankings_from_match(rankings, m))
        for p, r in rankings.items():
            mu_per_game[p].append(r.mu)

    delta_mus = {p: [j - i for i, j in zip(mu[:-1], mu[1:])] for p, mu in mu_per_game.items()}
    for x in delta_mus.values():
        plt.scatter(range(1, len(x) + 1), x)
    plt.show()


def plot_avg_score_over_games(previous_ranking_info, matches_info):
    order_players = sorted(previous_ranking_info.keys())
    scores = defaultdict(list)

    for m in matches_info:
        played = set()
        for t in m:
            for p in t["team"]:
                scores[p].append(t["score"])
                played.add(p)
        for p in order_players:
            if p not in played:
                scores[p].append(None)
    for s in scores.values():
        x = [avg for avg, *_ in
             accumulate(s,
                        lambda t, a: t if a is None else ((t[1] + a) / (t[2] + 1), t[1] + a, t[2] + 1),
                        initial=(0, 0, 0))
             ]
        plt.scatter(range(1, len(x) + 1), x)
    plt.show()
