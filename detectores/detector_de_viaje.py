from geopy.distance import great_circle
from eventos.viaje import EventoDeViaje
from fisica.calculador_dinstancias_por_coordenadas import CalculadorDistanciasPorCoordenadas
from fisica.calculador_velocidad_por_intervalos import CalculadorVelocidad
from geolocalizacion.proveedor_velocidad_maxima import ProveedorVelocidadMaxima
from fisica.velocidad import Velocidad

class DetectorDeViaje(object):
    @classmethod
    def nuevo_con(cls, gps, estrategia_de_reporte_de_eventos):
        return cls(gps=gps, estrategia_de_reporte_de_eventos=estrategia_de_reporte_de_eventos)

    def __init__(self, gps, estrategia_de_reporte_de_eventos):
        self._gps = gps
        self._estrategia_de_reporte_de_eventos = estrategia_de_reporte_de_eventos
        self._estado = Detenido.para(detector=self)
        self._intervalo_actual = None
        self._intervalo_anterior = None

        self._gps.agregar_observador(self)

    def ubicacion_obtenida(self, intervalo):
        self._actualizar_intervalos(intervalo)

        if(self._intervalo_anterior == None):
            self.cambiar_a_estado(EnViaje)
        else:
            self._estado.agregar_distancia_viaje(self._intervalo_anterior, self._intervalo_actual)

    def _actualizar_intervalos(self, nuevo_intervalo):
        self._intervalo_anterior = self._intervalo_actual
        self._intervalo_actual = nuevo_intervalo


    def reportar_nuevo_evento_de_viaje(self, distancia):
        evento = EventoDeViaje.nuevo(distancia = distancia)
        self._estrategia_de_reporte_de_eventos.reportar_evento(evento)

    def cambiar_a_estado(self, estado):
        self._estado = estado.para(detector=self)

    def estado(self):
        return self._estado


class EstadoDeDeteccion(object):
    @classmethod
    def para(cls, detector):
        return cls(detector=detector)


    def agregar_distancia_viaje(self, intervalo1,intervalo2):
        raise NotImplementedError('responsabilidad de la subclase')


class EnViaje(EstadoDeDeteccion):

    def __init__(self, detector):
        self.detector = detector
        self.distancia = great_circle()


    def agregar_distancia_viaje(self, intervalo1,intervalo2):
        distancia = CalculadorDistanciasPorCoordenadas().obtener_distancia(intervalo1.coordenadas(),intervalo2.coordenadas())
        self.distancia = self.distancia + distancia

        if(distancia == great_circle()):
            self.detector.reportar_nuevo_evento_de_viaje(self.distancia)
            self.detector.cambiar_a_estado(Detenido)


class Detenido(EstadoDeDeteccion):

    def __init__(self, detector):
        self.detector = detector

    def agregar_distancia_viaje(self, intervalo1,intervalo2):
        distancia = CalculadorDistanciasPorCoordenadas().obtener_distancia(intervalo1.coordenadas(),intervalo2.coordenadas())
        if(distancia > great_circle()):
            self.detector.cambiar_a_estado(EnViaje)
            self.detector.estado().agregar_distancia_viaje(intervalo1,intervalo2)



