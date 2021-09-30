import simpy
import pandas as pd
from services import create_graph
from services import dataset_services as dfs
from services import distribute_bikes_by_popularity
from services import create_stations
from services import create_processes
from services import distribute_bikes_equally
from services import distribute_bikes_and_docks_equally

temperature = 66
humidity = 64
bikes_input = 500
docks_input = 1500  # used only in distribution of bikes and docks equally
# distribute_bikes_by_popularity, distribute_bikes_equally, distribute_bikes_and_docks_equally
function = distribute_bikes_and_docks_equally
dia = 1

dataset_station = pd.read_csv('services/datasets/station_cleaned.csv')

dataset_weather = pd.read_csv('services/datasets/weather.csv')
dataset_weather['Date'] = pd.to_datetime(dataset_weather['Date']).dt.date

dataset_trip = pd.read_csv("services/datasets/trip_cleaned.csv")
dataset_trip['Date'] = pd.to_datetime(dataset_trip['starttime']).dt.date

date_df = dfs.in_df_to_date(dataset_weather, humidity, temperature)  # humidity and temperature
rides_df = pd.merge(dataset_trip, date_df.head(dia), how='inner', on='Date')


# Create graph
create_graph(rides_df)

# Prepare simulation
environment = simpy.Environment()
initial_time = rides_df['starttime'][0]


# Create stations
stations = create_stations(environment, initial_time, dataset_station)


# Verify number of bikes leaving and arriving each station
for station in stations:
    dataset = dataset_trip
    popularity_from = dfs.from_count(dataset, station)
    popularity_to = dfs.to_count(dataset, station)
    popularity = popularity_from + popularity_to
    stations[station].popularity = popularity


# distribute bikes and docks
total_of_bikes = function(environment, stations, bikes_input, docks_input)
# total_of_bikes = distribute_bikes_equally(environment, stations, bikes_input)

# Create and run simulation processes
bad_stations = dfs.return_bad_stations('services/datasets/station.csv')
create_processes(environment, rides_df, bad_stations, stations)
environment.run()

# Calculate total waiting time in queue
start_time_waited = 0
end_time_waited = 0
for station in stations:
    start_time_waited += stations[station].start_queue_time
    end_time_waited += stations[station].end_queue_time

print("Total time of queues to get bike: ", start_time_waited)
print("Total time of queues to put bike: ", end_time_waited)
print("Total time of queues: ", start_time_waited + end_time_waited)
print("Number of trips: ", len(rides_df))

