import matplotlib.pyplot as plt
from PIL import Image
import cv2
import utils
import visualise
import os


FILE = "Unofficial Official Top In Town League - Sheet1.csv"
rank_info, matches_info = utils.csv_to_game_record(FILE)
players = sorted(utils.players_with_min_matches(matches_info, 5))

visualise.pprint_rankings_history(rank_info, matches_info)

if not os.path.exists("figs"):
    os.mkdir("figs")

for p in players:
    visualise.plot_player_mu(p, rank_info, matches_info)
    visualise.plot_player_score(p, matches_info)
    visualise.plot_player_distance_from_second(p, matches_info)
    saved_figs = [f"figs/{p}_score.png", f"figs/{p}_2nd.png", f"figs/{p}_mu.png"]
    h_img = cv2.hconcat([plt.imread(f) for f in saved_figs])
    plt.imsave(f"figs/{p}_combined.png", h_img)


img, *imgs = [Image.open(f"figs/{p}_combined.png") for p in players]
img.save(fp="stats.gif", format='GIF', append_images=imgs, save_all=True, duration=2500, loop=0)
visualise.combinations_wins_distribution(matches_info)
visualise.combinations_score_diff(matches_info)
