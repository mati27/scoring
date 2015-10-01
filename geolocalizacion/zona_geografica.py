import math


class ZonaGeografica(object):
    @classmethod
    def definida_por(cls, vertice, vertice_opuesto):
        return cls(vertice=vertice, vertice_opuesto=vertice_opuesto)

    def __init__(self, vertice, vertice_opuesto):
        self.izquierda = min(vertice[0], vertice_opuesto[0])
        self.derecha = max(vertice[0], vertice_opuesto[0])
        self.abajo = min(vertice[1], vertice_opuesto[1])
        self.arriba = max(vertice[1], vertice_opuesto[1])

    def esta_dentro(self, coordenada):
        return self.izquierda <= coordenada[0] <= self.derecha and self.abajo <= coordenada[1] <= self.arriba
