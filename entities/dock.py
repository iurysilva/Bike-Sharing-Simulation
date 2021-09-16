class Dock:
    def __init__(self, environment, bikes_avaliable):
        self.environment = environment
        self.bikes_avaliable = bikes_avaliable

    def provide_bike(self, rider):
        yield self.environment.timeout(rider.arrival_time)
        print(carro.nome, 'chegou em', self.env.now)
        with self.bombas.request() as bomba:
            yield bomba
            print(carro.nome, 'iniciou abastecimento em', self.env.now)
            yield self.env.timeout(carro.tempo_abastecimento)
            print(carro.nome, 'saiu do abastecimento em', self.env.now)