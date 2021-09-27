from datetime import timedelta
from datetime import datetime
from services import get_difference_in_minutes
from services import get_date_str


class Station:
    def __init__(self, id, environment, initial_time, bikes_avaliable, docks_avaliable):
        self.id = id
        self.initial_time = initial_time
        self.date_format_str = '%m/%d/%Y %H:%M'
        self.environment = environment
        self.bikes = bikes_avaliable
        self.docks = docks_avaliable
        self.minutes_waited = 0

    def get_environment_time(self):
        time = datetime.strptime(self.initial_time, self.date_format_str)
        time += timedelta(minutes=self.environment.now)
        return time.strftime(self.date_format_str)

    def provide_bike(self, rider, stations):
        yield self.environment.timeout(get_difference_in_minutes(self.initial_time, rider.arrival_time))
        print(rider.id, 'Chegou em',self.id, self.get_environment_time())
        rider_minutes_waited = 0
        print("Numero de docks: %s,  numero de bikes: %s\n" % (self.docks.level, self.bikes.level))
        with self.bikes.get(1) as bike:
            self.docks.put(1)
            yield bike
            self.minutes_waited += get_difference_in_minutes(rider.arrival_time, str(self.get_environment_time()))
            rider_minutes_waited += get_difference_in_minutes(rider.arrival_time, str(self.get_environment_time()))
            print(rider.id, 'Iniciou viagem em %s %s, duração: %d min' % (self.id, self.get_environment_time(),
                                                                          rider.trip_duration))
            print("tempo total esperado: ", rider_minutes_waited, '\n')
            yield self.environment.timeout(rider.trip_duration)
            end_time = str(self.get_environment_time())
            with stations[rider.id_to_station].docks.get(1) as dock:
                yield dock
                stations[rider.id_to_station].minutes_waited += get_difference_in_minutes(end_time, str(self.get_environment_time()))
                rider_minutes_waited += get_difference_in_minutes(end_time, str(self.get_environment_time()))
                print(rider.id, 'Terminou a viagem em', rider.id_to_station, self.get_environment_time())
                print("Tempo total esperado: ", rider_minutes_waited, '\n')
                stations[rider.id_to_station].bikes.put(1)
