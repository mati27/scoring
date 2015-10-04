# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeteccionDeEventos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recorrido', models.FileField(upload_to=b'recorridos')),
                ('asegurado', models.CharField(max_length=255)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventoDetectado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('evento_serializado', models.TextField()),
                ('deteccion', models.ForeignKey(related_name='_eventos_detectados', to='calculador_de_scoring.DeteccionDeEventos')),
            ],
        ),
    ]
