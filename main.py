import matplotlib.pyplot as plt
from PIL import Image
import cv2

import utils
import visualise


FILE = "/home/tutor/Downloads/Unofficial Official Top In Town League - Sheet1.csv"
rank_info, matches_info = utils.csv_to_game_record(FILE)
players = sorted(["Zac", "DD", "Kerry", "Gerry", "George", "Henry", "Stephen"])
visualise.pprint_rankings_history(rank_info, matches_info)
for p in players:
    visualise.plot_player_mu(p, rank_info, matches_info)
    visualise.plot_player_score(p, matches_info)
    score = plt.imread(f"figs/{p}_score.png")
    mu = plt.imread(f"figs/{p}_mu.png")
    h_img = cv2.hconcat([score, mu])
    plt.imsave(f"figs/{p}_combined.png", h_img)


img, *imgs = [Image.open(f"figs/{p}_combined.png") for p in players]
img.save(fp="stats.gif", format='GIF', append_images=imgs, save_all=True, duration=2500, loop=0)
