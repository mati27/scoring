from unittest import TestCase
from datetime import timedelta
from detectores.detector_de_zona_peligrosa import DetectorDeViajeAZonaPeligrosa
from geolocalizacion.gps import GPS
from geolocalizacion.satelite import SateliteMock, SimuladorDeRecorrido, RecorridoEnLista
from geolocalizacion.zona_geografica import ZonaGeografica


class DetectorDeZonaPeligrosaTestCase(TestCase):
    def setUp(self):
        self.eventos_registrados = []

    def reportar_evento(self, evento):
        self.eventos_registrados.append(evento)

    def un_gps_que_notifique_el_recorrido(self, recorrido):
        estrategia_de_recorrido = RecorridoEnLista(recorrido)
        satelite = SateliteMock(simulador_de_recorrido=SimuladorDeRecorrido(estrategia=estrategia_de_recorrido))
        return GPS.nuevo(satelite=satelite, actualizar_cada=timedelta(microseconds=1))


    def test_se_reportan_dos_eventos_por_ingresar_a_dos_zonas_peligrosas_distintas(self):
        gps = self.un_gps_que_notifique_el_recorrido([(34, 57), (34, 59), (34,62), (34,64)])

        zona_peligrosa = ZonaGeografica.definida_por((34, 58), (38, 60))
        zona_peligrosa1 = ZonaGeografica.definida_por((34, 63), (38, 64))
        DetectorDeViajeAZonaPeligrosa.nuevo_con(gps=gps, zonas_peligrosas=[zona_peligrosa, zona_peligrosa1],
                                                estrategia_de_reporte_de_eventos=self)

        gps.activar()

        self.assertEquals(len(self.eventos_registrados), 2)
        self.assertEquals(self.eventos_registrados[0].zona(), zona_peligrosa)
        self.assertEquals(self.eventos_registrados[1].zona(), zona_peligrosa1)



    def tipo(self):
        return 'ZonaPeligrosa'


