import streamlit as st
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as make_subplots
from streamlit_folium import folium_static
import pandas as pd
import folium as fo
import requests

def create_map():
    us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
    fig=px.scatter_mapbox(us_cities,lat="lat",lon="lon",hover_name="City",hover_data=['State','Population'],zoom=3,height=300,color_discrete_sequence=['fuchsia'],title="Population of the 1,000 largest US cities")
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

def create_map_boundry():
    us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
    fig=px.scatter_mapbox(us_cities,lat="lat",lon="lon",hover_name="City",hover_data=['State','Population'],zoom=3,height=300,color_discrete_sequence=['fuchsia'],title="Population of the 1,000 largest US cities")
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(mapbox_bounds={"west": -180, "east": -50, "south": 20, "north": 90})
    st.plotly_chart(fig)


def create_map2():
    us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
    fig=px.scatter_mapbox(us_cities,lat="lat",lon="lon",hover_name="City",hover_data=['State','Population'],zoom=3,height=300,color_discrete_sequence=['fuchsia'],title="Population of the 1,000 largest US cities")

    fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[{
            "below":'traces',
            "sourcetype":"raster",
            "sourceattribution":"United States Geological Survey",
            "source":["https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"]}]
        )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
      

def create_map3():
    data={
        'Name':['Polygon 1','Polygon 2'],
        'Geometry': [
            'POLYGON ((-74.1 40.7, -74.1 40.8, -74.0 40.8, -74.0 40.7, -74.1 40.7))',
            'POLYGON ((-74.2 40.6, -74.2 40.7, -74.1 40.7, -74.1 40.6, -74.2 40.6))'
        ]
    }
    gdf=gpd.GeoDataFrame(data,geometry=gpd.GeoSeries.from_wkt(data['Geometry']))

    fig=px.choropleth_mapbox(
        gdf,
        geojson=gdf.geometry.__geo_interface__,
        locations=gdf.index,
        color='Name',
        mapbox_style='carto-positron',
        center={"lat": gdf.geometry.centroid.y.mean(), "lon": gdf.geometry.centroid.x.mean()},
        zoom=10
        )
    
    st.plotly_chart(fig)


def create_map4():
    token='sk.eyJ1IjoiYXJ5YW5ndXB0YTA1MTAiLCJhIjoiY2xyMzg0OHR6MGtqcTJxbzhtZ2R4aHRnayJ9.nHJjqslAba902tc_SgF47A'
    token2='pk.eyJ1IjoiYXJ5YW5ndXB0YTA1MTAiLCJhIjoiY2t5bGV3aWVrMG43aTJxcG41ZDBpY2cwZiJ9.4ekrP_HyQY8w8mi14lx9hA'
    fig=go.Figure(go.Scattermapbox(
        mode="markers+text+lines",
        lon=[-75,-80,-50], lat=[45,20,-20],
        marker={'size':20,'symbol':['bus','harbor','airport']},
        text=["Bus","Harbor","airport"], textposition="bottom right"))
    fig.update_layout(
        mapbox={
            'accesstoken':token2,
            'style':'outdoors',
            'zoom':1},
        showlegend=False)
    st.plotly_chart(fig)


def get_routes(start_coord,end_coord):
    osrm_url = f"http://router.project-osrm.org/route/v1/driving/{start_coord[1]},{start_coord[0]};{end_coord[1]},{end_coord[0]}"

    response=requests.get(osrm_url)
    route=response.json()

    distance=route['routes'][0]['distance']

    return distance

def create_distance_map():
    start_point=(40.7128,-74.0060) # new york
    end_point=(34.0522,-118.2437) #los angeles

    distance=get_routes(start_point,end_point)
    mymap=fo.Map(location=start_point,zoom_start=5)

    fo.Marker(location=start_point,popup='New York').add_to(mymap)
    fo.Marker(location=end_point,popup='Los Angeles').add_to(mymap)

    fo.PolyLine(locations=[start_point,end_point],color='red',weight=5).add_to(mymap)

    fo.Marker(location=((start_point[0]+end_point[0])/2,(start_point[1]+end_point[1])/2),popup=f'Distance: {distance / 1000:.2f} km').add_to(mymap)

    mymap.save('map.html')
    return mymap

def plot_folium_map():
    mymap=create_distance_map()    
    folium_static(mymap)

def main():
    st.title('Map')
    st.header("Us cites population map")
    create_map()
    st.header("Us cites population map with boundry")
    create_map_boundry()
    st.header("Us cites different layout map")
    create_map2()
    st.header("Polygon map")
    create_map3()
    st.header("Mapbox map with marker")
    create_map4()
    st.header("Distance map")
    plot_folium_map()


if __name__ =='__main__':
    main()        