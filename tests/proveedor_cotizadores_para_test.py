from unicodedata import decimal
from geopy.distance import Distance
from cotizadores.cotizador_por_distancia_recorrida import CotizadorPorDistanciaRecorrida
from cotizadores.cotizador_por_frenada_brusca import CotizadorPorFrenadaBrusca
from cotizadores.cotizador_por_rango_exceso_velocidad import CotizadorPorRangoExcesoVelocidad
from cotizadores.cotizador_por_viaje_frecuente_a_zona_peligrosa import CotizadorPorViajeFrecuenteAZonaPeligrosa
from scoreador.proveedor_cotizadores import ProveedorCotizadoresEventos



class ProveedorCotizadoresParaTest(ProveedorCotizadoresEventos):
    def obtener_cotizadores_eventos(self):
        ret = [
            CotizadorPorFrenadaBrusca.con_penalizacion(40),
            CotizadorPorRangoExcesoVelocidad.con_rango_y_penalizacion(20, 30, 40),
            CotizadorPorRangoExcesoVelocidad.con_rango_y_penalizacion(31, float("inf"), 80),
            CotizadorPorViajeFrecuenteAZonaPeligrosa.con_penalizacion_para_cantidad_viajes(40, 2),
            CotizadorPorDistanciaRecorrida.con_penalizacion_para_distancia(10, Distance(2000))
        ]
        return ret



