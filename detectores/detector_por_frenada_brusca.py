__author__ = 'bernapanarello'
#http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3019610/
#Calculo de velocidad

class DetectorPorFrenadaBrusca:
    def __init__(self, limite_deceleracion, velocidad_parada):
        self.limite_deceleracion = limite_deceleracion
        self.velocidad_parada = velocidad_parada

    def ubicacion_obtenida(self, intervalo):


