## ClusterTales
=========================

### Project Overview

Can we produce recommendations without any user-data based instead on a deeper understanding of the content itself? 
What percentage of the corpus are we recommending? Let's find out!


### Walkthrough Demo

1. Initialize enviornment from ClusterTales.env
2. Navigate to this directory
3. Run `streamlit Hello.py`
4. Get Clusterin'!


### Project Organization

This repo contains a lot of information organized in the following manner.

* `scraping_preprocessing`
    - contains all python files and notebooks used to generate the data found in `data` not found in sources

* `data` 
    - contains all of the data used by ClusterTales

* `market_basket_analysis`
    - contains a notebook and output of a market basket analysis using content as baskets of tropes

* `notebooks`
    - contains all final notebooks involved in the project

* `images`
    - contains images used in the streamlit app

* `pages` and `Hello.py`
    - contains pages used in the streamlit app

* `reports`
    - contains final report which summarises the project

* `access.py` and `recommend.py`
    - Contains the project source code (refactored from the notebooks)

* `ClusterTales_env.yml`
    - Conda environment specification

* `README.md`
    - Project landing page (this page)


### Credits & References

* Trope Examples and Trope/Media IMDb match: https://github.com/dhruvilgala/tvtropes
* IMDb dataset: https://developer.imdb.com/non-commercial-datasets/

--------