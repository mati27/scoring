from geopy.distance import Distance
from asegurados.base import Asegurado
from cotizadores.cotizador_por_distancia_recorrida import CotizadorPorDistanciaRecorrida
from cotizadores.cotizador_por_frenada_brusca import CotizadorPorFrenadaBrusca
from cotizadores.cotizador_por_rango_exceso_velocidad import CotizadorPorRangoExcesoVelocidad
from cotizadores.cotizador_por_viaje_frecuente_a_zona_peligrosa import CotizadorPorViajeFrecuenteAZonaPeligrosa
from detectores.detector_de_exceso_de_velocidad import DetectorDeExcesoDeVelocidad
from detectores.detector_de_zona_peligrosa import DetectorDeViajeAZonaPeligrosa
from geolocalizacion.zona_geografica import ZonaGeografica

ZONAS_PELIGROSAS = [
    ZonaGeografica.definida_por((-34.551882, -58.462591), (-34.551882, -58.462591))
]

ASEGURADOS = [
    Asegurado.con(nombre='Carlos Perez')
]

CONFIGURACION_DE_DETECTORES = [
    {'tipo': DetectorDeViajeAZonaPeligrosa, 'parametros': {'zonas_peligrosas': ZONAS_PELIGROSAS}}
    #{'tipo': DetectorDeExcesoDeVelocidad, 'parametros': {'proveedor_velocidad_maxima': ZONAS_PELIGROSAS}}
]

CONFIGURACION_DE_COTIZADORES = [
    {'tipo': CotizadorPorFrenadaBrusca, 'parametros': {'penalizacion': 40}},
    {'tipo': CotizadorPorRangoExcesoVelocidad, 'parametros': {'penalizacion': 40, 'cota_inferior': 30, 'cota_superior': 40}},
    {'tipo': CotizadorPorRangoExcesoVelocidad, 'parametros': {'penalizacion': 80, 'cota_inferior': 31, 'cota_superior': float("inf")}},
    {'tipo': CotizadorPorViajeFrecuenteAZonaPeligrosa, 'parametros': {'penalizacion': 40, 'cantidad_viajes_para_penalizacion': 1}},
    {'tipo': CotizadorPorDistanciaRecorrida, 'parametros': {'penalizacion_por_unidad': 10, 'distancia_para_penalizacion': Distance(2000)}},
]