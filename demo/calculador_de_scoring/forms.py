from django import forms
from configuracion import ASEGURADOS


class FormularioDeDeteccionDeEventos(forms.Form):
    recorrido = forms.FileField()
    asegurado = forms.ChoiceField(
        choices=[(asegurado.nombre(), asegurado.nombre()) for asegurado in ASEGURADOS])
