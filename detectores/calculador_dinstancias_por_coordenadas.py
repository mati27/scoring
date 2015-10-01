from geopy.distance import great_circle
__author__ = 'bernapanarello'
class CalculadorDistanciasPorCoordenadas:
    def calcular_distancia(self, coordenada1, coordenada2):
        return great_circle(coordenada1, coordenada2)

