import math
from datetime import timedelta
from geopy.distance import great_circle

def ST_DBSCAN(df, spatial_threshold, temporal_threshold, min_neighbors):
    cluster_label = 0
    NOISE = -1
    UNMARKED = 777777
    stack = []

    # initialize each point with unmarked
    df['cluster'] = UNMARKED
    
    # for each point in database
    for index, point in df.iterrows():
        if df.loc[index]['cluster'] == UNMARKED:
            neighborhood = retrieve_neighbors(index, df, spatial_threshold, temporal_threshold)
            
            if len(neighborhood) < min_neighbors:
                df.set_value(index, 'cluster', NOISE)

            else: # found a core point
                cluster_label = cluster_label + 1
                df.set_value(index, 'cluster', cluster_label)# assign a label to core point

                for neig_index in neighborhood: # assign core's label to its neighbourhood
                    df.set_value(neig_index, 'cluster', cluster_label)
                    stack.append(neig_index) # append neighbourhood to stack
                
                while len(stack) > 0: # find new neighbors from core point neighbourhood
                    current_point_index = stack.pop()
                    new_neighborhood = retrieve_neighbors(current_point_index, df, \
                        spatial_threshold, temporal_threshold)
                    
                    if len(new_neighborhood) >= min_neighbors: # current_point is a new core
                        for neig_index in new_neighborhood:
                            neig_cluster = df.loc[neig_index]['cluster']
                            if (neig_cluster != NOISE) & (neig_cluster == UNMARKED): 
                                df.set_value(neig_index, 'cluster', cluster_label)
                                stack.append(neig_index)
    return df


def retrieve_neighbors(index_center, df, spatial_threshold, temporal_threshold):
    neigborhood = []

    center_point = df.loc[index_center]

    # filter by time 
    min_time = center_point['unix'] - temporal_threshold
    max_time = center_point['unix'] + temporal_threshold

    df = df[(df['unix'] >= min_time) & (df['unix'] <= max_time)]

    # filter by distance
    for index, point in df.iterrows():
        if index != index_center:
            distance = great_circle((center_point['latitude'], center_point['longitude']), \
                (point['latitude'], point['longitude'])).meters
            if distance <= spatial_threshold:
                neigborhood.append(index)

    return neigborhood