from eventos.base import Evento


class EventoDeViaje(Evento):
    @classmethod
    def nuevo(cls, distancia):
        return cls(distancia=distancia)

    def __init__(self, distancia):
        self._distancia = distancia

        super(EventoDeViaje, self).__init__()

    def distancia(self):
        return self._distancia

    def tipo(self):
        return 'Viaje'