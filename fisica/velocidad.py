from fisica.unidad_fisica import UnidadFisica

__author__ = 'bernapanarello'
class Velocidad(UnidadFisica):
    def __init__(self, magnitud):
        self.magnitud = magnitud

    def a_kilometros_por_hora(self):
        return (self.magnitud * 3600) / 1000

    def a_metros_por_segundo(self):
        return self.magnitud

    def multiplicar_por_escalar(self, escalar):
        self.magnitud * escalar
        return self

    def dividir_por_escalar(self, escalar):
        self.magnitud/escalar
        return self

