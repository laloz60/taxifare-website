import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from branca.element import Template, MacroElement



def get_directions_response(lat1, long1, lat2, long2, mode='drive'):
   url = "https://route-and-directions.p.rapidapi.com/v1/routing"
   key = "60f8aaa46bmsh0932177bac60980p1cc858jsn628fe7c29ba8"
   host = "route-and-directions.p.rapidapi.com"
   headers = {"X-RapidAPI-Key": key, "X-RapidAPI-Host": host}
   querystring = {"waypoints":f"{str(lat1)},{str(long1)}|{str(lat2)},{str(long2)}","mode":mode}
   response = requests.request("GET", url, headers=headers, params=querystring)
   return response

def get_map_data(dict = {}):

    lat_array = [float(pickup_latitude),float(dropoff_latitude)]
    lon_array = [float(pickup_longitude),float(dropoff_longitude)]
    df_map =  pd.DataFrame({"lat":lat_array,
                            "lon":lon_array})

    return df_map

def show_map(df_map,taxi_fare):

    legend_html = """
{% macro html(this, kwargs) %}
<div id='maplegend' class='maplegend'
    style='position: absolute; z-index: 9999; background-color: rgba(255, 255, 255, 0.5);
     border-radius: 6px; padding: 10px; font-size: 10.5px; right: 20px; top: 20px;'>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background: green; opacity: 0.75;'></span>Taxi fare: """+str(taxi_fare)+"""</li>
  </ul>
</div>
</div>
<style type='text/css'>
  .maplegend .legend-scale ul {margin: 0; padding: 0; color: #0f0f0f;}
  .maplegend .legend-scale ul li {list-style: none; line-height: 18px; margin-bottom: 1.5px;}
  .maplegend ul.legend-labels li span {float: left; height: 16px; width: 16px; margin-right: 4.5px;}
</style>
{% endmacro %}
"""

    #Get points to print route
   # response = get_directions_response(df_map['lat'][0], df_map['lon'][0], df_map['lat'][1], df_map['lon'][1])
   # mls = response.json()['features'][0]['geometry']['coordinates']
   # points = [(i[1], i[0]) for i in mls[0]]

    # Create a folium map centered between the two points
    m = folium.Map(location=[df_map['lat'].mean(), df_map['lon'].mean()], zoom_start=13)


    # Add markers for each location
    for index, row in df_map.iterrows():
        folium.Marker([row['lat'], row['lon']], popup=f"Location {index+1}").add_to(m)

    # Add a line between the two points
    folium.PolyLine(locations=[[df_map['lat'][0], df_map['lon'][0]], [df_map['lat'][1], df_map['lon'][1]]], color="red").add_to(m)
   # folium.PolyLine(points, weight=5, opacity=1).add_to(m)
    # Add the legend to the map
    legend = MacroElement()
    legend._template = Template(legend_html)
    m.get_root().add_child(legend)

    st_folium(m, width=700, height=500)

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')



pickup_datetime = st.text_input('date and time', '2014-07-06 19:18:00')
pickup_longitude = st.text_input('pickup longitude', '-73.950655')
pickup_latitude = st.text_input('pickup_latitude', '40.783282')
dropoff_longitude= st.text_input('dropoff longitude', '-73.984365')
dropoff_latitude = st.text_input('dropoff latitude', '40.769802')
passenger_count = st.text_input('passenger count', '2')




url = 'https://taxifare-308943013669.europe-west1.run.app/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

parameters = {"pickup_datetime":pickup_datetime,
              "pickup_longitude":pickup_longitude,
              "pickup_latitude":pickup_latitude,
              "dropoff_longitude":dropoff_longitude,
              "dropoff_latitude":dropoff_latitude,
              "passenger_count":passenger_count}

response = requests.get(url, parameters)

taxi_fare = response.json()['fare']

df_map = get_map_data(parameters)

show_map(df_map,round(taxi_fare,2))




