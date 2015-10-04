class Scoreador:
    def __init__(self, proveedor_cotizadores):
        self._proveedor_cotizadores = proveedor_cotizadores


    def cotizar(self, eventos):
        cotizadores = self._proveedor_cotizadores.obtener_cotizadores_eventos()
        ret = 0
        for evento in eventos:
            ret = ret + self.cotizar_evento(evento, cotizadores)

        return ret


    def cotizar_evento(self, evento, cotizadores):
        cotizador = next((c for c in cotizadores if c.acepta_evento (evento)), None)
        if (cotizador is None):
            raise RuntimeError('No se encontro un cotizador para el evento', evento)

        return cotizador.obtener_cotizacion_evento (evento)