from cotizadores.base import CotizadorBase


class CotizadorPorRangoExcesoVelocidad(CotizadorBase):
    def acepta_evento(self, evento):
        return evento.tipo() == 'ExcesoDeVelocidad' and (
            self._cota_exceso_velocidad_inferior <= evento.porcentaje_excedido() <= self._cota_exceso_velocidad_superior)

    def obtener_cotizacion_evento(self, evento):
        if not self.acepta_evento(evento):
            raise RuntimeError('Este cotizador no acepta el evento', evento)
        return self._penalizacion

    def __init__(self, cota_inferior, cota_superior, penalizacion):
        self._cota_exceso_velocidad_inferior = cota_inferior
        self._cota_exceso_velocidad_superior = cota_superior
        self._penalizacion = penalizacion

    @classmethod
    def con_rango_y_penalizacion(cls, cota_inferior, cota_superior, penalizacion):
        return cls(cota_inferior, cota_superior, penalizacion)