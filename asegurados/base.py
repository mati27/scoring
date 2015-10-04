class Asegurado(object):
    @classmethod
    def con(cls, nombre):
        return cls(nombre=nombre)

    def __init__(self, nombre):
        self._nombre = nombre

    def nombre(self):
        return self._nombre