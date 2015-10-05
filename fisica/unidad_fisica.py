__author__ = 'bernapanarello'
class UnidadFisica:

    def __lt__(self, other):
        return self.magnitud < other.magnitud

    def __gt__(self, other):
        return self.magnitud > other.magnitud

    def __eq__(self, other):
        return self.magnitud == other.magnitud

    def __add__(self, other):
       self.magnitud + other.magnitud
       return self

    def __div__(self, other):
       self.magnitud/other.magnitud
       return self