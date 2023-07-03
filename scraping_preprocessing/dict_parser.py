"""
Author: Ra Cohen (ra.q.cohen@gmail.com)
Date: May 11, 2023
Purpose: Transform csv's into dictionaries for fast look-up
"""

import pandas as pd
import json


film_tropes = pd.read_csv('data/film_imdb_match.csv')
tv_tropes = pd.read_csv('data/tv_imdb_match.csv')

media_df = pd.concat([film_tropes.tconst, tv_tropes.tconst])


print(media_ids[0])
print(imdb.getFeatures(media_ids[0]))


# media_ids_to_info = {id_ : imdb.get_by_id(id_) for id_ in media_ids}

# with open("data/media_imdb_info.json", "w+") as outfile:
    # json.dump(media_ids_to_info, outfile)
