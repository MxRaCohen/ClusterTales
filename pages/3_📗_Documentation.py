"""
Author: Ra Cohen (ra.q.cohen@gmail.com)
Date: June 24, 2023
Purpose: Build a streamlit app for my user interface of my skateboard. 
"""
import streamlit as st

st.set_page_config(
    page_title="Documentation",
    page_icon="📗",
)

st.write("# How Pop Tropeica Works! 📗")

st.sidebar.success("Explore our recommendations above.")

st.write('ClusterTales contains five stages including the user interface.')

st.image('images/ClusterTalesPipeline.png')

st.markdown(
    """
Firstly, A user selects a piece of media or multiple pieces of media to initialize related recommendations. Optionally they may include 'loved' tropes which must mandatorily be included in the resultant recommendations. 
1. **Candidate Retrieval** occurs in which those given pieces of media are broken into their tropes and then content is surfaced which also contains those tropes. If an insufficient number of candidates is surfaced, the neighbors of those starting tropes is queried from the trope graph and the content containing the neighboring tropes is added to the list of candidates. 
2. The next stage is **Filtering** in which the original content items are removed from the list of candidates as well as any pieces of content that do not contain the user specified tropes if supplied. 
3. In **Scoring** the candidate vectors are K-Means clustered along with an amalgamated vector of the input contents. The ‘home’ cluster is the resultant cluster containing the amalgamation of original inputs and all other clusters are then treated as variety clusters. 
4. Then **Ordering** occurs whereby the Manhattan distance from the amalgamation to each candidate is calculated, returning the 4 closest pieces of media within the home cluster and the closest representative from each variety cluster. 
5. Lastly, these results are then displayed to the user in the **User Interface**, this Streamlit app. 
"""
)