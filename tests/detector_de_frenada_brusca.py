from unittest import TestCase
from datetime import timedelta
from detectores.detector_de_frenada_brusca import DetectorDeFrenadaBrusca
from geolocalizacion.gps import GPS
from geolocalizacion.satelite import SateliteMock, SimuladorDeRecorrido, RecorridoEnLista

class DetectorDeFrenadaBruscaTestCase(TestCase):
    def setUp(self):
        self.eventos_registrados = []

    def reportar_evento(self, evento):
        self.eventos_registrados.append(evento)

    def un_gps_que_notifique_el_recorrido(self, recorrido):
        estrategia_de_recorrido = RecorridoEnLista(recorrido)
        satelite = SateliteMock(simulador_de_recorrido=SimuladorDeRecorrido(estrategia=estrategia_de_recorrido))
        return GPS.nuevo(satelite=satelite, actualizar_cada=timedelta(microseconds=1))
