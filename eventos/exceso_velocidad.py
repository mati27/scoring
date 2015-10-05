from eventos.base import Evento


class EventoDeExcesoDeVelocidad(Evento):
    @classmethod
    def nuevo(cls, porcentaje_de_velocidad, porcentaje_excedido):
        return cls(porcentaje_de_velocidad=porcentaje_de_velocidad, porcentaje_excedido=porcentaje_excedido)

    def __init__(self, porcentaje_de_velocidad, porcentaje_excedido):
        self._porcentaje_de_velocidad = porcentaje_de_velocidad
        self._porcentaje_excedido = porcentaje_excedido

        super(EventoDeExcesoDeVelocidad, self).__init__()

    def porcentaje_de_velocidad(self):
        return self._porcentaje_de_velocidad

    def porcentaje_excedido(self):
        return self._porcentaje_excedido

    def tipo(self):
        return 'ExcesoDeVelocidad'