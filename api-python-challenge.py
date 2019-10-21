#WeatherPy

# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import json

# Import API key
from api_keys import api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)

#Generate Cities List

# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)

#Convert city list into dataframe
cities_pd = pd.DataFrame(cities)
cities_pd.describe()
cities_pd.head()

#Set Base URL
base_url = "http://api.openweathermap.org/data/2.5/weather?"

results = []

cloudiness = []
country = []
date = []
humidity = []
lat = []
lng =[]
max_temp = []
wind_speed = []

counter = 0
set_counter = 0


for city in cities:
    url = f"{base_url}q={city}&APPID={api_key}"
    weather = requests.get(url).json()
    
    #print(json.dumps(weather, indent = 4, sort_keys = False))
    
    #Append data to lists
    cloudiness.append(weather['clouds']['all'])
    country.append(weather['sys']['country'])
    date.append(weather['dt'])
    humidity.append(weather['main']['humidity'])
    max_temp.append(weather['main']['temp_max'])
    wind_speed.append(weather['wind']['speed'])
    lat.append(weather['coord']['lat'])
    lng.append(weather['coord']['lon'])
    
    if counter <50:
        counter +=1
    elif counter >=50:
        counter = 0
        set_counter +=1
    print(f"Weather data from {city.upper()} requested: city {counter} out of 49, from set {set_counter}")

#Transform extracted data into dataframe
ls_zip = zip(cities, cloudiness, country, date, humidity, max_temp, wind_speed, lat, lng)

weather_df = pd.DataFrame(data = ls_zip)
weather_df = weather_df.rename(columns = {0:"Cities",
                                          1: "Cloudiness",
                                          2: "Country",
                                          3: "Date",
                                          4: "Humidity",
                                          5: "Max Temp",
                                          6: "Wind Speed",
                                          7: "Latitude",
                                          8: "Longitude"
                                         })

#Latitude vs Temperature (Kelvin) Scatter plot
plt.scatter(lat, max_temp, edgecolors = 'k')
plt.xlabel("Latitude")
plt.ylabel("Temperature (Kelvin)")
plt.grid()

plt.title(f"Latitude vs Temperature (Kelvin) ({weather_df['Date'][0]})")
plt.show(block = False)

#Latitude vs Humidity (%) Scatter plot
plt.scatter(lat, humidity, edgecolors = 'k')
plt.xlabel("Latitude")
plt.ylabel("Humidity (%)")
plt.xlim(-95,95)
plt.ylim(65,102)
plt.grid()

plot_date = datetime.fromtimestamp(weather_df['Date'][0]).date()
plt.title(f"City Latitude vs Humidity (%) ({plot_date})")
plt.show(block = False)

#Latitude vs Cloudiness (%) Scatter plot
plt.scatter(lat, cloudiness, edgecolors = 'k')
plt.xlabel("Latitude")
plt.ylabel("Cloudiness")
plt.xlim(-95,95)

plt.grid()

plot_date = datetime.fromtimestamp(weather_df['Date'][0]).date()
plt.title(f"City Latitude vs Cloudiness (%) ({plot_date})")
plt.show(block = False)

#Latitude vs Wind Speed (m/s) Scatter plot
plt.scatter(lat, wind_speed, edgecolors = 'k')
plt.xlabel("Latitude")
plt.ylabel("Wind Speed (m/s)")
plt.xlim(-95,95)

plt.grid()

plot_date = datetime.fromtimestamp(weather_df['Date'][0]).date()
plt.title(f"City Latitude vs Wind Speed (m/s) ({plot_date})")
plt.show(block = False)
