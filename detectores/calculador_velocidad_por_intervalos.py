from detectores.calculador_dinstancias_por_coordenadas import CalculadorDistanciasPorCoordenadas
from detectores.velocidad import Velocidad

__author__ = 'bernapanarello'


class CalculadorVelocidadPorIntervalos:
    def calcular_velocidad(self, intervalo_inicial, intervalo_final):
        distancia = CalculadorDistanciasPorCoordenadas().calculador.calcular_distancia(intervalo_inicial.coordenadas,
                                                                                       intervalo_final.coordenadas)
        return Velocidad(distancia.meters / (intervalo_final.timestamp - intervalo_inicial.timestamp).seconds)

