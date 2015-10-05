# coding=utf-8
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import View

from asegurados.historial_de_eventos import HistorialDeEventos
from calculador_de_scoring.models import PersistidorDeEventos, SerializadorPickle
from calculador_de_scoring.proveedor_cotizadores_por_config import ProveedorCotizadoresPorConfig
from configuracion import CONFIGURACION_DE_DETECTORES, CONFIGURACION_DE_COTIZADORES
from detectores.detector_de_exceso_de_velocidad import DetectorDeExcesoDeVelocidad
from detectores.detector_de_frenada_brusca import DetectorDeFrenadaBrusca
from detectores.detector_de_viaje import DetectorDeViaje
from detectores.detector_de_zona_peligrosa import DetectorDeViajeAZonaPeligrosa
from eventos.base import RegistrarEnHistorialDeEventos
from forms import FormularioDeDeteccionDeEventos
from models import DeteccionDeEventos
from geolocalizacion.gps import GPS
from geolocalizacion.satelite import SateliteMock, SimuladorDeRecorrido, RecorridoEnArchivo
from scoreador.scoreador import Scoreador


class VistaPaso1(View):
    def get(self, request):
        tabla_de_detectores = TablaDeDetectores(configuracion_de_detectores=CONFIGURACION_DE_DETECTORES)
        formulario_de_deteccion_de_eventos = FormularioDeDeteccionDeEventos()
        return render(request, 'paso_1.html', context={'tabla_de_detectores': tabla_de_detectores,
                                                       'formulario_de_deteccion_de_eventos': formulario_de_deteccion_de_eventos})

    def post(self, request):
        formulario_de_deteccion_de_eventos = FormularioDeDeteccionDeEventos(request.POST, request.FILES)
        tabla_de_detectores = TablaDeDetectores(configuracion_de_detectores=CONFIGURACION_DE_DETECTORES)

        if formulario_de_deteccion_de_eventos.is_valid():
            deteccion = DeteccionDeEventos.nueva_con(**formulario_de_deteccion_de_eventos.cleaned_data)

            self.detectar_eventos(deteccion)

            return redirect('resultado', id_deteccion=deteccion.id)

        return render(request, 'paso_1.html', context={'tabla_de_detectores': tabla_de_detectores,
                                                       'formulario_de_deteccion_de_eventos': formulario_de_deteccion_de_eventos})

    def detectar_eventos(self, deteccion):
        simulador_de_recorrido = SimuladorDeRecorrido.simular_usando(
            RecorridoEnArchivo.usando(archivo_de_recorrido=deteccion.recorrido.file.name))

        gps = GPS.nuevo(satelite=SateliteMock.usando(simulador_de_recorrido), actualizar_cada=timedelta(microseconds=1))
        historial_de_eventos = HistorialDeEventos.para(asegurado=deteccion.asegurado)

        self.crear_detectores(gps, historial_de_eventos)

        gps.activar()

        self.persistir_eventos_de(deteccion, historial_de_eventos)

    def crear_detectores(self, gps, historial_de_eventos):
        detectores = []

        for configuracion_de_detector in CONFIGURACION_DE_DETECTORES:
            tipo_de_detector = configuracion_de_detector['tipo']
            estrategia_de_reporte_de_eventos = RegistrarEnHistorialDeEventos.nuevo_con(historial_de_eventos=historial_de_eventos)

            detector = tipo_de_detector.nuevo_con(gps=gps,
                                                  estrategia_de_reporte_de_eventos=estrategia_de_reporte_de_eventos,
                                                  **configuracion_de_detector['parametros'])
            detectores.append(detector)

        return detectores

    def persistir_eventos_de(self, deteccion, historial_de_eventos):
        persistidor = PersistidorDeEventos(serializador=SerializadorPickle())

        for evento in historial_de_eventos.eventos_registrados():
            persistidor.persistir(deteccion, evento)


class VistaPaso2(View):
    def get(self, request, id_deteccion):
        deteccion = get_object_or_404(DeteccionDeEventos, id=id_deteccion)

        eventos = self.obtener_eventos_de(deteccion)
        tabla_de_eventos = TablaDeEventos(eventos=eventos)

        scoreador = self.obtener_scoreador()
        puntaje = scoreador.cotizar(eventos)

        return render(request, 'paso_2.html', context={'tabla_de_eventos': tabla_de_eventos, 'puntaje': puntaje})

    def post(self, request):
        pass

    def obtener_eventos_de(self, deteccion):
        eventos = []
        serializador = SerializadorPickle()

        for evento_detectado in deteccion.eventos_detectados():
            evento = serializador.deserializar(evento_detectado.evento_serializado)
            eventos.append(evento)

        return eventos

    def obtener_scoreador(self):
        proveedor = ProveedorCotizadoresPorConfig(CONFIGURACION_DE_COTIZADORES)
        return Scoreador(proveedor_cotizadores=proveedor)

class Tabla(object):
    def __init__(self):
        self._filas = []

        self._definir_filas()

    def filas(self):
        return self._filas

    def _definir_filas(self):
        raise NotImplementedError('responsabilidad de la subclase')


class TablaDeEventos(Tabla):
    def __init__(self, eventos):
        self._eventos = eventos

        super(TablaDeEventos, self).__init__()

    def _definir_filas(self):
        for evento in self._eventos:
            self._filas.append(FilaDeTablaDeEventos.para(evento))


class FilaDeTablaDeEventos(object):
    @classmethod
    def para(cls, evento):
        for subclase in cls.__subclasses__():
            if subclase.acepta(evento):
                return subclase(evento)

        raise Exception('No se puede construir una fila para el evento')

    @classmethod
    def acepta(cls, evento):
        raise NotImplementedError('responsabilidad de la subclase')

    def __init__(self, evento):
        self._evento = evento

    def nombre(self):
        raise NotImplementedError('responsabilidad de la subclase')

    def descripcion(self):
        raise NotImplementedError('responsabilidad de la subclase')


class FilaDeEventoDeZonaPeligrosa(FilaDeTablaDeEventos):
    @classmethod
    def acepta(cls, evento):
        return evento.tipo() == 'ViajeZonaPeligrosa'

    def nombre(self):
        return u'Evento de ingreso a zona peligrosa'

    def descripcion(self):
        zona = self._evento.zona()
        return u'Se ingresó a la zona delimitada por %s y %s' % (
            str(zona.vertice_superior()), str(zona.vertice_inferior()))


class FilaDeEventoDeFrenadaBrusca(FilaDeTablaDeEventos):
    @classmethod
    def acepta(cls, evento):
        return evento.tipo() == 'FrenadaBrusca'

    def nombre(self):
        return u'Evento de frenada brusca'

    def descripcion(self):
        return u''


class TablaDeDetectores(Tabla):
    def __init__(self, configuracion_de_detectores):
        self._configuracion_de_detectores = configuracion_de_detectores
        
        super(TablaDeDetectores, self).__init__()

    def _definir_filas(self):
        for detector in self._configuracion_de_detectores:
            self._filas.append(FilaDeTablaDetectores.para(detector))


class FilaDeTablaDetectores(object):
    @classmethod
    def para(cls, configuracion_de_detector):
        for subclase in cls.__subclasses__():
            if subclase.acepta(configuracion_de_detector):
                return subclase(configuracion_de_detector)

        raise Exception('No se puede construir una fila para el detector de tipo %s' % configuracion_de_detector['tipo'])

    @classmethod
    def acepta(cls, configuracion_de_detector):
        raise NotImplementedError('responsabilidad de la subclase')

    def __init__(self, configuracion_de_detector):
        self._configuracion_de_detector = configuracion_de_detector

    def nombre(self):
        raise NotImplementedError('responsabilidad de la subclase')

    def parametros(self):
        raise NotImplementedError('responsabilidad de la subclase')


class FilaDetectorDeZonaPeligrosa(FilaDeTablaDetectores):
    @classmethod
    def acepta(cls, configuracion_de_detector):
        return configuracion_de_detector['tipo'] == DetectorDeViajeAZonaPeligrosa

    def nombre(self):
        return 'Detector de Viaje a Zona Peligrosa'

    def parametros(self):
        zonas_peligrosas = u'Zonas peligrosas:\n'
        zonas_peligrosas += u'<ul>'

        for zona_peligrosa in self._configuracion_de_detector['parametros']['zonas_peligrosas']:
            zonas_peligrosas += u'<li>Zona definida por %s y %s</li>' % (
                str(zona_peligrosa.vertice_superior()), str(zona_peligrosa.vertice_inferior()))
        zonas_peligrosas += u'</ul>'

        return zonas_peligrosas


class FilaDetectorDeFrenadaBrusca(FilaDeTablaDetectores):
    @classmethod
    def acepta(cls, configuracion_de_detector):
        return configuracion_de_detector['tipo'] == DetectorDeFrenadaBrusca

    def nombre(self):
        return 'Detector de Frenada Brusca'

    def parametros(self):
        limite_de_aceleracion_en_ms2 = self._configuracion_de_detector['parametros']['limite_aceleracion'].a_ms2()
        return u'Límite de aceleración: %s m/s2' % limite_de_aceleracion_en_ms2


class FilaDetectorDeViaje(FilaDeTablaDetectores):
    @classmethod
    def acepta(cls, configuracion_de_detector):
        return configuracion_de_detector['tipo'] == DetectorDeViaje

    def nombre(self):
        return 'Detector de Viaje'

    def parametros(self):
        return u''


class FilaDetectorDeExcesoDeVelocidad(FilaDeTablaDetectores):
    @classmethod
    def acepta(cls, configuracion_de_detector):
        return configuracion_de_detector['tipo'] == DetectorDeExcesoDeVelocidad

    def nombre(self):
        return 'Detector de Exceso de Velocidad'

    def parametros(self):
        return u'Porcentaje máximo de exceso: %s' % str(self._configuracion_de_detector['parametros']['porcentaje_de_velocidad_maxima'])
