import matplotlib.pyplot as plt
from PIL import Image
import cv2
from collections import Counter
import utils
import visualise
import os


FILE = "Unofficial Official Top In Town League - Sheet1.csv"
rank_info, matches_info = utils.csv_to_game_record(FILE)

played = Counter()
for m in matches_info:
    for t in m:
        for p in t["team"]:
            played[p] += 1
players = sorted({k for k, v in played.items() if v >= 5})

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
