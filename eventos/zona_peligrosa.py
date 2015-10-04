from eventos.base import Evento


class EventoDeViajeAZonaPeligrosa(Evento):
    @classmethod
    def nuevo(cls, zona):
        return cls(zona=zona)

    def __init__(self, zona):
        self._zona = zona

        super(EventoDeViajeAZonaPeligrosa, self).__init__()

    def zona(self):
        return self._zona

    def tipo(self):
        return 'ViajeZonaPeligrosa'