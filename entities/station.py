from datetime import timedelta
from datetime import datetime
from services import get_difference_in_minutes


class Station:
    def __init__(self, id, environment, initial_time, bikes_avaliable, docks_avaliable):
        self.id = id
        self.initial_time = initial_time
        self.date_format_str = '%m/%d/%Y %H:%M'
        self.environment = environment
        self.bikes = bikes_avaliable
        self.docks = docks_avaliable

    def get_environment_time(self):
        time = datetime.strptime(self.initial_time, self.date_format_str) + timedelta(minutes=self.environment.now)
        return time

    def provide_bike(self, rider, stations):
        yield self.environment.timeout(get_difference_in_minutes(self.initial_time, rider.arrival_time))
        print(rider.id, 'Chegou em',self.id, self.get_environment_time())
        print("Numero de docks: %s,  numero de bikes: %s" % (self.docks.level, self.bikes.level))
        with self.bikes.get(1) as bike:
            self.docks.put(1)
            yield bike
            print(rider.id, 'Iniciou viagem em %s, duração: %d' % (self.get_environment_time(), rider.trip_duration))
            yield self.environment.timeout(rider.trip_duration)
            with stations[rider.id_to_station].docks.get(1) as dock:
                yield dock
                print(rider.id, 'Terminou a viagem em', rider.id_to_station, self.get_environment_time())
                stations[rider.id_to_station].bikes.put(1)

