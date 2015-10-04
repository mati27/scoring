from unittest import TestCase
from datetime import timedelta
from geopy.distance import great_circle
from detectores.detector_de_exceso_de_velocidad import DetectorDeExcesoDeVelocidad
from detectores.detector_de_viaje import DetectorDeViaje
from fisica.calculador_dinstancias_por_coordenadas import CalculadorDistanciasPorCoordenadas
from geolocalizacion.gps import GPS
from geolocalizacion.satelite import SateliteMock, SimuladorDeRecorrido, RecorridoEnLista
from geolocalizacion.zona_geografica import ZonaGeografica
from geolocalizacion.proveedor_velocidad_maxima import ProveedorVelocidadMaxima
from fisica.velocidad import Velocidad


class DetectorDeExcesoDeVelocidadTestCase(TestCase):
    def setUp(self):
        self.eventos_registrados = []

    def reportar_evento(self, evento):
        self.eventos_registrados.append(evento)

    def un_gps_que_notifique_el_recorrido(self, recorrido):
        estrategia_de_recorrido = RecorridoEnLista(recorrido)
        satelite = SateliteMock(simulador_de_recorrido=SimuladorDeRecorrido(estrategia=estrategia_de_recorrido))
        return GPS.nuevo(satelite=satelite, actualizar_cada=timedelta(seconds=1))


    def test_se_reporta_un_evento_de_viaje(self):

        recorrido =  [
                    (-34.551882, -58.463000),
                    (-34.551882, -58.463500),
                    (-34.551882, -58.464000),
                    (-34.551882, -58.464100),
                    (-34.551882, -58.464200),
                    (-34.551882, -58.464300),
                    (-34.551882, -58.464400),
                    (-34.551882, -58.464400),
                    ]

        gps = self.un_gps_que_notifique_el_recorrido(recorrido)

        DetectorDeViaje.nuevo_con(gps=gps,estrategia_de_reporte_de_eventos=self)

        gps.activar()

        self.assertEquals(len(self.eventos_registrados), 1)


    def test_se_reportan_dos_eventos_de_viaje(self):

        recorrido =  [
                    (-34.551882, -58.463000),
                    (-34.551882, -58.463500),
                    (-34.551882, -58.464000),
                    (-34.551882, -58.464100),
                    (-34.551882, -58.464200),
                    (-34.551882, -58.464300),
                    (-34.551882, -58.464400),
                    (-34.551882, -58.464400),
                    (-34.551882, -58.464500),
                    (-34.551882, -58.464600),
                    (-34.551882, -58.464700),
                    (-34.551882, -58.464800),
                    (-34.551882, -58.464800),
                    ]

        gps = self.un_gps_que_notifique_el_recorrido(recorrido)

        DetectorDeViaje.nuevo_con(gps=gps,estrategia_de_reporte_de_eventos=self)

        gps.activar()

        self.assertEquals(len(self.eventos_registrados), 2)


