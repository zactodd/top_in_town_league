from utils import update_rankings_from_match


def pprint_rankings_history(previous_ranking_info, matches_info):
    order_players = sorted(previous_ranking_info.keys())
    rankings = previous_ranking_info.copy()
    num_players = len(previous_ranking_info)
    format_row = " {:<12}|" * (num_players + 1)
    score_row = " {:<12}|" + " {:>12}|" * num_players
    line_row = "-" * len(format_row.format(*tuple([""] * (num_players + 1))))
    print(format_row.format("players", *sorted(previous_ranking_info.keys())))
    print(score_row.format("starting mu", *(f'{previous_ranking_info[p].mu:.2f}' for p in order_players)))
    print(line_row)
    print(line_row)
    for m in matches_info:
        teams = {}
        score = {}
        for i, t in enumerate(m, 1):
            teams.update({p: i for p in t["team"]})
            score.update({p: t["score"] for p in t["team"]})
        print(score_row.format("team: ", *(teams[p] if p in teams else "-" for p in order_players)))
        print(score_row.format("score: ", *(score[p] if p in score else "-" for p in order_players)))
        rankings.update(update_rankings_from_match(rankings, m))
        print(score_row.format("mu: ", *(f'{rankings[p].mu:.2f}' for p in order_players)))
        print(line_row)
