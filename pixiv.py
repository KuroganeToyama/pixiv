import datetime
import os
import glob
import re
from tokens import *

URL_FILE = "urls.txt"
ARTWORK_URL = "https://www.pixiv.net/en/artworks/"

from pixiv_utils.pixiv_crawler import (
    KeywordCrawler,
    UserCrawler,
    RankingCrawler,
    checkDir,
    displayAllConfig,
    download_config,
    network_config,
    ranking_config,
    user_config,
)

if __name__ == "__main__":
    # Clean up
    files = glob.glob(os.path.join("images", '*'))
    for file in files:
        os.remove(file)

    # network_config.proxy["https"] = "127.0.0.1:7890"
    network_config.proxy["https"] = ""
    user_config.user_id = USER_ID
    user_config.cookie = COOKIE
    download_config.with_tag = False
    download_config.url_only = True
    ranking_config.start_date = datetime.date(2024, 9, 23)
    ranking_config.range = 2
    ranking_config.mode = "weekly"
    ranking_config.content_mode = "illust"
    ranking_config.num_artwork = 20

    displayAllConfig()
    checkDir(download_config.store_path)

    # app = RankingCrawler(capacity=20)

    app = UserCrawler(artist_id="9296614", capacity=50)
    
    # app = KeywordCrawler(
    #     keyword="(reimu hakurei OR 博麗霊夢)",
    #     order=False,
    #     mode=["safe", "r18", "all"][0],
    #     n_images=20,
    #     capacity=200,
    # )

    if download_config.url_only == True:
        urls = app.run()

        seen_ids = set()
        with open(URL_FILE, "w") as file:
            for url in urls:
                match = re.search(r'/(\d+)_p', url)
                if match:
                    artwork_id = match.group(1)
                    if artwork_id not in seen_ids:
                        seen_ids.add(artwork_id)
                        pixiv_url = f"{ARTWORK_URL}{artwork_id}"
                        file.write(pixiv_url)
                        file.write('\n')

    else:
        app.run()