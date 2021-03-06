from geopy.distance import Distance
from detectores.base import DetectorDeEventos
from eventos.viaje import EventoDeViaje
from fisica.calculador_dinstancias_por_coordenadas import CalculadorDistanciasPorCoordenadas


class DetectorDeViaje(DetectorDeEventos):
    @classmethod
    def nuevo_con(cls, gps, estrategia_de_reporte_de_eventos):
        return cls(gps=gps, estrategia_de_reporte_de_eventos=estrategia_de_reporte_de_eventos)

    def __init__(self, gps, estrategia_de_reporte_de_eventos):
        self._estado = Detenido.para(detector=self)
        self._intervalo_actual = None
        self._intervalo_anterior = None

        super(DetectorDeViaje, self).__init__(gps=gps,
                                              estrategia_de_reporte_de_eventos=estrategia_de_reporte_de_eventos)

    def ubicacion_obtenida(self, intervalo):
        self._actualizar_intervalos(intervalo)

        if self._intervalo_anterior is None:
            self.cambiar_a_estado(EnViaje)
        else:
            self._estado.agregar_distancia_viaje(self._intervalo_anterior, self._intervalo_actual)

    def _actualizar_intervalos(self, nuevo_intervalo):
        self._intervalo_anterior = self._intervalo_actual
        self._intervalo_actual = nuevo_intervalo

    def reportar_nuevo_evento_de_viaje(self, distancia):
        evento = EventoDeViaje.nuevo(distancia=distancia)
        self.reportar_evento(evento)

    def cambiar_a_estado(self, estado):
        self._estado = estado.para(detector=self)

    def estado(self):
        return self._estado


class EstadoDeViaje(object):
    @classmethod
    def para(cls, detector):
        return cls(detector=detector)

    def agregar_distancia_viaje(self, intervalo1, intervalo2):
        raise NotImplementedError('responsabilidad de la subclase')


class EnViaje(EstadoDeViaje):
    def __init__(self, detector):
        self.detector = detector
        self.distancia = Distance(0)

    def agregar_distancia_viaje(self, intervalo1, intervalo2):
        distancia = CalculadorDistanciasPorCoordenadas().obtener_distancia(intervalo1.coordenadas(),
                                                                           intervalo2.coordenadas())
        self.distancia = self.distancia + distancia

        if distancia == Distance(0):
            self.detector.reportar_nuevo_evento_de_viaje(self.distancia)
            self.detector.cambiar_a_estado(Detenido)


class Detenido(EstadoDeViaje):

    def __init__(self, detector):
        self.detector = detector

    def agregar_distancia_viaje(self, intervalo1, intervalo2):
        distancia = CalculadorDistanciasPorCoordenadas().obtener_distancia(intervalo1.coordenadas(),
                                                                           intervalo2.coordenadas())
        if distancia > Distance(0):
            self.detector.cambiar_a_estado(EnViaje)
            self.detector.estado().agregar_distancia_viaje(intervalo1, intervalo2)
