from geopy.distance import Distance
from asegurados.base import Asegurado
from cotizadores.cotizador_por_distancia_recorrida import CotizadorPorDistanciaRecorrida
from cotizadores.cotizador_por_frenada_brusca import CotizadorPorFrenadaBrusca
from cotizadores.cotizador_por_rango_exceso_velocidad import CotizadorPorRangoExcesoVelocidad
from cotizadores.cotizador_por_viaje_frecuente_a_zona_peligrosa import CotizadorPorViajeFrecuenteAZonaPeligrosa
from detectores.detector_de_exceso_de_velocidad import DetectorDeExcesoDeVelocidad
from detectores.detector_de_frenada_brusca import DetectorDeFrenadaBrusca
from detectores.detector_de_viaje import DetectorDeViaje
from detectores.detector_de_zona_peligrosa import DetectorDeViajeAZonaPeligrosa
from fisica.aceleracion import Aceleracion
from fisica.velocidad import Velocidad
from geolocalizacion.proveedor_velocidad_maxima import ProveedorVelocidadMaxima
from geolocalizacion.zona_geografica import ZonaGeografica


ZONAS_PELIGROSAS = [

    ZonaGeografica.definida_por((34.551882, 58.465000), (34.551882, 58.465600)),
    ZonaGeografica.definida_por((34.551882, 58.463000), (34.551882, 58.463500))
]


zona_geografica = ZonaGeografica.definida_por((34.551000, 58.462000), (34.553882, 58.762591))
catalogo_de_velocidades_maximas = dict()
catalogo_de_velocidades_maximas[zona_geografica] =  Velocidad.nueva_con_km_por_h(magnitud = 145)

PROVEEDOR_DE_VELOCIDAD_MAXIMA =ProveedorVelocidadMaxima.nuevo(catalogo_de_velocidades_maximas=catalogo_de_velocidades_maximas)



ASEGURADOS = [
    Asegurado.con(nombre='Carlos Perez')
]

CONFIGURACION_DE_DETECTORES = [
    {'tipo': DetectorDeViajeAZonaPeligrosa, 'parametros': {'zonas_peligrosas': ZONAS_PELIGROSAS}},
    {'tipo': DetectorDeViaje, 'parametros': {}},
    {'tipo': DetectorDeExcesoDeVelocidad, 'parametros': {'proveedor_velocidad_maxima': PROVEEDOR_DE_VELOCIDAD_MAXIMA, 'porcentaje_de_velocidad_maxima': 10, 'distancia_excedido': Distance(0.1)}},
    {'tipo': DetectorDeFrenadaBrusca, 'parametros': {'limite_aceleracion': Aceleracion.desde_gs(-0.45)}}
]




CONFIGURACION_DE_COTIZADORES = [
    {'tipo': CotizadorPorFrenadaBrusca, 'parametros': {'penalizacion': 10}},
    {'tipo': CotizadorPorRangoExcesoVelocidad, 'parametros': {'penalizacion': 20, 'cota_inferior': 10, 'cota_superior': 19}},
    {'tipo': CotizadorPorRangoExcesoVelocidad, 'parametros': {'penalizacion': 60, 'cota_inferior': 20, 'cota_superior': float("inf")}},
    {'tipo': CotizadorPorViajeFrecuenteAZonaPeligrosa, 'parametros': {'penalizacion': 100, 'cantidad_viajes_para_penalizacion': 2}},
    {'tipo': CotizadorPorDistanciaRecorrida, 'parametros': {'penalizacion_por_unidad': 10, 'distancia_para_penalizacion': Distance(10)}},
]
