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

    print(format_row.format("players", *sorted(previous_ranking_info.keys())))
    print(line)
    print(score_row.format("mu", *(f'{previous_ranking_info[p].mu:.2f}' for p in order_players)))
    print(line)

    for game_idx, m in enumerate(matches_info, 1):
        print(line)
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
                pwinrate.append(f'{100 * other_metrics[p]["wins"] / other_metrics[p]["played"]:.2f}')
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
        print(line)

    prints = pmu, pplayed, pwins, pwinrate, ptotal, pavg = [], [], [], [], [], []
    for p in order_players:
        pmu.append(f'{rankings[p].mu:.2f}')
        pplayed.append(other_metrics[p]["played"])
        pwins.append(other_metrics[p]["wins"])
        pwinrate.append(f'{100 * other_metrics[p]["wins"] / other_metrics[p]["played"]:.2f}')
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

    for y in mu_per_game.values():
        plt.plot(range(1, len(y) + 1), y)
    plt.plot([1, len(y)], [25, 25], ls="--", c="r", lw=3)
    plt.show()


def plot_delta_mu_over_games(previous_ranking_info, matches_info):
    rankings = previous_ranking_info.copy()
    mu_per_game = {p: [r.mu] for p, r in rankings.items()}

    for game_idx, m in enumerate(matches_info, 1):
        rankings.update(update_rankings_from_match(rankings, m))
        for p, r in rankings.items():
            mu_per_game[p].append(r.mu)

    delta_mus = {p: [j - i if i != j else None for i, j in zip(mu[:-1], mu[1:])] for p, mu in mu_per_game.items()}
    for y in delta_mus.values():
        plt.scatter(range(1, len(y) + 1), y)
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
        y = [avg if p > 0 else None for avg, _, p in
             accumulate(s,
                        lambda t, a: t if a is None else ((t[1] + a) / (t[2] + 1), t[1] + a, t[2] + 1),
                        initial=(0, 0, 0))
             ]
        plt.scatter(range(1, len(y) + 1), y)
    plt.plot([1, len(y)], [4, 4], ls="--", c="r", lw=3)
    plt.show()


def plot_winrate_over_games(previous_ranking_info, matches_info):
    order_players = sorted(previous_ranking_info.keys())
    wins = defaultdict(list)

    for m in matches_info:
        played = set()
        for t in m:
            for p in t["team"]:
                wins[p].append(t["score"] >= 10)
                played.add(p)
        for p in order_players:
            if p not in played:
                wins[p].append(None)
    for s in wins.values():
        y = [w if p > 0 else None for w, _, p in
             accumulate(s,
                        lambda t, a: t if a is None else ((t[1] + a) / (t[2] + 1), t[1] + a, t[2] + 1),
                        initial=(0, 0, 0))
             ]
        plt.scatter(range(1, len(y) + 1), y)
    plt.plot([1, len(y)], [0.25, 0.25], ls="--", c="r", lw=3)
    plt.show()


def plot_player_score(player, matches_info, threhold_name="Gerry"):
    matches, scores, avg_scores, rankings = [], [], [], []
    for i, m in enumerate(matches_info, 1):
        for t in m:
            if player in t["team"]:
                matches.append(f"Game{i}")
                score = int(t["score"])
                scores.append(score)
                avg_scores.append(sum(scores) / len(scores))
                if score < 5:
                    rankings.append("red")
                elif score >= 10:
                    rankings.append("gold")
                else:
                    rankings.append("grey")
                break

    plt.bar(matches, scores, color=rankings)
    plt.plot([-0.5, len(scores) -0.5], [4, 4], c="r", lw=2, alpha=0.7)
    plt.scatter(matches, avg_scores, c="blue", zorder=3, alpha=0.7)
    plt.xticks(rotation=45)

    labels = ["Win", "Loss", f"{threhold_name} threshold", "Avg Score"]
    legend_colours = ["gold", "grey", "red",  "blue"]
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in legend_colours]
    plt.legend(handles, labels, loc='lower center', ncol=2)
    plt.title(f"{player}'s Scores")
    plt.ylabel("Score")
    plt.ylim(2, 12)
    plt.yticks(range(2, 13))
    plt.grid(b=None, which='major', axis='y')
    plt.savefig(f"figs/{player}_score.png")
    plt.close()
    plt.clf()


def plot_player_mu(player, previous_ranking_info, matches_info):
    COLOURS = ["red", "green"]
    rankings = previous_ranking_info.copy()
    matches, mus, detla_mu, colours = [], [], [], []
    prev_mu = 25.0
    for i, m in enumerate(matches_info, 1):
        rankings.update(update_rankings_from_match(rankings, m))
        for t in m:
            if player in t["team"]:
                matches.append(f"Game{i}")
                mus.append((mu := rankings[player].mu) - 25)
                detla_mu.append(delta := mu - prev_mu)
                colours.append(COLOURS[delta > 0])
                prev_mu = mu
                break
    fig, ax = plt.subplots()
    ax.bar(matches, detla_mu, color=colours)
    plt.plot([-0.5, len(matches) - 0.5], [0, 0], ls="-", c="black", lw=3)
    ax.plot(matches, mus, lw="3", c="blue")
    sax = ax.secondary_yaxis('right', functions=(lambda x: x + 25, lambda x: x - 25))
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    sax.set_ylabel("Mu")

    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in ["green", "red", "blue"]]
    plt.legend(handles, ["/\\ mu", "\\/ mu", "mu"], loc='lower center', ncol=2)
    ax.set_title(f"{player}'s Mu")
    ax.set_ylim(-10, 10)
    ax.set_ylabel("Delta Mu")
    plt.grid(b=None, which='major', axis='y')
    plt.savefig(f"figs/{player}_mu.png")
    plt.close()
    plt.clf()


def plot_player_distance_from_second(player, matches_info, threshold_name="George"):
    matches, distances, avg_distance, colour = [], [], [], []
    for i, m in enumerate(matches_info, 1):
        second = sorted(m, key=lambda t: -t["score"])[1]["score"]
        for t in m:
            if player in t["team"]:
                matches.append(f"Game{i}")
                second_distance = int(t["score"]) - second
                distances.append(second_distance)
                avg_distance.append(sum(distances) / len(distances))
                colour.append("green" if second_distance > 0 else "red")

    plt.bar(matches, distances, color=colour)
    labels = ["+2nd Distance", "+2nd Distance", "Avg 2nd Distance"]
    legend_colours = ["green", "red", "blue"]
    plt.plot([-0.5, len(distances) - 0.5], [5, 5], c="black", lw=2, alpha=0.7)
    if threshold_name is not None:
        plt.plot([-0.5, len(distances) -0.5], [5, 5], c="gold", lw=2)
        labels = [">2nd", "<2nd", f"{threshold_name}'s Win", "Avg 2nd Distance"]
        legend_colours = ["green", "red", "gold", "blue"]

    plt.plot([-0.5, len(matches) - 0.5], [0, 0], ls="-", c="black", lw=3)

    plt.scatter(matches, avg_distance, c="blue", zorder=3, alpha=0.7)
    plt.xticks(rotation=45)

    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in legend_colours]
    plt.legend(handles, labels, loc='lower center', ncol=2)
    plt.title(f"{player}'s 2nd Distance")
    plt.ylabel("Score Difference")
    plt.ylim(-6, 6)
    plt.yticks(range(-6, 7))
    plt.grid(b=None, which='major', axis='y')
    plt.savefig(f"figs/{player}_2nd.png")
    plt.close()
    plt.clf()
