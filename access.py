"""
Author: Ra Cohen (ra.q.cohen@gmail.com)
Date: May 8, 2023
Purpose: Helper functions for working with trope and imdb data
"""
import pandas as pd
import numpy as np
import json
from collections import Counter

with open('data/id_to_poster.json') as json_file:
    id_to_poster = json.load(json_file)

with open('data/id_to_title.json') as json_file:
    id_to_title = json.load(json_file)

with open('data/title_to_id.json') as json_file:
    title_to_id = json.load(json_file)

with open('data/media_to_tropes.json') as json_file:
    media_to_tropes = json.load(json_file)

with open('data/tropes_to_media.json') as json_file:
    tropes_to_media = json.load(json_file)

def get_tropes_from_media(media_id):
    return media_to_tropes[media_id]

def get_media_from_tropes(trope_name):
    return tropes_to_media[trope_name]

def get_all_media_ids():
    return id_to_title.keys()

def get_media_name(media_id):
    return id_to_title[media_id]

def get_media_image(media_id):
    return id_to_poster[media_id]

def get_id_from_title(media_title):
    return title_to_id[media_title]
