from django import forms
from venta.models import *

class TortaForm(forms.ModelForm):
    class Meta:
        model = Torta
        fields = ['nombre', 'ingredientes', 'precio']

class AdicionalForm(forms.ModelForm):
    class Meta:
        model = Adicional
        fields = ['nombre']        