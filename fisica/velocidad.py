__author__ = 'bernapanarello'
class Velocidad(UnidadFisica):
    def __init__(self, magnitud):
        self.magnitud = magnitud

    def a_kilometros_por_hora(self):
        return (self.magnitud * 60) / 1000

    def a_metros_por_segundo(self):
        return self.magnitud
