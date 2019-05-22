import pandas as pd
from sys import argv
import numpy as np
import STDBSCAN
import instagram_API_script as api
import k_nearest_neighbour as knn

def plot_clusters(df, output_name):
    import matplotlib.pyplot as plt

    labels = df['cluster'].values
    X = df[['longitude', 'latitude']].values

    # Black removed and is used for noise instead.
    cluster_nr = set(labels)
    colours = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(cluster_nr))]
    for k, col in zip(cluster_nr, colours):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6)

    plt.title('Total number of clusters: {}'.format(len(cluster_nr)))
    plt.show()
    # plt.savefig(output_name)

def run():
    username = api.insta_to_excel()[3]
    filen = '{}.csv'.format(username)

    # table must contain 'latitude', 'longitude' and 'date_time'
    df = pd.read_csv(filen)

    spatial_threshold = knn.get_neighbours() # in meters
    temporal_threshold = api.insta_to_excel()[2] # in seconds
    min_neighbours = 1
    df_cluster = STDBSCAN.ST_DBSCAN(df, spatial_threshold, temporal_threshold, min_neighbours)
    print(df_cluster)
    df_cluster.to_csv('{}_res.csv'.format(username))

    return(df_cluster)
