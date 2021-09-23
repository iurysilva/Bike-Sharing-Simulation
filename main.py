import simpy
from datetime import datetime
from datetime import timedelta
from entities import Station
from entities import Rider
import pandas as pd


dataset = pd.read_csv("services/datasets/trip.csv", error_bad_lines=False)

environment = simpy.Environment()

initial_time = dataset['starttime'][0]
bikes_avaliable = 3
docks_avaliable = 3
bikes = simpy.Container(environment, capacity=bikes_avaliable, init=bikes_avaliable)
docks = simpy.Container(environment, capacity=docks_avaliable, init=0)
station = Station(environment, initial_time, bikes, docks)

for id in range(10):
    rider = Rider(environment, id, dataset['starttime'][id], dataset['stoptime'][id])
    environment.process(station.provide_bike(rider))


environment.run()
