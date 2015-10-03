class CotizadorKilometraje:
    def cotizar(self, distancia):
        raise NotImplementedError('responsabilidad de la subclase')


class CotizadorKilometrajePorPenalizacionFija(CotizadorKilometraje):
    def __init__(self, distancia_penalizable, penalizacion):
        self._penalizacion = penalizacion
        self._distancia_penalizable = distancia_penalizable

    def cotizar(self, distancia):
        ratio = int(distancia / self._distancia_penalizable)
        return ratio * self._penalizacion

    @classmethod
    def con_puntos_para_distancia(cls, distancia_penalizable, penalizacion):
        return cls(distancia_penalizable=distancia_penalizable, penalizacion=penalizacion)

