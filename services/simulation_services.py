import simpy
from services import get_amount_of_resources
from entities import Station
from entities import Rider


def distribute_bikes_by_popularity(environment, stations, bikes_avaliable):
    total_of_bikes = 0
    bikes_remaining = 0
    for station in stations:
        if stations[station].max_bikes_number != 0:
            max_bikes_number = stations[station].max_bikes_number
            bikes_number = get_amount_of_resources(bikes_avaliable, stations, stations[station].popularity)
            total_of_bikes += bikes_number
            if bikes_number > max_bikes_number:
                bikes_amount = max_bikes_number
                bikes_remaining += bikes_number - max_bikes_number
            elif bikes_number + bikes_remaining <= max_bikes_number:
                bikes_amount = bikes_number + bikes_remaining
                bikes_remaining = 0
            else:
                bikes_amount = bikes_number
            bikes = simpy.Container(environment, capacity=max_bikes_number, init=bikes_amount)
            stations[station].bikes = bikes
            bikes_level = stations[station].bikes.level
            stations[station].docks = simpy.Container(environment, capacity=max_bikes_number,
                                                      init=max_bikes_number - bikes_level)
    return total_of_bikes


def distribute_bikes_equally(environment, stations, bikes_avaliable):
    total_of_bikes = 0
    for station in stations:
        if stations[station].max_bikes_number != 0:
            max_bikes_number = stations[station].max_bikes_number
            bikes_number = round(bikes_avaliable/len(stations))
            total_of_bikes += bikes_number
            bikes = simpy.Container(environment, capacity=max_bikes_number, init=bikes_number)
            stations[station].bikes = bikes
            bikes_level = stations[station].bikes.level
            stations[station].docks = simpy.Container(environment, capacity=max_bikes_number,
                                                      init=max_bikes_number - bikes_level)
    return total_of_bikes


def create_stations(environment, initial_time, dataset_station):
    stations = {}
    for row in range(len(dataset_station)):
        id = dataset_station.loc[row, 'station_id']
        docks_number = dataset_station.loc[row, 'current_dockcount']
        station = Station(id, environment, initial_time, None, None, docks_number)
        stations[id] = station
    return stations


def create_processes(environment, rides_df, bad_stations, stations):
    for row in range(len(rides_df)):
        from_station_id = rides_df['from_station_id'][row]
        to_station_id = rides_df['to_station_id'][row]
        if from_station_id not in bad_stations and to_station_id not in bad_stations:
            start_time = rides_df['starttime'][row]
            end_time = rides_df['stoptime'][row]
            rider = Rider(environment, row, from_station_id, to_station_id, start_time, end_time)
            environment.process(stations[rider.id_from_station].provide_bike(rider, stations))


