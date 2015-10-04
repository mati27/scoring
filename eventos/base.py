from datetime import datetime


class Evento(object):
    def __init__(self):
        self._fecha = datetime.now()

    def fecha(self):
        return self._fecha


class EstrategiaDeReporteDeEventos(object):
    def reportar_evento(self, evento):
        raise NotImplementedError('responsabilidad de la subclase')


class RegistrarEnHistorialDeEventos(EstrategiaDeReporteDeEventos):
    def __init__(self, historial_de_eventos):
        self._historial_de_eventos = historial_de_eventos

    def reportar_evento(self, evento):
        self._historial_de_eventos.registrar_evento(evento)
