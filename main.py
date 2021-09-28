import simpy
import pandas as pd
from services import create_graph
from services import dataset_services as dfs
from services import distribute_bikes_by_popularity
from services import create_stations
from services import create_processes
from services import distribute_bikes_equally

temperature = 24
humidity = 50
bikes_input = 100
function = distribute_bikes_equally  # distribute_bikes_by_popularity, distribute_bikes_equally

dataset_station = pd.read_csv('services/datasets/station_cleaned.csv')

dataset_weather = pd.read_csv('services/datasets/weather.csv')
dataset_weather['Date'] = pd.to_datetime(dataset_weather['Date']).dt.date

dataset_trip = pd.read_csv("services/datasets/trip_cleaned.csv", error_bad_lines=False)
dataset_trip['Date'] = pd.to_datetime(dataset_trip['starttime']).dt.date

date_df = dfs.in_df_to_date(dataset_weather, humidity, temperature)  # humidity and temperature
rides_df = pd.merge(dataset_trip, date_df.head(1), how='inner', on='Date')


# Create graph
# create_graph(rides_df)

# Prepare simulation
environment = simpy.Environment()
initial_time = rides_df['starttime'][0]


# Create stations
stations = create_stations(environment, initial_time, dataset_station)

# Verify number of bikes leaving and arriving each station
for station in stations:
    dataset = rides_df
    popularity_from = dfs.from_count(dataset, station) - dfs.to_count(dataset, station)
    popularity_to = dfs.from_count(dataset, station)
    popularity = (popularity_from + popularity_to)/2
    if popularity < 0:
        popularity = 0
    stations[station].popularity = popularity

# distribute bikes and docks
total_of_bikes = function(environment, stations, bikes_input)
# total_of_bikes = distribute_bikes_equally(environment, stations, bikes_input)

# Create and run simulation processes
bad_stations = dfs.return_bad_stations('services/datasets/station.csv')
create_processes(environment, rides_df, bad_stations, stations)
environment.run()

# Calculate total waiting time in queue
total_time_waited = 0
for station in stations:
    total_time_waited += stations[station].minutes_waited
print("Total time of queues: ", total_time_waited)
