import folium
from folium.plugins import MarkerCluster
import instagram_API_script as api
import tablib
from folium.features import DivIcon
import main_stdbscan as scan

## initiate leaflet map
start_coords = [52.0907, 5.1214]
coords = []
my_map = folium.Map(location=start_coords, zoom_start=4)

## create csv and load as dataframe
create_csv = scan.run()
username = api.insta_to_excel()[3]
filen = '{}_res.csv'.format(username)
df = tablib.Dataset().load(open(filen).read())
print(df)

## fill map with info from dataframe
color_lst = ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
             'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
             'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen',
             'gray', 'lightgray']

# add map markers to map
for i in range(len(df)):
    travel_id = int(df[i][-1])
    coord = [float(df[i][-4]), float(df[i][-3])]
    if travel_id != -1:
        folium.Marker(coord, popup=df[i][-2], icon=folium.Icon(icon='cloud', color='{}'.format(color_lst[travel_id]))).add_to(my_map)
    elif travel_id == -1:
        folium.Marker(coord, popup=df[i][-2], icon=folium.Icon(icon='cloud', color='black')).add_to(my_map)
    # add post_number from dataframe to the map
    folium.Marker(coord, icon=DivIcon(html='<div style="font-size: 16pt; font-family:Courier New; color : black">{}</div>'.format(df[i][2]))).add_to(my_map)
    coords += [coord]

# add polylines to map
for i in range(len(coords) - 1):
    travel_id = int(df[i][-1])
    if df[i][-4] != None:
        temp_coords = (coords[i], coords[i + 1])
        folium.PolyLine(temp_coords, color='{}'.format(color_lst[travel_id])).add_to(my_map)
    else:
        continue

## save map as .html
my_map.save('{}_rec.html'.format(api.insta_to_excel()[3]))
