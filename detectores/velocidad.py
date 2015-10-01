__author__ = 'bernapanarello'
class Velocidad:
    def __init__(self, magnitud):
        self.magnitud = magnitud

    def kilometros_por_hora(self):
        return (self.magnitud * 60) / 1000

    def metros_por_segundo(self):
        return self.magnitud
