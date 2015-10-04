__author__ = 'bernapanarello'
class CotizadorBase:
    def acepta_evento(self, evento):
        raise NotImplementedError('responsabilidad de la subclase')

    def obtener_cotizacion_evento(self, evento):
        raise NotImplementedError('responsabilidad de la subclase')

    def tipo_cotizador(self):
        raise NotImplementedError('responsabilidad de la subclase')
