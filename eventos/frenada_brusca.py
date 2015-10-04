from eventos.base import Evento


class EventoDeFrenadaBrusca(Evento):
    @classmethod
    def nuevo(cls):
        return cls()

    def __init__(self):
        super(EventoDeFrenadaBrusca, self).__init__()

    def tipo(self):
        return 'FrenadaBrusca'