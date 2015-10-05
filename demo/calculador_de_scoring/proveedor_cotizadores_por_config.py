from scoreador.proveedor_cotizadores import ProveedorCotizadoresEventos


class ProveedorCotizadoresPorConfig(ProveedorCotizadoresEventos):
    def __init__(self, config):
        self._config = config

    def obtener_cotizadores_eventos(self):

        cotizadores = []

        for configuracion_de_cotizador in self._config:
            tipo_de_cotizador = configuracion_de_cotizador['tipo']

            cotizador = tipo_de_cotizador(**configuracion_de_cotizador['parametros'])
            cotizadores.append(cotizador)

        return cotizadores



