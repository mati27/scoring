from unittest import TestCase
from geolocalizacion.satelite import SimuladorDeRecorrido, RecorridoEnArchivo, RecorridoEnLista


class SimuladorDeRecorridoTestCase(TestCase):
    def test_simular_recorrido_usando_estrategia_de_recorrido_en_archivo(self):
        archivo_de_recorrido = 'recorrido_de_prueba'

        simulador = SimuladorDeRecorrido.simular_usando(estrategia=RecorridoEnArchivo.usando(archivo_de_recorrido))

        coordenadas_primer_punto = simulador.siguiente_punto_del_recorrido()
        coordenadas_segundo_punto = simulador.siguiente_punto_del_recorrido()

        self.assertEquals(coordenadas_primer_punto[0], -34.551212)
        self.assertEquals(coordenadas_primer_punto[1], -58.463000)
        self.assertEquals(coordenadas_segundo_punto[0], -34.551882)
        self.assertEquals(coordenadas_segundo_punto[1], -58.462591)
        self.assertTrue(simulador.termino_el_recorrido())

    def test_simular_recorrido_usando_estrategia_de_recorrido_en_lista(self):
        lista_de_recorrido = [(-34.551212, -58.463000), (-34.551882, -58.462591)]
        simulador = SimuladorDeRecorrido.simular_usando(estrategia=RecorridoEnLista.usando(lista_de_recorrido))

        coordenadas_primer_punto = simulador.siguiente_punto_del_recorrido()
        coordenadas_segundo_punto = simulador.siguiente_punto_del_recorrido()

        self.assertEquals(coordenadas_primer_punto[0], -34.551212)
        self.assertEquals(coordenadas_primer_punto[1], -58.463000)
        self.assertEquals(coordenadas_segundo_punto[0], -34.551882)
        self.assertEquals(coordenadas_segundo_punto[1], -58.462591)
        self.assertTrue(simulador.termino_el_recorrido())
