import utils
import visualise
import json


with open(utils.HISTORY_PATH) as f:
    games_info = json.load(f)

rank_info = utils.load_init_rankings(games_info["starting_info"])
visualise.pprint_rankings_history(rank_info, games_info["matches"])
