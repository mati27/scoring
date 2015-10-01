from eventos.base import Evento


class EventoDeFrenadaBrusca(Evento):
    @classmethod
    def nuevo(cls):
        return cls()

    def __init__(self):
        super(EventoDeFrenadaBrusca, self).__init__()