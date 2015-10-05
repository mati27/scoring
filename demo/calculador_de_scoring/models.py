# coding=utf-8
import pickle
from django.db import models

"""
    Objetos usados únicamente para la persistencia.
    NO están relacionados con el modelo de objetos propuesto.
"""
class DeteccionDeEventos(models.Model):
    recorrido = models.FileField(upload_to='recorridos')
    asegurado = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)

    def eventos_detectados(self):
        return self._eventos_detectados.all()

    @classmethod
    def nueva_con(cls, recorrido, asegurado):
        instancia = cls(recorrido=recorrido, asegurado=asegurado)

        instancia.full_clean()
        instancia.save()

        return instancia


class EventoDetectado(models.Model):
    deteccion = models.ForeignKey('DeteccionDeEventos', related_name='_eventos_detectados')
    evento_serializado = models.TextField()

    @classmethod
    def nuevo(cls, deteccion, evento_serializado):
        instancia = cls(deteccion=deteccion, evento_serializado=evento_serializado)

        instancia.full_clean()
        instancia.save()

        return instancia


class PersistidorDeEventos(object):
    def __init__(self, serializador):
        self._serializador = serializador

    def persistir(self, deteccion, evento):

        EventoDetectado.nuevo(deteccion=deteccion, evento_serializado=self._serializador.serializar(evento))


class SerializadorPickle(object):
    def serializar(self, objeto):
        return pickle.dumps(objeto)

    def deserializar(self, objeto_serializado):
        return pickle.loads(objeto_serializado)
