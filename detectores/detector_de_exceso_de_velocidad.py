from geopy.distance import Distance
from detectores.base import DetectorDeEventos
from eventos.exceso_velocidad import EventoDeExcesoDeVelocidad
from fisica.calculador_dinstancias_por_coordenadas import CalculadorDistanciasPorCoordenadas
from fisica.calculador_velocidad_por_intervalos import CalculadorVelocidad


class DetectorDeExcesoDeVelocidad(DetectorDeEventos):
    @classmethod
    def nuevo_con(cls, gps, estrategia_de_reporte_de_eventos, proveedor_velocidad_maxima, porcentaje_de_velocidad_maxima, distancia_excedido):
        return cls(gps=gps, estrategia_de_reporte_de_eventos=estrategia_de_reporte_de_eventos,proveedor_velocidad_maxima=proveedor_velocidad_maxima, porcentaje_de_velocidad_maxima= porcentaje_de_velocidad_maxima, distancia_excedido = distancia_excedido)

    def __init__(self, gps, estrategia_de_reporte_de_eventos, proveedor_velocidad_maxima, porcentaje_de_velocidad_maxima, distancia_excedido):

        self._proveedor_velocidad_maxima = proveedor_velocidad_maxima
        self._estado = EnVelocidadNoExcedida.para(detector=self)
        self._intervalo_actual = None
        self._intervalo_anterior = None
        self._porcentaje_de_velocidad_maxima = porcentaje_de_velocidad_maxima
        self._distancia_excedido = distancia_excedido

        super(DetectorDeExcesoDeVelocidad, self).__init__(gps=gps,
                                                          estrategia_de_reporte_de_eventos=estrategia_de_reporte_de_eventos)

    def ubicacion_obtenida(self, intervalo):

        self._actualizar_intervalos(intervalo)
        if self._intervalo_anterior is not None:
            if self._detectar_si_se_encuentra_excedido_en_velocidad(intervalo.coordenadas()):
                self._estado.agregar_distancia_excedido(self._intervalo_anterior, self._intervalo_actual)


    def _actualizar_intervalos(self, nuevo_intervalo):
        self._intervalo_anterior = self._intervalo_actual
        self._intervalo_actual = nuevo_intervalo

    def _detectar_si_se_encuentra_excedido_en_velocidad(self, coordenadas):

        velocidad = CalculadorVelocidad().obtener_velocidad_por_intervalos(self._intervalo_anterior,
                                                                           self._intervalo_actual)
        velocidad_maxima = self._proveedor_velocidad_maxima.velocidad_maxima(coordenadas)
        porcentaje = self._porcentaje_de_velocidad_maxima
        velocidad_tope = velocidad_maxima.multiplicar_por_escalar(porcentaje).dividir_por_escalar(
            100) + velocidad_maxima

        return velocidad > velocidad_tope

    def reportar_nuevo_evento_de_exceso_de_velocidad(self, porcentaje_de_velocidad, porcentaje_excedido):

        evento = EventoDeExcesoDeVelocidad.nuevo(porcentaje_de_velocidad=porcentaje_de_velocidad,
                                                 porcentaje_excedido=porcentaje_excedido)
        self.reportar_evento(evento)

    def cambiar_a_estado(self, estado):
        self._estado = estado.para(detector=self)

    def estado(self):
        return self._estado

    def distancia_excedido(self):
        return self._distancia_excedido

    def porcentaje_de_velocidad_maxima(self):
        return self._porcentaje_de_velocidad_maxima

    def proveedor_de_velocidad_maxima(self):
        return self._proveedor_velocidad_maxima


class EstadoDeDeteccion(object):
    @classmethod
    def para(cls, detector):
        return cls(detector=detector)

    def agregar_distancia_excedido(self, intervalo1, intervalo2):
        raise NotImplementedError('responsabilidad de la subclase')


class EnVelocidadExcedida(EstadoDeDeteccion):

    def __init__(self, detector):
        self.detector = detector
        self.distancia_excedido = Distance(0)

    def agregar_distancia_excedido(self, intervalo1, intervalo2):
        distancia = CalculadorDistanciasPorCoordenadas().obtener_distancia(intervalo1.coordenadas(),
                                                                           intervalo2.coordenadas())
        self.distancia_excedido = self.distancia_excedido + distancia

        if self.distancia_excedido > self.detector.distancia_excedido():
            velocidad_excedido = CalculadorVelocidad().obtener_velocidad_por_intervalos(intervalo1, intervalo2)
            velocidad_maxima = (self.detector.proveedor_de_velocidad_maxima()).velocidad_maxima(intervalo2.coordenadas())
            porcentaje_excedido = ((velocidad_excedido.a_metros_por_segundo() * 100) / velocidad_maxima.a_metros_por_segundo()) - 100


            self.detector.reportar_nuevo_evento_de_exceso_de_velocidad(self.detector.porcentaje_de_velocidad_maxima(),
                                                                       porcentaje_excedido)

            distancia_que_sigue_excedido = self.distancia_excedido - self.detector.distancia_excedido()
            if distancia_que_sigue_excedido > Distance(0):
                self.distancia_excedido = distancia_que_sigue_excedido
            else:
                self.detector.cambiar_a_estado(EnVelocidadNoExcedida)


class EnVelocidadNoExcedida(EstadoDeDeteccion):
    def __init__(self, detector):
        self.detector = detector

    def agregar_distancia_excedido(self, intervalo1, intervalo2):
        self.detector.cambiar_a_estado(EnVelocidadExcedida)
        self.detector.estado().agregar_distancia_excedido(intervalo1, intervalo2)
