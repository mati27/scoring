from unittest import TestCase
from geolocalizacion.zona_geografica import ZonaGeografica


class ZonaGeograficaTestCase(TestCase):
    def test_un_punto_de_coordenadas_dentro_del_rectangulo_definido_por_la_zona_debe_estar_dentro_de_la_misma(self):
        zona = ZonaGeografica.definida_por((-34.550921, -58.456218), (-34.559983, -58.461696))

        self.assertTrue(zona.esta_dentro((-34.551102, -58.459541)))

    def test_un_punto_de_coordenadas_fuera_del_rectangulo_definido_por_la_zona_debe_estar_fuera_de_la_misma(self):
        zona = ZonaGeografica.definida_por((-34.550921, -58.456218), (-34.559983, -58.461696))

        self.assertFalse(zona.esta_dentro((-34.541102, -58.459541)))

    def test_un_punto_de_coordenadas_en_el_borde_del_rectangulo_definido_por_la_zona_debe_estar_dentro_de_la_misma(self):
        zona = ZonaGeografica.definida_por((-34.550921, -58.456218), (-34.559983, -58.461696))

        self.assertTrue(zona.esta_dentro((-34.550921, -58.459541)))
