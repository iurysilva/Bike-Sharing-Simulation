from datetime import datetime
from services import get_difference_in_minutes


class Rider:
    def __init__(self, environment, id, id_from_station, id_to_station, trip_start_time, trip_end_time):
        self.id = id
        self.environment = environment
        self.id_from_station = id_from_station
        self.id_to_station = id_to_station
        self.arrival_time = trip_start_time
        self.trip_start_time = trip_start_time
        self.trip_end_time = trip_end_time
        self.trip_duration = self.get_trip_duration()

    def get_trip_duration(self):
        return get_difference_in_minutes(self.trip_start_time, self.trip_end_time)
