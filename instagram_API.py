import requests
import urllib
import json
import openpyxl
import tablib
import statistics as st
import shapely
import numpy as np
import geopy.distance
from datetime import datetime
from access_tokens import ACCESS_TOKEN

BASE_URL = 'https://api.instagram.com/v1/'

def get_user_info():
    # request_url = BASE_URL + 'users/search?q={}access_token={}'.format(insta_username, ACCESS_TOKEN)
    # request_url = 'https://api.instagram.com/v1/tags/nofilter/media/recent?access_token={}'.format(ACCESS_TOKEN)
    # request_url = 'https://api.instagram.com/v1/users/self/?access_token={}'.format(ACCESS_TOKEN) # works!! gives user info

    request_url = 'https://api.instagram.com/v1/users/self/media/recent/?access_token={}'.format(ACCESS_TOKEN) # YES!! gives media info INCLUDING geotag
    # print('GET request url : {}'.format(request_url))
    user_info = requests.get(request_url).json()

    return user_info

def insta_to_excel():
    user_info = get_user_info()
    user_data = user_info['data']

    headers = ('post_number', 'unix', 'user', 'date_time', 'latitude', 'longitude', 'location_name')
    data = tablib.Dataset(headers=headers)
    
    travel_id = 1
    # extract column information from JSON
    for i in range(len(user_data)):
        user_image = user_data[i]

        # oid
        oid = i + 1

        # date
        date = datetime.utcfromtimestamp(int(user_image['created_time'])).strftime('%Y-%m-%d %H:%M:%S.%f')
        unix = user_image['created_time']

        #location
        if user_image['location'] != None:
            latitude = user_image['location']['latitude']
            longitude = user_image['location']['longitude']
            location_name = user_image['location']['name']
        else:
            latitude = None
            longitude = None
            location_name = None

        # username
        user = user_image['user']['username']

        # text = user_image['caption']['text']
        if latitude != None:
            data.append([oid, unix, user, date, latitude, longitude, location_name])
        else:
            continue

    mean_time = stops_and_moves(user_data)

    pddata = (data.export('df')).dropna()
    pddata.to_csv('{}.csv'.format(user))
    # writer = pd.ExcelWriter('{}.xlsx'.format(user))
    # writer.save()

    return data, user_data, mean_time, user

def stops_and_moves(user_data):
    time = []

    for i in range(len(user_data)):
        user_image = user_data[i]
        unix_date = user_image['created_time']
        unix_int = int(unix_date)
        if user_image['location'] != None:
            time = time + [unix_int]
        else:
            continue

    begin_time = time[-1]
    end_time = time[0]

    passed_time = end_time - begin_time
    mean_post_time = passed_time / len(user_data)

    # this part of the function checks for passed time between all posts
    between_time_lst = []

    for i in range(len(time) -1):
        first = time[i]
        second = time[i+1]
        between_time = first - second
        between_time_lst = between_time_lst + [between_time]

    median_between = np.median(between_time_lst)

    return mean_post_time
