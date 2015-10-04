from unittest import TestCase
from datetime import timedelta
from detectores.detector_de_exceso_de_velocidad import DetectorDeExcesoDeVelocidad
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


    def test_no_se_reportan_eventos_cuando_no_se_excede_la_velocidad_maxima(self):

        recorrido =  [
                    (-34.551882, -58.463000),
                    (-34.551882, -58.463500),
                    (-34.551882, -58.464000),
                    (-34.551882, -58.464100),
                    (-34.551882, -58.464200),
                    (-34.551882, -58.464300),
                    (-34.551882, -58.464400),
                    ]

        gps = self.un_gps_que_notifique_el_recorrido(recorrido)


        zona_geografica = ZonaGeografica.definida_por((-34.551000, -58.462000), (-34.553882, -58.762591))
        catalogo_de_velocidades_maximas = dict()

        catalogo_de_velocidades_maximas[zona_geografica] = Velocidad(40)
        proveedor_velocidad_maxima = ProveedorVelocidadMaxima.nuevo(catalogo_de_velocidades_maximas=catalogo_de_velocidades_maximas)


        DetectorDeExcesoDeVelocidad.nuevo_con(gps=gps,proveedor_velocidad_maxima=proveedor_velocidad_maxima ,
                                                estrategia_de_reporte_de_eventos=self, porcentaje_de_velocidad_maxima= 10, distancia_excedido=100)

        gps.activar()

        self.assertEquals(len(self.eventos_registrados), 0)


    def test_no_se_reportan_eventos_cuando_se_excede_la_velocidad_menos_de_100_metros(self):
       recorrido =  [
                    (-34.551882, -58.463000),
                    (-34.551882, -58.463500),
                    (-34.551882, -58.464000),
                    (-34.551882, -58.464100),
                    (-34.551882, -58.464200),
                    (-34.551882, -58.464300),
                    (-34.551882, -58.464400),
                    ]

       gps = self.un_gps_que_notifique_el_recorrido(recorrido)
       zona_geografica = ZonaGeografica.definida_por((-34.551000, -58.462000), (-34.553882, -58.762591))
       catalogo_de_velocidades_maximas = dict()


       catalogo_de_velocidades_maximas[zona_geografica] = Velocidad(26)
       proveedor_velocidad_maxima = ProveedorVelocidadMaxima.nuevo(catalogo_de_velocidades_maximas=catalogo_de_velocidades_maximas)

       DetectorDeExcesoDeVelocidad.nuevo_con(gps=gps,proveedor_velocidad_maxima=proveedor_velocidad_maxima ,
                                                estrategia_de_reporte_de_eventos=self, porcentaje_de_velocidad_maxima= 10, distancia_excedido=100)

       gps.activar()
       self.assertEquals(len(self.eventos_registrados), 0)



    def test_se_reportan_dos_eventos_cuando_el_recorrido_se_excede_en_velocidad_mas_de_200_metros(self):



        recorrido =  [
                    (-34.551882, -58.463000),
                    (-34.551882, -58.463500),
                    (-34.551882, -58.464000),
                    (-34.551882, -58.464500),
                    (-34.551882, -58.465000),
                    (-34.551882, -58.465500),
                    (-34.551882, -58.466000),
                    (-34.551882, -58.466500),
                    ]

        gps = self.un_gps_que_notifique_el_recorrido(recorrido)

        zona_geografica = ZonaGeografica.definida_por((-34.551000, -58.462000), (-34.553882, -58.762591))
        catalogo_de_velocidades_maximas = dict()

        catalogo_de_velocidades_maximas[zona_geografica] = Velocidad(26)
        proveedor_velocidad_maxima = ProveedorVelocidadMaxima.nuevo(catalogo_de_velocidades_maximas=catalogo_de_velocidades_maximas)


        DetectorDeExcesoDeVelocidad.nuevo_con(gps=gps,proveedor_velocidad_maxima=proveedor_velocidad_maxima ,
                                                estrategia_de_reporte_de_eventos=self, porcentaje_de_velocidad_maxima= 10, distancia_excedido=100)

        gps.activar()

        self.assertEquals(len(self.eventos_registrados), 3)



    def test_no_se_encuentra_velocidad_maxima_para_alguna_coordenada(self):
        try:
            recorrido =  [
                        (-34.551882, -58.463000),
                        (-34.551882, -58.463500),
                        (-34.551882, -58.464000),
                        (-34.551882, -58.464100),
                        (-34.551882, -58.464200),
                        (-34.551882, -58.464300),
                        (-34.551882, -58.464400),
                        ]

            gps = self.un_gps_que_notifique_el_recorrido(recorrido)
            zona_geografica = ZonaGeografica.definida_por((-34.551000, -58.464000), (-34.553882, -58.762591))
            catalogo_de_velocidades_maximas = dict()


            catalogo_de_velocidades_maximas[zona_geografica] = Velocidad(26)
            proveedor_velocidad_maxima = ProveedorVelocidadMaxima.nuevo(catalogo_de_velocidades_maximas=catalogo_de_velocidades_maximas)

            DetectorDeExcesoDeVelocidad.nuevo_con(gps=gps,proveedor_velocidad_maxima=proveedor_velocidad_maxima ,
                                                    estrategia_de_reporte_de_eventos=self, porcentaje_de_velocidad_maxima= 10, distancia_excedido=100)

            gps.activar()
            self.assertEquals(len(self.eventos_registrados), 0)

        except RuntimeError, e:
            print e

