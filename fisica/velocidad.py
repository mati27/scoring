from fisica.unidad_fisica import UnidadFisica

__author__ = 'bernapanarello'
class Velocidad(UnidadFisica):
    @classmethod
    def nueva_con_km_por_h(cls, magnitud):
        magnitud_m_por_s = (magnitud * 1000) / 3600
        return cls(magnitud_m_por_s)


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

