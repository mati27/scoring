from geopy.distance import Distance
from cotizadores.base import CotizadorBase


class CotizadorPorDistanciaRecorrida(CotizadorBase):
    def acepta_evento(self, evento):
        return evento.tipo() == 'Viaje'

    def obtener_cotizacion_evento(self, evento):
        if not self.acepta_evento(evento):
            raise RuntimeError('Este cotizador no acepta el evento', evento)

        self.incrementar_distancia_acumulada(evento.distancia())

        return self.obtener_penalizacion()

    def incrementar_distancia_acumulada(self, distancia):
        self._distancia_acumulada += distancia

    def obtener_penalizacion(self):
        unidades_penalizables = int(self._distancia_acumulada / self._distancia_para_penalizacion)
        if unidades_penalizables > 0:
            distancia_penalizada = unidades_penalizables * self._distancia_para_penalizacion.kilometers
            resto = self._distancia_acumulada.kilometers - distancia_penalizada
            self._distancia_acumulada  = Distance (resto)
        return unidades_penalizables * self._penalizacion_por_unidad

    def __init__(self, penalizacion_por_unidad, distancia_para_penalizacion):
        self._penalizacion_por_unidad = penalizacion_por_unidad
        self._distancia_acumulada = Distance(0)
        self._distancia_para_penalizacion = distancia_para_penalizacion

    @classmethod
    def con_penalizacion_para_distancia(cls, penalizacion_por_unidad, distancia_para_penalizacion):
        return cls(penalizacion_por_unidad=penalizacion_por_unidad,distancia_para_penalizacion=distancia_para_penalizacion)
