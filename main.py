import utils
import visualise
import json
import pprint


FILE = "/home/tutor/Downloads/Unofficial Official Top In Town League - Sheet1.csv"
rank_info, matches_info = utils.csv_to_game_record(FILE)
pprint.pprint(matches_info)
visualise.pprint_rankings_history(rank_info, matches_info)

