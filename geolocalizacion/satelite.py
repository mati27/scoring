class SateliteMock(object):
    @classmethod
    def usando(cls, simulador_de_recorrido):
        return cls(simulador_de_recorrido=simulador_de_recorrido)

    def __init__(self, simulador_de_recorrido):
        self.simulador_de_recorrido = simulador_de_recorrido

    def obtener_ubicacion_de(self, gps):
        if not self.simulador_de_recorrido.termino_el_recorrido():
            punto_del_recorrido = self.simulador_de_recorrido.siguiente_punto_del_recorrido()
            return RespuestaDeCoordenadas.nueva_con(coordenadas=punto_del_recorrido)

        return RespuestaVacia()


class SimuladorDeRecorrido(object):
    @classmethod
    def simular_usando(cls, estrategia):
        return cls(estrategia=estrategia)

    def __init__(self, estrategia):
        self.estrategia = estrategia

    def siguiente_punto_del_recorrido(self):
        return self.estrategia.siguiente_punto_del_recorrido()

    def termino_el_recorrido(self):
        return self.estrategia.termino_el_recorrido()


class EstrategiaDeRecorrido(object):
    def siguiente_punto_del_recorrido(self):
        raise NotImplementedError('subclass responsibility')

    def termino_el_recorrido(self):
        raise NotImplementedError('subclass responsibility')


class RecorridoEnLista(EstrategiaDeRecorrido):
    @classmethod
    def usando(cls, lista_de_puntos_de_recorrido):
        return cls(lista_de_puntos_de_recorrido=lista_de_puntos_de_recorrido)

    def __init__(self, lista_de_puntos_de_recorrido):
        self.lista_de_puntos_de_recorrido = lista_de_puntos_de_recorrido

    def siguiente_punto_del_recorrido(self):
        return self.lista_de_puntos_de_recorrido.pop(0)

    def termino_el_recorrido(self):
        return len(self.lista_de_puntos_de_recorrido) == 0


class RecorridoEnArchivo(EstrategiaDeRecorrido):
    @classmethod
    def usando(cls, archivo_de_recorrido):
        return cls(archivo_de_recorrido=archivo_de_recorrido)

    def __init__(self, archivo_de_recorrido):
        self.coordenadas_del_recorrido = []

        self._leer_archivo_y_obtener_coordenadas(archivo_de_recorrido)

    def siguiente_punto_del_recorrido(self):
        return self.coordenadas_del_recorrido.pop(0)

    def termino_el_recorrido(self):
        return len(self.coordenadas_del_recorrido) == 0

    def _abrir(self, nombre_de_archivo):
        return open(nombre_de_archivo)

    def _cerrar(self, archivo_de_recorrido):
        return archivo_de_recorrido.close()

    def _contruir_coordenadas(self, coordenadas_como_texto):
        coordenadas = coordenadas_como_texto.split(',')
        return float(coordenadas[0]), float(coordenadas[1])

    def _leer_archivo_y_obtener_coordenadas(self, nombre_archivo_de_recorrido):
        archivo_de_recorrido = self._abrir(nombre_de_archivo=nombre_archivo_de_recorrido)
        
        for linea_de_coordenadas in archivo_de_recorrido:
            self.coordenadas_del_recorrido.append(self._contruir_coordenadas(linea_de_coordenadas))

        self._cerrar(archivo_de_recorrido)


class RespuestaDeSatelite(object):
    def procesar_desde(self, gps):
        raise NotImplementedError('subclass responsibility')


class RespuestaDeCoordenadas(RespuestaDeSatelite):
    @classmethod
    def nueva_con(cls, coordenadas):
        return cls(coordenadas=coordenadas)

    def __init__(self, coordenadas):
        self._coordenadas = coordenadas

    def coordenadas(self):
        return self._coordenadas

    def procesar_desde(self, gps):
        gps.procesar_respuesta_de_coordenadas(self)


class RespuestaVacia(RespuestaDeSatelite):
    def procesar_desde(self, gps):
        gps.procesar_respuesta_vacia(self)
