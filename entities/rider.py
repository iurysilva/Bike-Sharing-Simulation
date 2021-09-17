from datetime import datetime
from services import get_difference_in_minutes


class Rider:
    def __init__(self, environment, id, trip_start_time, trip_end_time):
        self.id = id
        self.environment = environment
        self.arrival_time = trip_start_time
        self.trip_start_time = trip_start_time
        self.trip_end_time = trip_end_time
        self.trip_duration = self.get_trip_duration()

    def get_trip_duration(self):
        return get_difference_in_minutes(self.trip_start_time, self.trip_end_time)
