from fisica.aceleracion import Aceleracion

__author__ = 'bernapanarello'
class CalculadorAceleracion:
    def obtener_aceleracion_por_delta_velocidad(self, velocidadInicial, tiempoInicial, velocidadFinal, tiempoFinal):
        aceleracion = (velocidadFinal.a_metros_por_segundo - velocidadInicial.a_metros_por_segundo) / (tiempoInicial - tiempoFinal).seconds
        return Aceleracion(aceleracion)

