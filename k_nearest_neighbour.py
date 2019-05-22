import instagram_API_script as api
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
import geopy.distance

def get_neighbours(k=1):
    # create array of coordinates
    df = api.insta_to_excel()[0]

    x = []

    for i in df:
        x += [[i[4], i[5]]]

    x = np.array(x)

    dist = distance.squareform(distance.pdist(x))
    closest = np.argsort(dist, axis=1)

    # find maximum distance closest point
    # where 'k' is equal to min_pts in st_dbscan
    
    neigh_lst = closest[:, 1:k+1]
    distances = []
    for i in range(len(neigh_lst)):
        bx = neigh_lst[i]
        a = x[i]
        b = x[bx][k-1]

        distances += [geopy.distance.distance(a, b).m]

    spatial_treshold = max(distances)

    plt.plot(distances)
    # plt.show()
    
    return spatial_treshold
