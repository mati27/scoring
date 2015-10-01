from fisica.calculador_dinstancias_por_coordenadas import CalculadorDistanciasPorCoordenadas
from fisica.velocidad import Velocidad

__author__ = 'bernapanarello'


class CalculadorVelocidad:
    def obtener_velocidad_por_intervalos(self, intervalo_inicial, intervalo_final):
        distancia = CalculadorDistanciasPorCoordenadas().calculador.calcular_distancia(intervalo_inicial.coordenadas,
                                                                                       intervalo_final.coordenadas)
        return Velocidad(distancia.meters / (intervalo_final.timestamp - intervalo_inicial.timestamp).seconds)

