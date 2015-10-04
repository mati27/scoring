from asegurados.base import Asegurado
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
]
