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

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre','tipo','precio']      
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }          

class PrecioTortasIngredientesForm(forms.ModelForm):
    class Meta:
        model = PrecioTortasIngredientes
        fields = ['especial', 'normal', 'precio']
        widgets = {
            'especial': forms.NumberInput(attrs={'class': 'form-control'}),
            'normal': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '1.00'}),
        }
        labels = {
            'especial': 'Cantidad Especial',
            'normal': 'Cantidad Normal',
            'precio': 'Precio Total',
        }        