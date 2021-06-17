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
        print(format_row.format("team", *(teams[p] if p in teams else "-" for p in order_players)))
        print(score_row.format("score", *(scores[p] if p in scores else "-" for p in order_players)))
        print(line)
        print(score_row.format("mu", *(f'{rankings[p].mu:.2f}' for p in order_players)))
        print(score_row.format("wins", *(other_metrics[p]["wins"] if p in other_metrics else "-" for p in order_players)))
        print(score_row.format("win rate",
                               *(f'{other_metrics[p]["wins"] / other_metrics[p]["played"]:.2f}'
                                 if p in other_metrics else "-" for p in order_players)))
        print(score_row.format("total score", *(sum(other_metrics[p]["scores"]) if p in other_metrics else "-" for p in order_players)))
        print(score_row.format("avg score", *(f'{sum(other_metrics[p]["scores"]) / other_metrics[p]["played"]:.2f}' if p in other_metrics else "-" for p in order_players)))
        print(double_line)

