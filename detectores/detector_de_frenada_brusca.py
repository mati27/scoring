#http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3019610/
#http://nujournal.net/HighAccuracySpeed.pdf


from eventos.frenada_brusca import EventoDeFrenadaBrusca
from fisica.calculador_aceleracion import CalculadorAceleracion
from fisica.calculador_velocidad_por_intervalos import CalculadorVelocidad

class DetectorDeFrenadaBrusca:
    @classmethod
    def nuevo_con(cls, gps, limite_aceleracion, estrategia_de_reporte_de_eventos):
        return cls(gps=gps, limite_aceleracion=limite_aceleracion,
                   estrategia_de_reporte_de_eventos=estrategia_de_reporte_de_eventos)

    def __init__(self, gps, limite_aceleracion, estrategia_de_reporte_de_eventos):
        self._estrategia_de_reporte_de_eventos = estrategia_de_reporte_de_eventos
        self._gps = gps
        self._limite_aceleracion = limite_aceleracion
        self._aceleracion = None
        self._velocidad_actual = None
        self._velocidad_anterior = None
        self._intervalo_actual = None
        self._intervalo_anterior = None
        self._estado_aceleracion = EnAceleracionNormal.para(self)
        self._gps.agregar_observador(self)

    def ubicacion_obtenida(self, intervalo):

        self.actualizar_intervalos(intervalo)
        self.actualizar_velocidades()
        self.actualizar_aceleracion()
        self.verificar_aceleracion()

    def actualizar_intervalos(self, nuevo_intervalo):
        self._intervalo_anterior = self._intervalo_actual
        self._intervalo_actual = nuevo_intervalo

    def actualizar_velocidades(self):
        if self._intervalo_anterior is not None:
            nuevaVelocidad = CalculadorVelocidad().obtener_velocidad_por_intervalos(self._intervalo_anterior,self._intervalo_actual )
            self._velocidad_anterior = self._velocidad_actual
            self._velocidad_actual = nuevaVelocidad
            print ("Velocidad actual ", self._velocidad_actual.a_kilometros_por_hora())

    def actualizar_aceleracion(self):
        if self._velocidad_anterior is not None:
          self._aceleracion = CalculadorAceleracion().obtener_aceleracion_por_delta_velocidad(self._velocidad_anterior,
                                                                                             self._intervalo_anterior.timestamp(),
                                                                                             self._velocidad_actual,


                                                                                             self._intervalo_actual.timestamp())
          print (self._aceleracion.a_gs())

    def verificar_aceleracion(self):
        if self._aceleracion is not None:
            if self._aceleracion < self._limite_aceleracion:
                self._estado_aceleracion.en_aceleracion_brusca()
            else:
                self._estado_aceleracion.en_aceleracion_normal()

    def reportar_nuevo_evento_de_frenada_brusca(self):
        evento = EventoDeFrenadaBrusca.nuevo()
        self._estrategia_de_reporte_de_eventos.reportar_evento(evento)

    def cambiar_a_estado_aceleracion_normal(self):
            self._estado_aceleracion = EnAceleracionNormal.para(self)

    def cambiar_a_estado_aceleracion_brusca(self):
            self._estado_aceleracion = EnAceleracionBrusca.para(self)


class EstadoDeAceleracion(object):
    @classmethod
    def para(cls, detector):
        return cls(detector=detector)

    def __init__(self, detector):
        self.detector = detector

    def en_aceleracion_brusca(self):
        raise NotImplementedError('responsabilidad de la subclase')

    def en_aceleracion_normal(self):
        raise NotImplementedError('responsabilidad de la subclase')


class EnAceleracionNormal(EstadoDeAceleracion):
    def en_aceleracion_brusca(self):
        self.detector.reportar_nuevo_evento_de_frenada_brusca()
        self.detector.cambiar_a_estado_aceleracion_brusca()

    def en_aceleracion_normal(self):
        pass


class EnAceleracionBrusca(EstadoDeAceleracion):
    def en_aceleracion_brusca(self):
        pass

    def en_aceleracion_normal(self):
        self.detector.cambiar_a_estado_aceleracion_normal()




