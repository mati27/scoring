from eventos.exceso_velocidad import EventoDeExcesoDeVelocidad
from fisica.calculador_dinstancias_por_coordenadas import CalculadorDistanciasPorCoordenadas
from fisica.calculador_velocidad_por_intervalos import CalculadorVelocidad
from geolocalizacion.proveedor_velocidad_maxima import ProveedorVelocidadMaxima
from fisica.velocidad import Velocidad

class DetectorDeExcesoDeVelocidad(object):
    @classmethod
    def nuevo_con(cls, gps, proveedor_velocidad_maxima, estrategia_de_reporte_de_eventos, porcentaje_de_velocidad, distancia_excedido):
        return cls(gps=gps, proveedor_velocidad_maxima=proveedor_velocidad_maxima,
                   estrategia_de_reporte_de_eventos=estrategia_de_reporte_de_eventos, porcentaje_de_velocidad= porcentaje_de_velocidad, distancia_excedido = distancia_excedido)

    def __init__(self, gps, proveedor_velocidad_maxima, estrategia_de_reporte_de_eventos, porcentaje_de_velocidad, distancia_excedido):
        self._gps = gps
        self._proveedor_velocidad_maxima = proveedor_velocidad_maxima
        self._estrategia_de_reporte_de_eventos = estrategia_de_reporte_de_eventos
        self._estado = EnVelocidadNoExcedida.para(detector=self)
        self._intervalo_actual = None
        self._intervalo_anterior = None
        self._porcentaje_de_velocidad = porcentaje_de_velocidad
        self._distancia_excedido = distancia_excedido

        self._gps.agregar_observador(self)

    def ubicacion_obtenida(self, intervalo):
        self._actualizar_intervalos(intervalo)
        if(self._intervalo_anterior != None):
            if (self._detectar_si_se_encuentra_excedido_en_velocidad(intervalo.coordenadas())):
                self._estado.agregar_distancia_excedido(self._intervalo_anterior, self._intervalo_actual)

    def _actualizar_intervalos(self, nuevo_intervalo):
        self._intervalo_anterior = self._intervalo_actual
        self._intervalo_actual = nuevo_intervalo


    def _detectar_si_se_encuentra_excedido_en_velocidad(self, coordenadas):

        velocidad = CalculadorVelocidad().obtener_velocidad_por_intervalos(self._intervalo_anterior,self._intervalo_actual )
        velocidad_maxima = self._proveedor_velocidad_maxima.velocidad_maxima(coordenadas)
        porcentaje = self._porcentaje_de_velocidad
        velocidad_tope = velocidad_maxima.multiplicar_por_escalar(porcentaje).dividir_por_escalar(100) + velocidad_maxima

        return velocidad > velocidad_tope


    def reportar_nuevo_evento_de_exceso_de_velocidad(self, porcentaje_de_velocidad, velocidad_excedido):
        evento = EventoDeExcesoDeVelocidad.nuevo(porcentaje_de_velocidad = porcentaje_de_velocidad, velocidad_excedido = velocidad_excedido )
        self._estrategia_de_reporte_de_eventos.reportar_evento(evento)

    def cambiar_a_estado(self, estado):
        self._estado = estado.para(detector=self)

    def estado(self):
        return self._estado

    def distancia_excedido(self):
        return self._distancia_excedido

    def porcentaje_de_velocidad(self):
        return self._porcentaje_de_velocidad


class EstadoDeDeteccion(object):
    @classmethod
    def para(cls, detector):
        return cls(detector=detector)

    def agregar_distancia_excedido(self, distancia):
        raise NotImplementedError('responsabilidad de la subclase')


class EnVelocidadExcedida(EstadoDeDeteccion):

    def __init__(self, detector):
        self.detector = detector
        self.distancia_excedido = 0

    def agregar_distancia_excedido(self, intervalo1,intervalo2):
        distancia = CalculadorDistanciasPorCoordenadas().obtener_distancia(intervalo1.coordenadas(),intervalo2.coordenadas())
        self.distancia_excedido = self.distancia_excedido + distancia.meters

        if(self.distancia_excedido > (self.detector).distancia_excedido()):
            velocidad_excedido = CalculadorVelocidad().obtener_velocidad_por_intervalos(intervalo1,intervalo2 )
            self.detector.reportar_nuevo_evento_de_exceso_de_velocidad(self.detector.porcentaje_de_velocidad, velocidad_excedido)

            distancia_que_sigue_excedido = (self.distancia_excedido) - ((self.detector).distancia_excedido())
            if (distancia_que_sigue_excedido > 0):
                self.distancia_excedido = distancia_que_sigue_excedido
            else:
                self.detector.cambiar_a_estado(EnVelocidadNoExcedida)


class EnVelocidadNoExcedida(EstadoDeDeteccion):

    def __init__(self, detector):
        self.detector = detector

    def agregar_distancia_excedido(self, intervalo1,intervalo2):
        self.detector.cambiar_a_estado(EnVelocidadExcedida)
        self.detector.estado().agregar_distancia_excedido(intervalo1,intervalo2)


