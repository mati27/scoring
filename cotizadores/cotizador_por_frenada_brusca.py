from cotizadores.base import CotizadorBase
from eventos.frenada_brusca import EventoDeFrenadaBrusca


class CotizadorPorFrenadaBrusca(CotizadorBase):
    def acepta_evento(self, evento):
        return evento.tipo == 'FrenadaBrusca'

    def obtener_cotizacion_evento(self, evento):
        if not self.acepta_evento(evento):
            raise RuntimeError('Este cotizador no acepta el evento', evento)
        return self._penalizacion

    def __init__(self, penalizacion):
        self._penalizacion = penalizacion

    @classmethod
    def con_penalizacion(cls, penalizacion):
        return cls(penalizacion)
