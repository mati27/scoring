from fisica.velocidad import Velocidad


class ProveedorVelocidadMaxima(object):
    @classmethod
    def nuevo(cls, catalogo_de_velocidades_maximas):
        return cls(catalogo_de_velocidades_maximas=catalogo_de_velocidades_maximas)

    def __init__(self, catalogo_de_velocidades_maximas):
        self._catalogo_de_velocidades_maximas = catalogo_de_velocidades_maximas

    def velocidad_maxima(self, coordenadas):
        velocidad_maxima = Velocidad(100)

        for zona,velocidad_maxima_zona in self._catalogo_de_velocidades_maximas.items():
            if zona.esta_dentro(coordenadas):
                velocidad_maxima =  velocidad_maxima_zona


        return velocidad_maxima