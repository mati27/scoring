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

    def test_no_se_reporta_un_evento_cuando_en_el_recorrido_no_se_ingresa_a_una_zona_peligrosa(self):
        gps = self.un_gps_que_notifique_el_recorrido([(-34.551212, -58.463000), (-34.551882, -58.462591)])

        zona_peligrosa = ZonaGeografica.definida_por((-35.551212, -58.463000), (-35.551882, -58.462591))
        DetectorDeViajeAZonaPeligrosa.nuevo_con(gps=gps, zonas_peligrosas=[zona_peligrosa],
                                                estrategia_de_reporte_de_eventos=self)

        gps.activar()

        self.assertListEqual(self.eventos_registrados, [])

    def test_se_reporta_un_evento_cuando_el_recorrido_inicia_fuera_de_la_zona_peligrosa_e_ingresa(self):
        gps = self.un_gps_que_notifique_el_recorrido([(34, 57), (34, 59)])

        zona_peligrosa = ZonaGeografica.definida_por((34, 58), (38, 60))
        DetectorDeViajeAZonaPeligrosa.nuevo_con(gps=gps, zonas_peligrosas=[zona_peligrosa],
                                                estrategia_de_reporte_de_eventos=self)

        gps.activar()

        self.assertEquals(len(self.eventos_registrados), 1)
        self.assertEquals(self.eventos_registrados[0].zona(), zona_peligrosa)

    def test_no_se_vuelve_a_reportar_un_evento_si_el_recorrido_se_mantiene_en_la_zona_peligrosa(self):
        gps = self.un_gps_que_notifique_el_recorrido([(34, 57), (34, 59), (35, 59)])

        zona_peligrosa = ZonaGeografica.definida_por((34, 58), (38, 60))
        DetectorDeViajeAZonaPeligrosa.nuevo_con(gps=gps, zonas_peligrosas=[zona_peligrosa],
                                                estrategia_de_reporte_de_eventos=self)

        gps.activar()

        self.assertEquals(len(self.eventos_registrados), 1)
        self.assertEquals(self.eventos_registrados[0].zona(), zona_peligrosa)

    def test_se_reporta_un_unico_evento_si_el_recorrido_pasa_por_una_zona_peligrosa_y_sale(self):
        gps = self.un_gps_que_notifique_el_recorrido([(34, 57), (34, 59), (35, 59), (35, 61)])

        zona_peligrosa = ZonaGeografica.definida_por((34, 58), (38, 60))
        DetectorDeViajeAZonaPeligrosa.nuevo_con(gps=gps, zonas_peligrosas=[zona_peligrosa],
                                                estrategia_de_reporte_de_eventos=self)

        gps.activar()

        self.assertEquals(len(self.eventos_registrados), 1)
        self.assertEquals(self.eventos_registrados[0].zona(), zona_peligrosa)

    def test_se_reportan_dos_eventos_si_el_recorrido_pasa_por_una_zona_peligrosa_sale_y_vuelve_a_ingresar(self):
        gps = self.un_gps_que_notifique_el_recorrido([(34, 57), (34, 59), (35, 59), (35, 61), (36, 60)])

        zona_peligrosa = ZonaGeografica.definida_por((34, 58), (38, 60))
        DetectorDeViajeAZonaPeligrosa.nuevo_con(gps=gps, zonas_peligrosas=[zona_peligrosa],
                                                estrategia_de_reporte_de_eventos=self)

        gps.activar()

        self.assertEquals(len(self.eventos_registrados), 2)
        self.assertEquals(self.eventos_registrados[0].zona(), zona_peligrosa)
        self.assertEquals(self.eventos_registrados[1].zona(), zona_peligrosa)
