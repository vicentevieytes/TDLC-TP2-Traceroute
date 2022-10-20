
import plotly.graph_objects as go
import ipaddress
import json
import requests
from geoip import geolite2
from geopy.geocoders import Nominatim

def parseInfo(file): #---> (List) (ipAddress,(longitude, latitude), city)
    returnedList =[]
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            splittedLine = line.split()
            if len(splittedLine) > 4:
                returnedList.append((splittedLine[0], (float(splittedLine[1]), float(splittedLine[2])), f'{splittedLine[3]} {splittedLine[4]}'))
            else:
                returnedList.append((splittedLine[0], (float(splittedLine[1]), float(splittedLine[2])), splittedLine[3]))
    return returnedList

        
def mapsInit(fig):

    fig.update_layout(
    margin ={'l':50,'t':50,'b':50,'r':50},
    mapbox = {
        'center': {'lon': 10, 'lat': 10},
        'style': "stamen-terrain",
        'center': {'lon': -20, 'lat': -20},
        'zoom': 1})

def addRoute(fig,name,position,color):
    '''
    name --> (str) name of the line
    position --> (tuple) ((lon1,lon2), (lat1,lat2))
    '''
    lonPath = position[0][0]
    latPath = position[0][1]
    city = position[1]

    fig.add_trace(go.Scattergeo(
        name = name,
        mode = "lines",
        line=go.scattergeo.Line(color=color, width=3),
        lon = lonPath,
        lat = latPath,
        marker = {'size':10}))

def mark(fig ,markName, position,name='My IP'):
    '''
    position --> (tuple) (lon,lat)
    '''
    lonPath = position[0]
    latPath = position[1]
    fig.add_trace(go.Scattermapbox(
        name = name,
        text = markName,
        mode = "markers",
        lon = (lonPath,),
        lat = (latPath,),
        marker = {'size': 15}
        ))

# get geo location of the ipList and insert myLoc and TargetLoc

fileNames = ["AustraliaLocationInfo", "IndiaLocationInfo", "QatarLocationInfo", "SudafricaLocationInfo"]

colors = ["red", "green", "yellow","purple"]
offsets = [0.0, 0.2, -0.2, 0.4]

# initiate the maps
fig = go.Figure()
#mapsInit(fig)

for filename, color, offset in zip(fileNames, colors, offsets):

    
    routeLocList = parseInfo(filename)

    # prepare for and linear route in map
    
    routeLocLon =[]
    routeLocLat = []

    for x in routeLocList:
       
        routeLocLon.append(x[1][0])
        routeLocLat.append(x[1][1]+offset)



    # creating the route
    for i in range(len(routeLocLon)-1):
        route_city = routeLocList[i+1][2]
        route_ip = routeLocList[i+1][0]
        print(route_ip,'---',route_city)
        addRoute(fig,f'{route_ip}, {route_city}',((routeLocLon[i:i+2],routeLocLat[i:i+2]),route_city),color)
        
    
fig.write_html("mapa.html")
fig.show()

