from eventos.base import Evento


class EventoDeExcesoDeVelocidad(Evento):
    @classmethod
    def nuevo(cls, porcentaje_de_velocidad, velocidad_excedido):
        return cls(porcentaje_de_velocidad=porcentaje_de_velocidad, velocidad_excedido=velocidad_excedido)

    def __init__(self, porcentaje_de_velocidad, velocidad_excedido):
        self._porcentaje_de_velocidad = porcentaje_de_velocidad
        self._velocidad_excedido = velocidad_excedido

        super(EventoDeExcesoDeVelocidad, self).__init__()

    def porcentaje_de_velocidad(self):
        return self._porcentaje_de_velocidad

    def velocidad_excedido(self):
        return self._velocidad_excedido

    def tipo(self):
        return 'ExcesoDeVelocidad'