from unittest import TestCase
from geopy.distance import Distance
from eventos.exceso_velocidad import EventoDeExcesoDeVelocidad
from eventos.frenada_brusca import EventoDeFrenadaBrusca
from eventos.viaje import EventoDeViaje
from eventos.zona_peligrosa import EventoDeViajeAZonaPeligrosa
from scoreador.scoreador import Scoreador

from tests.proveedor_cotizadores_para_test import ProveedorCotizadoresParaTest


class ScorearEventos(TestCase):
    def setUp(self):
        pass


    def test_scorear_2_frenadas_bruscas_y_2_viajes_a_zona_peligrosa(self):
        scoreador = Scoreador(proveedor_cotizadores=ProveedorCotizadoresParaTest())
        eventos = [
            EventoDeFrenadaBrusca.nuevo(),
            EventoDeViajeAZonaPeligrosa.nuevo(None),
            EventoDeViajeAZonaPeligrosa.nuevo(None),
            EventoDeFrenadaBrusca.nuevo()

        ]

        scoring = scoreador.cotizar(eventos)
        self.assertEquals(scoring, 120)


    #Suponiendo 10ptos por cada 2000km, 20 viajes de 200 suman 4000km, tiene que scorear 20ptos
    def test_20_viajes_20km_suman_20ptos_scoring(self):
        scoreador = Scoreador(proveedor_cotizadores=ProveedorCotizadoresParaTest())
        eventos = [
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200)),
            EventoDeViaje.nuevo(Distance(200))
        ]

        scoring = scoreador.cotizar(eventos)
        self.assertEquals(scoring, 20)

    def test_dos_rangos_de_exceso_velocidad(self):
        scoreador = Scoreador(proveedor_cotizadores=ProveedorCotizadoresParaTest())
        eventos = [
            EventoDeExcesoDeVelocidad.nuevo(27, None),
            EventoDeExcesoDeVelocidad.nuevo(45, None)

        ]

        scoring = scoreador.cotizar(eventos)
        self.assertEquals(scoring, 120)