
class HistorialDeEventos(object):
    @classmethod
    def para(cls, asegurado):
        return cls(asegurado=asegurado)

    def __init__(self, asegurado):
        self._asegurado = asegurado
        self._eventos = []

    def registrar_evento(self, evento):
        self._eventos.append(evento)

    def eventos_registrados(self):
        return self._eventos
