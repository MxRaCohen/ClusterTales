"""
Author: Ra Cohen (ra.q.cohen@gmail.com)
Date: Jun 24, 2023
Purpose: Interaction logic for working with trope-based content recommendations.
"""
import pandas as pd
import numpy as np
import json
import access
import networkx as nx
from sklearn.cluster import KMeans

print('loading expanded tags')
expanded_tags = pd.read_csv('data/id_to_expanded_tropes.csv', index_col='id_')

# Build the trope graph
def get_trope_graph(verbose=False):
    if verbose:
        print('getting trope graph')
    raw_tropes = pd.read_csv('data/tropes.csv')
    
    node_list = raw_tropes.iloc[:29024,]
    node_list = node_list[['_id', 'name', 'url']]
    
    edge_list = raw_tropes.iloc[29024:,]
    edge_list = edge_list[['_start', '_end']]
    
    # Let's get our graph from trope to trope instead of trope id's 
    id_to_trope = dict()
    for dict_ in node_list.to_dict(orient='records'):
        id_to_trope[dict_['_id']] = dict_['name']
    
    named_edge_list = list()
    for edge in list(edge_list.itertuples(index=False)):
        start = edge[0]
        end = edge[1]
        named_edge_list.append((id_to_trope[start], id_to_trope[end]))
    
    trope_graph = nx.MultiDiGraph()
    # Add our edges
    keys = trope_graph.add_edges_from(named_edge_list)


    # Prune the missing tropes
    current_nodes = [i for i in trope_graph.__iter__()]
    for node in current_nodes:
        if node not in expanded_tags.columns:
            trope_graph.remove_node(node)
    
    return trope_graph

trope_graph = get_trope_graph()

# Verify content contains required tropes
def check_required_tropes(content_id, mandatory_tropes, verbose=False):
    if verbose:
        print('checking required tropes')
    present_tropes = set(access.get_tropes_from_media(content_id))
    present_and_required = present_tropes.union(set(mandatory_tropes))
    if len(present_and_required) == len(present_tropes):
        return True
    return False

# Input is a list of names of content as selected in the multi-select and 
# and mandatory trope list from trope explorer
def find_candidates(input_list, mandatory_tropes = None, verbose=False):
    if verbose:
        print('finding candidates')
    original_ids = list()
    for content in input_list:
        original_ids.append(access.get_id_from_title(content))
    
    original_tropes = set()
    for id_ in original_ids:
        for trope in access.get_tropes_from_media(id_):
            original_tropes.add(trope)
    
    original_candidates = set()
    for trope in original_tropes:
        for content in access.get_media_from_tropes(trope):
            if mandatory_tropes:
                if check_required_tropes(content, mandatory_tropes):
                    original_candidates.add(content)
            else:
                original_candidates.add(content)
    
    if len(original_candidates) > 100:
        return (original_ids, original_candidates)
    
    expanded_tropes = set()
    for trope in original_tropes:
        try:
            for neighbor in trope_graph.neighbors(trope):
                expanded_tropes.add(neighbor)
        except:
            pass
    
    candidates = set()
    for trope in expanded_tropes:
        for content in access.get_media_from_tropes(trope):
            if mandatory_tropes:
                if check_required_tropes(content, mandatory_tropes):
                    candidates.add(content)
            else:
                candidates.add(content)
    
    # Return original ids and candidate ids
    return (original_ids, candidates)

# Find subset of expanded tags based on tropes
def find_candidate_expanded_tags(candidates, verbose=False):
    if verbose:
        print('finding candidates expanded tags')
    starting_df = expanded_tags.loc[candidates]
    bool_cols = ~starting_df.any(bool_only=True)
    only_falses = bool_cols[bool_cols]
    # Get the names of these columns
    cols_only_falses = only_falses.index.to_list()
    # Remove these columns
    df = starting_df.drop(cols_only_falses, axis=1)
    return df


# Define the manhattan distance
def manhattan_distance(point1, point2):
    distance = 0
    for x1, x2 in zip(point1, point2):
        difference = x2 - x1
        absolute_difference = abs(difference)
        distance += absolute_difference

    return distance

# Given an amalgamation of the original ids and a dataset, return n closest
def get_n_nearest_neighbors(amalgam, remainder, n=4, verbose=False):
    if verbose:
        print('getting nearest neighbors')
    distances = list()
    for id_ in remainder.index:
        # Calculate the manhattan distance between the reduced original and each candidate
        candidate = remainder.loc[id_]
        difference = manhattan_distance(amalgam, candidate)
        distances.append((difference, id_))
    
    distances.sort(reverse=True)
    n_nearest_ids = list()
    for dist, id_ in distances[0:n]:
        n_nearest_ids.append(id_)

    return n_nearest_ids

# Execute clustering and get recommendations both in and out of the home cluster
def get_recommendations_from_expanded_candidates(original_ids, candidates, n=4, verbose=False):
    if verbose:
        print('getting recommendations from expanded candidates')
    # Amalgamate original content to 1 central node
    originals = candidates.loc[original_ids]
    reduced_original = originals.any(axis=0)
    remainder = candidates.drop(original_ids)
    
    # Add amalgam back to remainder
    remainder.loc['amalgam'] = reduced_original.transpose()
    
    
    # Initialize Clustering to n different clusters + home cluster
    if remainder.shape[0] > n+1:
        kmeans = KMeans(n_clusters=n+1)
    else:
        neighbors = dict()
        
        neighbors['nearest'] = [x for x in remainder.drop('amalgam').index]
        neighbors['variety'] = list()
        print('early return due to insufficient neighbors')
        return neighbors

    # Fit
    kmeans.fit(remainder)

    # Predict
    cluster_labels = kmeans.predict(remainder)

    remainder['cluster'] = cluster_labels
    home_cluster = remainder.loc['amalgam']['cluster']
    
    nearest_n_neighbors = get_n_nearest_neighbors(reduced_original, remainder.loc[remainder['cluster'] == home_cluster].drop(columns=['cluster']), n)
    
    nearest_n_different_neighbors = list()
    for i in range(n+1):
        if i != home_cluster:
            nearest_n_different_neighbors.extend(get_n_nearest_neighbors(reduced_original, remainder.loc[remainder['cluster'] == i].drop(columns=['cluster']), 1))
    
    neighbors = dict()
    neighbors['nearest'] = nearest_n_neighbors
    neighbors['variety'] = nearest_n_different_neighbors
    
    return neighbors

# External accessor function to run the whole pipeline
def get_recommendations(starting_media, mandatory_tropes=None, verbose=False):
    if verbose:
        print('getting recommendations')
    original_ids, candidates = find_candidates(starting_media, mandatory_tropes, verbose)
    expanded_candidates = find_candidate_expanded_tags(candidates, verbose)
    recs = get_recommendations_from_expanded_candidates(original_ids, expanded_candidates, verbose)
    return recs
    