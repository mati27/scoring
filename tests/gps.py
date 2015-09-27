from unittest import TestCase
from geolocalizacion.gps import GPS
from geolocalizacion.satelite import SateliteMock, SimuladorDeRecorrido, RecorridoEnLista


class SateliteSpy(object):
    def __init__(self):
        self.ubicaciones_obtenidas_desde = []

    def obtener_ubicacion_de(self, gps):
        self.ubicaciones_obtenidas_desde.append(gps)

    def ubicacion_fue_obtenida_desde(self, gps):
        return gps in self.ubicaciones_obtenidas_desde


class GPSTestCase(TestCase):
    def setUp(self):
        self.ubicaciones_obtenidas = []

    def test_al_obtener_la_ubicacion_actual_el_GPS_obtiene_la_ubicacion_del_satelite(self):
        satelite = SateliteSpy()
        gps = self.un_gps(satelite=satelite)

        gps.obtener_ubicacion_actual()

        self.assertTrue(satelite.ubicacion_fue_obtenida_desde(gps))

    def un_gps(self, satelite):
        return GPS.nuevo(satelite=satelite)

    def test_al_activar_el_gps_los_que_estan_escuchando_reciben_las_coordenadas_obtenidas_del_satelite(self):
        estrategia_de_recorrido = RecorridoEnLista([(-34.551212, -58.463000), (-34.551882, -58.462591)])
        satelite = SateliteMock(simulador_de_recorrido=SimuladorDeRecorrido(estrategia=estrategia_de_recorrido))
        gps = self.un_gps(satelite=satelite)

        gps.agregar_observador(self)
        gps.activar()

        self.assertEquals(len(self.ubicaciones_obtenidas), 2)
        self.assertEquals(self.ubicaciones_obtenidas[0].latitud(), -34.551212)
        self.assertEquals(self.ubicaciones_obtenidas[0].longitud(), -58.463000)
        self.assertEquals(self.ubicaciones_obtenidas[1].latitud(), -34.551882)
        self.assertEquals(self.ubicaciones_obtenidas[1].longitud(), -58.462591)

    def ubicacion_obtenida(self, intervalo):
        self.ubicaciones_obtenidas.append(intervalo)
