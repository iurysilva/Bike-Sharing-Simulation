import simpy
from datetime import datetime
from datetime import timedelta
from entities import Station
from entities import Rider


environment = simpy.Environment()

initial_time = '10/13/2014 10:31'
bikes_avaliable = 3
docks_avaliable = 3
bikes = simpy.Container(environment, capacity=bikes_avaliable, init=bikes_avaliable)
docks = simpy.Container(environment, capacity=docks_avaliable, init=0)
station = Station(environment, initial_time, bikes, docks)

r1 = Rider(environment, 0, '10/13/2014 10:31', '10/13/2014 10:48')
r2 = Rider(environment, 1, '10/13/2014 10:31', '10/13/2014 10:48')


environment.process(station.provide_bike(r1))

environment.run()
