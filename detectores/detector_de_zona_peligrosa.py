from detectores.base import DetectorDeEventos
from eventos.zona_peligrosa import EventoDeViajeAZonaPeligrosa


class DetectorDeViajeAZonaPeligrosa(DetectorDeEventos):
    @classmethod
    def nuevo_con(cls, gps, zonas_peligrosas, estrategia_de_reporte_de_eventos):
        return cls(gps=gps, zonas_peligrosas=zonas_peligrosas,
                   estrategia_de_reporte_de_eventos=estrategia_de_reporte_de_eventos)

    def __init__(self, gps, zonas_peligrosas, estrategia_de_reporte_de_eventos):
        self._zonas_peligrosas = zonas_peligrosas
        self._estado = FueraDeZonaPeligrosa.para(detector=self)

        super(DetectorDeViajeAZonaPeligrosa, self).__init__(gps=gps,
                                                            estrategia_de_reporte_de_eventos=estrategia_de_reporte_de_eventos)

    def ubicacion_obtenida(self, intervalo):
        self._detectar_si_se_encuentra_en_zona_peligrosa_y_reportar(intervalo.coordenadas())

    def _detectar_si_se_encuentra_en_zona_peligrosa_y_reportar(self, coordenadas):
        for zona_peligrosa in self._zonas_peligrosas:
            if zona_peligrosa.esta_dentro(coordenadas):

                self._estado.se_encuentra_en(zona_peligrosa=zona_peligrosa)
                return

        self._estado.fuera_de_zonas_peligrosas()

    def reportar_nuevo_evento_de_viaje_a(self, zona_peligrosa):
        evento = EventoDeViajeAZonaPeligrosa.nuevo(zona=zona_peligrosa)
        self.reportar_evento(evento)

    def cambiar_a_estado(self, estado):
        self._estado = estado.para(detector=self)


class EstadoDeUbicacion(object):
    @classmethod
    def para(cls, detector):
        return cls(detector=detector)

    def __init__(self, detector):
        self.detector = detector

    def se_encuentra_en(self, zona_peligrosa):
        raise NotImplementedError('responsabilidad de la subclase')

    def fuera_de_zonas_peligrosas(self):
        raise NotImplementedError('responsabilidad de la subclase')


class FueraDeZonaPeligrosa(EstadoDeUbicacion):
    def se_encuentra_en(self, zona_peligrosa):
        self.detector.reportar_nuevo_evento_de_viaje_a(zona_peligrosa=zona_peligrosa)
        self.detector.cambiar_a_estado(EnZonaPeligrosa)

    def fuera_de_zonas_peligrosas(self):
        pass


class EnZonaPeligrosa(EstadoDeUbicacion):
    def se_encuentra_en(self, zona_peligrosa):
        pass

    def fuera_de_zonas_peligrosas(self):
        self.detector.cambiar_a_estado(FueraDeZonaPeligrosa)


