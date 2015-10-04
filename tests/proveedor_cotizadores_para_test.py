from unicodedata import decimal
from cotizadores.cotizador_kilometraje import CotizadorKilometrajePorPenalizacionFija
from cotizadores.cotizador_por_frenada_brusca import CotizadorPorFrenadaBrusca
from cotizadores.cotizador_por_rango_exceso_velocidad import CotizadorPorRangoExcesoVelocidad
from cotizadores.cotizador_por_viaje_frecuente_a_zona_peligrosa import CotizadorPorViajeFrecuenteAZonaPeligrosa
from scoreador.proveedor_cotizadores import ProveedorCotizadores
from geopy import distance


class ProveedorCotizadoresParaTest(ProveedorCotizadores):
    def obtener_cotizadores_eventos(self):
        ret = [
            CotizadorPorFrenadaBrusca.con_penalizacion(40),
            CotizadorPorRangoExcesoVelocidad.con_rango_y_penalizacion(20, 30, 40),
            CotizadorPorRangoExcesoVelocidad.con_rango_y_penalizacion(41, float("inf"), 40),
            CotizadorPorViajeFrecuenteAZonaPeligrosa.con_penalizacion_para_cantidad_viajes(40, 100)
        ]
        return ret

    #Nota: El MCI de Distance de geopy se construye pasandole km
    def obtener_cotizador_kilometraje(self):
        return CotizadorKilometrajePorPenalizacionFija.con_puntos_para_distancia(distance.Distance(1), 10)


