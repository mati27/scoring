from datetime import datetime


class Evento(object):
    def __init__(self):
        self._fecha = datetime.now()

    def fecha(self):
        return self._fecha
