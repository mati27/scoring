from cotizadores.base import CotizadorBase


class CotizadorPorViajeFrecuenteAZonaPeligrosa(CotizadorBase):
    def acepta_evento(self, evento):
        return evento.tipo() == 'ViajeZonaPeligrosa'

    def obtener_cotizacion_evento(self, evento):
        if not self.acepta_evento(evento):
            raise RuntimeError('Este cotizador no acepta el evento', evento)

        self._cuenta_viajes += 1

        if self._cantidad_viajes_para_penalizacion == self._cuenta_viajes:
            self._cuenta_viajes = 0
            return self._penalizacion
        else:
            return 0

    def __init__(self, penalizacion, cantidad_viajes_para_penalizacion):
        self._penalizacion = penalizacion
        self._cuenta_viajes = 0
        self._cantidad_viajes_para_penalizacion = cantidad_viajes_para_penalizacion

    @classmethod
    def con_penalizacion_para_cantidad_viajes(cls, penalizacion, cantidad_viajes_para_penalizacion):
        return cls(penalizacion=penalizacion,cantidad_viajes_para_penalizacion=cantidad_viajes_para_penalizacion)
