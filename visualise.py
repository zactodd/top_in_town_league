from utils import update_rankings_from_match
from collections import defaultdict


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
        without_init = pteam, pscore, pwins, pwinrate, ptotal, pavg
        for p in order_players:
            pmu.append(f'{rankings[p].mu:.2f}')
            if p in scores:
                pteam.append(teams[p])
                pscore.append(scores[p])
            else:
                for i in game_prints:
                    i.append("-")
            if p in other_metrics:
                pwins.append(other_metrics[p]["wins"])
                pwinrate.append(f'{other_metrics[p]["wins"] / other_metrics[p]["played"]:.2f}')
                ptotal.append(sum(other_metrics[p]["scores"]))
                pavg.append(f'{sum(other_metrics[p]["scores"]) / other_metrics[p]["played"]:.2f}')
            else:
                for i in without_init:
                    i.append("-")
        print("\n".join(score_row.format(n, *s) for n, s in zip(("team", "score"), game_prints)))
        print(line)
        print("\n".join(score_row.format(n, *s)
                        for n, s in zip(("mu", "wins", "win rate", "total score", "avg score"), post_prints)))
        print(double_line)

    prints = pmu, pwins, pwinrate, ptotal, pavg = [], [], [], [], []
    for p in order_players:
        pmu.append(f'{rankings[p].mu:.2f}')
        pwins.append(other_metrics[p]["wins"])
        pwinrate.append(f'{other_metrics[p]["wins"] / other_metrics[p]["played"]:.2f}')
        ptotal.append(sum(other_metrics[p]["scores"]))
        pavg.append(f'{sum(other_metrics[p]["scores"]) / other_metrics[p]["played"]:.2f}')
    print("\n")
    print(line)
    print(format_row.format("players", *sorted(previous_ranking_info.keys())))
    print(line)
    print("\n".join(score_row.format(n, *s)
                    for n, s in zip(("mu", "wins", "win rate", "total score", "avg score"), prints)))
    print(line)




