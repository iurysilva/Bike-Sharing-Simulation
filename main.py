import simpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from services import dataset_services as dss

from services import create_graph
from services import distribute_bikes_equally
from services import distribute_bikes_by_popularity
from services import create_stations
from services import create_processes
from services import distribute_bikes_and_docks_equally

from datetime import datetime

bikes_increase_rate = 15
docks_increase_rate = 1
bikes_input = 60
docks_input = 100  # used only in distribution of bikes and docks equally
# distribute_bikes_by_popularity, distribute_bikes_equally, distribute_bikes_and_docks_equally
function = distribute_bikes_and_docks_equally

dataset_station = pd.read_csv('services/datasets/station_cleaned.csv')

dataset_weather = pd.read_csv('services/datasets/weather.csv')
dataset_weather['Date'] = pd.to_datetime(dataset_weather['Date']).dt.date

dataset_trip = pd.read_csv("services/datasets/trip_cleaned.csv")
dataset_trip['Date'] = pd.to_datetime(dataset_trip['starttime']).dt.date

mean_times_get = {}
mean_times_put = {}
total_times = []
months = dss.mean_temp_by_month(pd.read_csv('services/datasets/weather.csv'))
bikes_input_month = []
docks_input_month = []
for date in months:
    temperatura = months[date]
    min_temperature = 43.25806451612903

    if temperatura > min_temperature:
        value = round(((temperatura - min_temperature) / 2) * bikes_increase_rate)
        if bikes_input + value < docks_input:
            bikes_input += value

    if temperatura > min_temperature:
        value = round(((temperatura - min_temperature) / 2) * docks_increase_rate)
        docks_input += value

    month = datetime.strptime(date, "%m/%Y").month
    year = datetime.strptime(date, "%m/%Y").year
    rides_df = dss.month_to_date(dataset_trip, month, year)
    rides_df = rides_df.reset_index()

    # Prepare simulation
    environment = simpy.Environment()
    #print(rides_df)
    initial_time = rides_df['starttime'][0]


    # Create stations
    stations = create_stations(environment, initial_time, dataset_station)


    # Verify number of bikes leaving and arriving each station
    for station in stations:
        dataset = dataset_trip
        popularity_from = dss.from_count(dataset, station)
        popularity_to = dss.to_count(dataset, station)
        popularity = popularity_from + popularity_to
        stations[station].popularity = popularity


    # distribute bikes and docks
    total_of_bikes = function(environment, stations, bikes_input, docks_input)
    # total_of_bikes = distribute_bikes_equally(environment, stations, bikes_input)

    # Create and run simulation processes
    bad_stations = dss.return_bad_stations('services/datasets/station.csv')
    create_processes(environment, rides_df, bad_stations, stations)
    environment.run()

    # Calculate total waiting time in queue
    start_time_waited = 0
    end_time_waited = 0
    for station in stations:
        start_time_waited += stations[station].start_queue_time
        end_time_waited += stations[station].end_queue_time

    bikes_input_month.append(bikes_input)
    docks_input_month.append(docks_input)
    print("Total time of queues to get bike in this month: ", start_time_waited)
    print("Total time of queues to put bike in this month: ", end_time_waited)
    print("Total time of queues in this month: ", start_time_waited + end_time_waited)
    print("Number of trips in this month: ", len(rides_df))
    for station in stations:
        if station not in mean_times_get and station not in mean_times_put:
            mean_times_get[station] = []
            mean_times_put[station] = []
        mean_times_get[station].append(stations[station].start_queue_time/dss.day_count(rides_df))
        mean_times_put[station].append(stations[station].end_queue_time/dss.day_count(rides_df))

print("Bike amount by month: ", bikes_input_month)
print("Dock amount by month: ", docks_input_month)


plt.style.use("seaborn-dark")
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
ax1.set_title("Mean queue time by month to get bike from station")
ax2.set_title("Mean queue time by month to return bike")
for station in mean_times_get:
    ax1.plot(list(months), mean_times_get[station], label=station)
ax1.set_xticks(np.arange(0, len(months), step=2))
ax1.legend()


for station in mean_times_put:
    ax2.plot(list(months), mean_times_put[station], label=station)
ax2.set_xticks(np.arange(0, len(months), step=2))
ax2.legend()

