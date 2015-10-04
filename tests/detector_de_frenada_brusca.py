from unittest import TestCase
from datetime import timedelta
from detectores.detector_de_frenada_brusca import DetectorDeFrenadaBrusca
from fisica.aceleracion import Aceleracion
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
        return GPS.nuevo(satelite=satelite, actualizar_cada=timedelta(seconds=1))


    def test_frenada_brusca_larga_reporta_un_solo_evento(self):
        gps = self.un_gps_que_notifique_el_recorrido(
            [
                (-34.551882, -58.463000),
                (-34.551882, -58.464591),
                (-34.551882, -58.469591),
                (-34.551882, -58.471591),
                (-34.551882, -58.472591),
                (-34.551882, -58.478591),
             ]
        )

        DetectorDeFrenadaBrusca.nuevo_con(gps=gps, limite_aceleracion=Aceleracion.desde_gs(-0.45),
                                                estrategia_de_reporte_de_eventos=self)

        gps.activar()

        self.assertEquals(len(self.eventos_registrados), 1)

    def tipo(self):
        return 'FrenadaBrusca'