class DetectorDeEventos(object):
    def __init__(self, gps, estrategia_de_reporte_de_eventos):
        self._gps = gps
        self._estrategia_de_reporte_de_eventos = estrategia_de_reporte_de_eventos

        self._gps.agregar_observador(self)

    def ubicacion_obtenida(self, intervalo):
        raise NotImplementedError('responsabilidad de la subclase')

    def reportar_evento(self, evento):
        self._estrategia_de_reporte_de_eventos.reportar_evento(evento)
