import simpy
from entities import Station
from entities import Rider
import pandas as pd
from services import create_graph
from services import dataset_services as dfs
from services import get_amount_of_resources

dataset_station = pd.read_csv('services/datasets/station.csv')

dataset_weather = pd.read_csv('services/datasets/weather.csv')
dataset_weather['Date'] = pd.to_datetime(dataset_weather['Date']).dt.date

dataset_trip = pd.read_csv("services/datasets/trip_cleaned.csv", error_bad_lines=False)
dataset_trip['Date'] = pd.to_datetime(dataset_trip['starttime']).dt.date

date_df = dfs.in_df_to_date(dataset_weather, 20, 97)  # humidity and temperature
rides_df = pd.merge(dataset_trip, date_df, how='inner', on='Date')

# Create graph
# create_graph(rides_df)

# Prepare simulation
environment = simpy.Environment()
initial_time = rides_df['starttime'][0]
bikes_avaliable = 200
docks_avaliable = 300
bikes = simpy.Container(environment, capacity=bikes_avaliable, init=bikes_avaliable)
docks = simpy.Container(environment, capacity=docks_avaliable, init=docks_avaliable - bikes_avaliable)

# Create stations
stations = {}
for row in range(len(dataset_station)):
    id = dataset_station.loc[row, 'station_id']
    docks_number = dataset_station.loc[row, 'current_dockcount']
    station = Station(id, environment, initial_time, None, None, docks_number)
    stations[id] = station

# Verify number of bikes leaving each station
for station in stations:
    stations[station].from_station_number = dfs.from_count(dataset_trip, station)

# distribute bikes and docks
total_of_bikes = 0
bikes_remaining = 0
for station in stations:
    if stations[station].max_bikes_number != 0:
        max_bikes_number = stations[station].max_bikes_number
        bikes_number = get_amount_of_resources(500, stations, stations[station].from_station_number)
        total_of_bikes += bikes_number
        if bikes_number > max_bikes_number:
            bikes = simpy.Container(environment, capacity=max_bikes_number, init=max_bikes_number)
            bikes_remaining += max_bikes_number - bikes_number
        elif bikes_number + bikes_remaining <= max_bikes_number:
            bikes = simpy.Container(environment, capacity=max_bikes_number, init=bikes_number + bikes_remaining)
            bikes_remaining = 0
        elif bikes_number <= max_bikes_number:
            bikes = simpy.Container(environment, capacity=max_bikes_number, init=bikes_number)
        stations[station].bikes = bikes
        bikes_level = stations[station].bikes.level
        stations[station].docks = simpy.Container(environment, capacity=max_bikes_number, init=max_bikes_number - bikes_level)


# Create and run simulation processes
for row in range(len(rides_df)):
    rider = Rider(environment, row, rides_df['from_station_id'][row], rides_df['to_station_id'][row], rides_df['starttime'][row], rides_df['stoptime'][row])
    environment.process(stations[rider.id_from_station].provide_bike(rider, stations))
environment.run()

# Calculate total waiting time in queue
total_time_waited = 0
for station in stations:
    total_time_waited += stations[station].minutes_waited
print("Total time of queues: ", total_time_waited)
