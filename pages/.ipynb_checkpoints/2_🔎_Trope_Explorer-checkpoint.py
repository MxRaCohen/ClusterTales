import streamlit as st
import pandas as pd
import numpy as np
import access
import json
import pydeck as pdk
from urllib.error import URLError


st.set_page_config(page_title="Trope Explorer", page_icon="🌍")

st.markdown("# Trope Explorer")
st.sidebar.header("Trope Explorer")
st.write(
    """
    - 🔎 Explore the tropes in your media, 
    - ❤️ Love tropes to strengthen your recommendations,  
    - 🧠 Learn about the wide world of tropes.
    """
)

# Load in resources
with open('data/media_to_tropes.json') as json_file:
    media_to_tropes = json.load(json_file)
with open('data/title_to_id.json') as json_file:
    title_to_id = json.load(json_file)
with open('data/all_trope_metadata.json') as json_file:
    all_trope_metadata = json.load(json_file)

# Initialize Tropes from starting media
media_tropes = set()
for media in st.session_state["starting_media"]:
    for trope in media_to_tropes[title_to_id[media]]:
        media_tropes.add(trope)

if 'checked_tropes' not in st.session_state:
    st.session_state['checked_tropes'] = set()

# Initialize dictionary of checked tropes
checked_tropes = dict()

# Update the session state when a trope is checked
def update_states_checked_tropes():

    for trope in checked_tropes.keys():
        if checked_tropes[trope]:
            st.session_state['checked_tropes'].add(trope)

# Create an expander for a trope with relevant info
def create_trope_expander(trope):
    with st.expander(trope):
        if trope in st.session_state and st.session_state[trope]:
            checked_tropes[trope] = st.checkbox('❤️ Love this trope', key=trope, on_change=update_states_checked_tropes, value=True)
        else:
            checked_tropes[trope] = st.checkbox('❤️ Love this trope', key=trope, on_change=update_states_checked_tropes, value=False)
        st.write(all_trope_metadata[trope]['url'])
        st.write('--Descripion--')
        st.write(all_trope_metadata[trope]['description'])
        if st.session_state['starting_media']:
            st.write('--Examples in Your Media--')
            for media in st.session_state['starting_media']:
                id_ = title_to_id[media]
                if id_ in all_trope_metadata[trope]['examples'].keys():
                    st.write(media)
                    st.write('-' + all_trope_metadata[trope]['examples'][id_])
    
# Update your loved tropes
def get_loved_tropes():
    pass

# Lookup tropes not in your media
looked_up_tropes = st.multiselect('Trope Lookup', all_trope_metadata.keys(), default=None, key='manual_loved_tropes', on_change=get_loved_tropes, help='Look up any tropes not in your current media.')

if looked_up_tropes:
    for trope in [trope for trope in looked_up_tropes if trope not in st.session_state['checked_tropes']]:
        create_trope_expander(trope)

if st.session_state['checked_tropes']:
    st.write('Your Loved Tropes')
for trope in st.session_state['checked_tropes']:
    create_trope_expander(trope)
    
st.write('Other Tropes in Your Media')
# Create the checkboxes and store them in the dictionary
sorted_tropes = [trope for trope in media_tropes if trope not in st.session_state['checked_tropes']]
sorted_tropes.sort()
for trope in sorted_tropes:
    create_trope_expander(trope)

