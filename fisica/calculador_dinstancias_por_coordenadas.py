from geopy.distance import great_circle
__author__ = 'bernapanarello'
class CalculadorDistanciasPorCoordenadas:
    def obtener_distancia(self, coordenada1, coordenada2):
        return great_circle(coordenada1, coordenada2)

