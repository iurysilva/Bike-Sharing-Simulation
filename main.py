import simpy
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from IPython.display import display

from datetime import datetime
from datetime import timedelta
from entities import Station
from entities import Rider

from services import dataset_services as dfs

dataset_station = pd.read_csv('services/datasets/station.csv')

dataset_weather = pd.read_csv('services/datasets/weather.csv')
dataset_weather['Date'] = pd.to_datetime(dataset_weather['Date']).dt.date

dataset_trip = pd.read_csv("services/datasets/trip.csv", error_bad_lines=False)
dataset_trip['Date'] = pd.to_datetime(dataset_trip['starttime']).dt.date


#date_df = dfs.mean_humidity_to_date(dataset_weather,62)
date_df = dfs.mean_to_date(dataset_weather,62,68)
rides_df = pd.merge(dataset_trip,date_df, how='inner', on='Date')

#display(date_df)
#display(rides_df)

#city_graph = nx.Graph()
#city_graph = nx.from_pandas_edgelist(city_graph,'from_station_id','to_station_id')
#nx.draw(city_graph,with_labels=False)
#plt.savefig("filename.png")



environment = simpy.Environment()

initial_time = dataset_trip['starttime'][0]
bikes_avaliable = 100
docks_avaliable = 100
bikes = simpy.Container(environment, capacity=bikes_avaliable, init=bikes_avaliable)
docks = simpy.Container(environment, capacity=docks_avaliable, init=0)

stations = {}
for row in range(len(dataset_station)):
    id = dataset_station.loc[row,'station_id']
    #print(type(id))
    #display(id)
    station = Station(id,environment, initial_time, bikes, docks)
    stations[id] = station
    #print(dataset_station.loc[id,['station_id']])

for row in range(len(rides_df)):
    rider = Rider(environment, row, rides_df['from_station_id'][row], rides_df['to_station_id'][row], rides_df['starttime'][row], rides_df['stoptime'][row])
    environment.process(stations[rider.id_from_station].provide_bike(rider))
    environment.process(stations[rider.id_to_station].receive_bike(rider))


environment.run()
