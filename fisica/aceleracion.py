from fisica.unidad_fisica import UnidadFisica

__author__ = 'bernapanarello'
class Aceleracion(UnidadFisica):
    def __init__(self, magnitud):
        self.magnitud = magnitud

    def a_gs(self):
        return self.magnitud / 9.8

    def a_ms2(self):
        return self.magnitud


