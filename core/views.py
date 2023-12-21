from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.core import serializers

from venta.models import *
from core.forms import *


class Index(View):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        ingredientes = Ingrediente.objects.filter(activo=True)
        tortas = Torta.objects.exclude(ingredientes__activo=False)
        adicionales = Adicional.objects.filter(activo=True)

        max_length = max(len(ingredientes), len(tortas), len(adicionales))

        datos_tabla = []
        for i in range(max_length):
            fila = {
                'ingrediente': ingredientes[i].nombre if i < len(ingredientes) else '',
                'torta': tortas[i].nombre if i < len(tortas) else '',
                'adicional': adicionales[i].nombre if i < len(adicionales) else '',
                'picante': PICANTE[i][1] if i < len(PICANTE) else '',
            }
            datos_tabla.append(fila)

        pedidos_solicitados = Pedido.objects.filter(activo=0)
        pedidos_para_entrega = Pedido.objects.filter(activo=1)

        context = {
            'datos_tabla': datos_tabla,
            'pedidos_solicitados': pedidos_solicitados,
            'pedidos_para_entrega': pedidos_para_entrega,
        }

        return render(request, self.template_name, context)

class Elabora(View):
    template_name = 'core/elabora.html'

    def get(self, request, *args, **kwargs):
        pedidos_solicitados = Pedido.objects.filter(activo=0)
        context = {
            'pedidos_solicitados': pedidos_solicitados,
        }
        return render(request, self.template_name, context)

class Pedir(View):
    template_name = 'core/pedir.html'

    def get(self, request, *args, **kwargs):
        ingredientes = Ingrediente.objects.filter(activo=True)
        tortas = Torta.objects.exclude(ingredientes__activo=False)
        adicionales = Adicional.objects.filter(activo=True)

        max_length = max(len(ingredientes), len(tortas), len(adicionales))

        datos_tabla = []
        for i in range(max_length):
            fila = {
                'ingrediente': ingredientes[i].nombre if i < len(ingredientes) else '',
                'torta': tortas[i].nombre if i < len(tortas) else '',
                'adicional': adicionales[i].nombre if i < len(adicionales) else '',
                'picante': PICANTE[i][1] if i < len(PICANTE) else '',
            }
            datos_tabla.append(fila)

        context = {
            'datos_tabla': datos_tabla,
        }

        return render(request, self.template_name, context)

class Entrega(View):
    template_name = 'core/entrega.html'

    def get(self, request, *args, **kwargs):
        pedidos_para_entrega = Pedido.objects.filter(activo=1)

        context = {
            'pedidos_para_entrega': pedidos_para_entrega,
        }

        return render(request, self.template_name, context)

def nueva_torta(request):
    if request.method == 'POST':
        torta = request.POST['torta']
        cantidad = request.POST['cantidad']
        donde = request.POST['donde']
        picante = request.POST['picante']
        adicionales = request.POST['adicionales']
        pedido = Pedido.objects.create(
            torta=torta,
            cantidad=cantidad,
            donde=donde,
            picante=picante,
            adicionales=adicionales
        )
        pedido.save()
    url = reverse('pedir')
    return redirect(url)

def accion_torta(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        activo = request.POST.get('activo')

        if pk is None or activo is None:
            return JsonResponse({'error': 'Se requieren los parámetros "pk" y "activo"'}, status=400)

        Pedido.objects.filter(id=pk).update(activo=activo)

        if activo == '1' or activo == '9':
            pedidos_solicitados = Pedido.objects.filter(activo=0).values()
            data = {'pedidos_solicitados': list(pedidos_solicitados)}
        else:
            pedidos_para_entrega = Pedido.objects.filter(activo=1).values()
            data = {'pedidos_para_entrega': list(pedidos_para_entrega)}
        
        return JsonResponse(data)

    return JsonResponse({'error': 'No se recibió una solicitud POST'}, status=400)

class IngredienteListView(ListView):
    model = Ingrediente
    template_name = 'core/ingrediente_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context

class IngredienteDetailView(DetailView):
    model = Ingrediente
    template_name = 'core/ingrediente_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context

class IngredienteCreateView(PermissionRequiredMixin, CreateView):
    model = Ingrediente
    template_name = 'core/ingrediente_form.html'
    fields = ['nombre']
    success_url = reverse_lazy('ingrediente_list')
    permission_required = 'core.add_ingrediente'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context

class IngredienteUpdateView(PermissionRequiredMixin, UpdateView):
    model = Ingrediente
    template_name = 'core/ingrediente_form.html'
    fields = ['nombre']
    success_url = reverse_lazy('ingrediente_list')
    permission_required = 'core.change_ingrediente'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context

class IngredienteDeleteView(PermissionRequiredMixin, DeleteView):
    model = Ingrediente
    template_name = 'core/ingrediente_confirm_delete.html'
    success_url = reverse_lazy('ingrediente_list')
    permission_required = 'core.delete_ingrediente'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context

class Catalogo(ListView):
    model = Torta
    template_name = 'core/catalogo.html'
    def get(self, request, *args, **kwargs):
        context = {
            'catalogo': True,
            'tortas': Torta.objects.exclude(nombre=' Ninguna')
        }
        return render(request, self.template_name, context)

class TortaDetailView(DetailView):
    model = Torta
    template_name = 'core/torta_detail.html'
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', '0')
        context = {
            'catalogo': True,
            'tortas': Torta.objects.filter(id=pk).first()
        }
        return render(request, self.template_name, context)

class TortaCreateView(PermissionRequiredMixin, CreateView):
    model = Torta
    template_name = 'core/torta_form.html'
    form_class = TortaForm
    success_url = reverse_lazy('catalogo')
    permission_required = 'core.add_torta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context

class TortaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Torta
    template_name = 'core/torta_form.html'
    form_class = TortaForm
    success_url = reverse_lazy('catalogo')
    permission_required = 'core.update_torta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context

class TortaDeleteView(PermissionRequiredMixin, DeleteView):
    model = Torta
    template_name = 'core/torta_confirm_delete.html'
    success_url = reverse_lazy('catalogo')
    permission_required = 'core.delete_torta'    
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', '0')
        context = {
            'catalogo': True,
            'tortas': Torta.objects.filter(id=pk).first()
        }
        return render(request, self.template_name, context)

class AdicionalListView(PermissionRequiredMixin, ListView):
    model = Adicional
    template_name = 'core/adicional_list.html'
    permission_required = 'core.view_adicional'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context

class AdicionalCreateView(PermissionRequiredMixin, CreateView):
    model = Adicional
    form_class = AdicionalForm
    template_name = 'core/adicional_form.html'
    success_url = reverse_lazy('adicional_list')
    permission_required = 'core.add_adicional'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context

class AdicionalUpdateView(PermissionRequiredMixin, UpdateView):
    model = Adicional
    form_class = AdicionalForm
    template_name = 'core/adicional_form.html'
    success_url = reverse_lazy('adicional_list')
    permission_required = 'core.change_adicional'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context

class AdicionalDeleteView(PermissionRequiredMixin, DeleteView):
    model = Adicional
    template_name = 'core/adicional_confirm_delete.html'
    success_url = reverse_lazy('adicional_list')
    permission_required = 'core.delete_adicional'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context
