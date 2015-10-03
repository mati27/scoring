from scoreador.scoring import Scoring


class Scoreador:
    def __init__(self, proveedor_cotizadores):
        self._proveedor_cotizadores = proveedor_cotizadores


    def cotizar(self, kilometraje, eventos):
        cotizadores = self._proveedor_cotizadores.obtener_cotizadores_eventos()
        cotizador_kilometraje = self._proveedor_cotizadores.obtener_cotizador_kilometraje()
        ret = 0
        for evento in eventos:
            ret = ret + self.cotizar_evento(evento, cotizadores)

        ret += cotizador_kilometraje.cotizar(kilometraje)

        return ret


    def cotizar_evento(self, evento, cotizadores):
        cotizador = next((c for c in cotizadores if c.acepta(evento)), None)
        if (cotizador is None):
            raise RuntimeError('No se encontró un cotizador para el evento', evento)

        return cotizador.cotizar(evento)