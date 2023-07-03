import streamlit as st
from st_clickable_images import clickable_images
import pandas as pd
import numpy as np
import access
import recommend
import json

st.set_page_config(page_title="Content Recommender", page_icon="📈")

st.markdown("# 🎭 Content Recommender")
st.sidebar.header("🎭 Content Recommender")
st.write(
    """Pick a starting point for your recommendations and sit tight.
    Once you get some initial recommendations, feel free to checkout the 
    🔎 **Trope Explorer** to discover the tropes that power your favorite content.
    Love a trope to make sure it gets included in your next batch of recommendations.
    Lastly, Enjoy ClusterTales!"""
)

if "starting_media" not in st.session_state:
    st.session_state["starting_media"] = list()

if 'checked_tropes' not in st.session_state:
    st.session_state['checked_tropes'] = set()

with open('data/title_to_id.json') as json_file:
    title_to_id = json.load(json_file)

starting_media = st.multiselect('Select Media', title_to_id.keys(), default=st.session_state['starting_media'], help='Select the media for which you want recommendations.')

if st.session_state['checked_tropes']:
    st.write('Your loved tropes: ' + ', '.join(list(st.session_state['checked_tropes'])))

if starting_media:
    if st.session_state['checked_tropes']:
        recs = recommend.get_recommendations(starting_media, st.session_state['checked_tropes'])
    else:
        recs = recommend.get_recommendations(starting_media)
    
    st.write('Nearest Neighbors')

    nearest_clicked = clickable_images([access.get_media_image(recs['nearest'][i]) for i in range(len(recs['nearest']))],
                                titles=[access.get_media_name(recs['nearest'][i]) for i in range(len(recs['nearest']))],
                                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                img_style={"margin": "5px", "height": "200px"},
    )
    
    if nearest_clicked != -1:
        name = access.get_media_name(recs['nearest'][clicked])
        if name not in st.session_state['starting_media']:
            st.session_state['starting_media'].append(name)

    st.write('Variety - Nearest Neighboring Cluster')

    variety_clicked = clickable_images([access.get_media_image(recs['variety'][i]) for i in range(len(recs['variety']))],
                                titles=[access.get_media_name(recs['variety'][i]) for i in range(len(recs['variety']))],
                                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                img_style={"margin": "5px", "height": "200px"},
    )
    
    if variety_clicked != -1:
        name = access.get_media_name(recs['variety'][clicked])
        if name not in st.session_state['starting_media']:
            st.session_state['starting_media'].append(name)

if starting_media:
   st.session_state["starting_media"] = starting_media
