"""
Author: Ra Cohen (ra.q.cohen@gmail.com)
Date: May 8, 2023
Purpose: Build a streamlit app for my user interface of my skateboard. 
"""
import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to ClusterTales! 👋")

st.sidebar.success("Explore our recommendations above.")

st.markdown(
    """
    ClusterTales is an open-source clustering app built specifically for recommending
    TV shows and movies based on their [Tropes](https://tvtropes.org/pmwiki/pmwiki.php/Main/Trope).
    **👈 Get started with the 🎭 Content Recommender from the sidebar** to see an example
    of what ClusterTales can do!
    ### Want to learn more?
    - After selecting a starting point in the 🎭 **Content Recommender**, check out the 🔎 **Trope Explorer** to learn more about Tropes.
    - Jump into our 📗 **Documentation** to learn more about how ClusterTales works.
    ### Having trouble?
    - ClusterTales works with a large dataset and will likely take upwards of 3 minutes to initialize. Patience is paramount!
    - The images on ClusterTales may be clickable but I do not recommend it as it will reload the entire page again.
    - Tried 'loving' a trope but it didn't work? Try 'loving' a different trope and the first is sure to pop-up!
"""
)

if "starting_media" not in st.session_state:
    st.session_state["starting_media"] = None

if 'checked_tropes' not in st.session_state:
    st.session_state['checked_tropes'] = set()