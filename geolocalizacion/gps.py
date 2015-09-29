import time
from datetime import datetime


class GPS(object):
    @classmethod
    def nuevo(cls, satelite, actualizar_cada):
        return cls(satelite=satelite, actualizar_cada=actualizar_cada)

    def __init__(self, satelite, actualizar_cada):
        self.satelite = satelite
        self.actualizar_cada = actualizar_cada
        self.observadores = []

    def agregar_observador(self, observador):
        self.observadores.append(observador)

    def obtener_ubicacion_actual(self):
        return self.satelite.obtener_ubicacion_de(gps=self)

    def activar(self):
        self._obtener_ubicacion_actual_mientras_haya_respuesta()

    def procesar_respuesta_de_coordenadas(self, respuesta):
        intervalo = Intervalo.con(coordenadas=respuesta.coordenadas(), timestamp=datetime.now())

        self._notificar_observadores_con(nuevo_intervalo=intervalo)

        self._esperar_proxima_respuesta()

    def procesar_respuesta_vacia(self, respuesta):
        pass

    def _obtener_ubicacion_actual_mientras_haya_respuesta(self):
        respuesta = self.obtener_ubicacion_actual()

        respuesta.procesar_desde(gps=self)

    def _notificar_observadores_con(self, nuevo_intervalo):
        for observador in self.observadores:
            observador.ubicacion_obtenida(nuevo_intervalo)

    def _esperar_proxima_respuesta(self):
        time.sleep(self.actualizar_cada.total_seconds())

        self._obtener_ubicacion_actual_mientras_haya_respuesta()


class Intervalo(object):
    @classmethod
    def con(cls, coordenadas, timestamp):
        return cls(coordenadas=coordenadas, timestamp=timestamp)

    def __init__(self, coordenadas, timestamp):
        self._coordenadas = coordenadas
        self._timestamp = timestamp

    def coordenadas(self):
        return self._coordenadas

    def latitud(self):
        return self.coordenadas()[0]

    def longitud(self):
        return self.coordenadas()[1]

    def timestamp(self):
        return self._timestamp
