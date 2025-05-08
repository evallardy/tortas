from django.conf import settings
from django.views import View
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView,TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.core import serializers
from django.db import transaction
from django.views.decorators.http import require_POST
from django.db.models import Sum
from django.utils.timezone import localdate
from django.contrib.auth.mixins import LoginRequiredMixin
import qrcode
import base64
import secrets
from io import BytesIO

from venta.models import *
from core.forms import *

class PresentaQRView(View):
    def get(self, request, *args, **kwargs):
        # Busca token
        contenido = get_object_or_404(Llave, activo=1)

        # Genera el código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_data = f'{settings.SITE_URL}/solicitar/{contenido.token}/'  # URL del curso
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill='black', back_color='white')

        # Guarda la imagen en un objeto BytesIO
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        # Codifica la imagen a base64
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        img_url = f"data:image/png;base64,{img_base64}"

        return render(request, 'core/mostrar_qr.html', {
            'qr_url': img_url
        })

class SolicitarTortaView(View):
    template_name = 'core/pideCliente.html'

    def get(self, request, *args, **kwargs):
        tortas = Torta.objects.exclude(ingredientes__activo=False).order_by('nombre')
        ingredientes = Ingrediente.objects.filter(activo=True).order_by('nombre')
        adicionales = Adicional.objects.filter(activo=True).order_by('nombre')
        precioingredientes = PrecioTortasIngredientes.objects.filter(activo=True)

        context = {
            'tortas': tortas,
            'ingredientes': ingredientes,
            'adicionales': adicionales,
            'precioingredientes': precioingredientes,
        }

        return render(request, self.template_name, context)
    
    def post(self, request):
        tortas = request.POST.getlist('torta[]')
        valores = request.POST.getlist('valor[]')
        nombre = request.POST.get('nombre')

        
        with transaction.atomic():
            for torta, valor in zip(tortas, valores):
                valorNumerico = valor.replace(',','')
                partes = torta.split('-')
                cantidad = partes[0].strip()
                nuevo_pedido = Pedido.objects.create(
                    nombre=nombre,
                    cantidad=cantidad,
                    solicitud=torta,
                    precio=valorNumerico,
                    activo=1,
                )
                # Aquí puedes guardar en la base de datos si es necesario

        return redirect('pide_cliente')    
    
def tortas_pago(request, pk):
    tortas = Pedido.objects.filter(pago=pk).values('cantidad', 'solicitud', 'precio')
    lista = list(tortas)
    return JsonResponse(lista, safe=False)

class ReportePagosView(TemplateView):
    template_name = 'core/reporte_pagos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener todas las fechas únicas del campo created
        fechas = Pagos.objects.dates('created', 'day', order='DESC')

        tiene_pagos = False

        if fechas:
            
            tiene_pagos = True
            
            context['fechas'] = fechas

            # Obtener fecha seleccionada por GET o usar la más reciente
            fecha_seleccionada = self.request.GET.get('fecha')
            if fecha_seleccionada:
                registros = Pagos.objects.filter(created__date=fecha_seleccionada)
            elif fechas:
                fecha_seleccionada = fechas[0].strftime('%Y-%m-%d')
                registros = Pagos.objects.filter(created__date=fecha_seleccionada)
            else:
                registros = []

            context['fecha_seleccionada'] = fecha_seleccionada
            context['registros'] = registros
            context['total_importe_real'] = registros.aggregate(total=Sum('importe_real'))['total'] or 0
            context['total_importe'] = registros.aggregate(total=Sum('importe'))['total'] or 0
            context['total_tortas'] = registros.aggregate(total=Sum('cantidad_torta'))['total'] or 0
        context['tiene_pagos'] = tiene_pagos
        return context

class PrecioTortasListView(ListView):
    model = PrecioTortasIngredientes
    template_name = 'core/precio_torta_ingrediente_list.html'
    context_object_name = 'precios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context

class PrecioTortasCreateView(CreateView):
    model = PrecioTortasIngredientes
    form_class = PrecioTortasIngredientesForm
    template_name = 'core/precio_torta_ingrediente_form.html'
    success_url = reverse_lazy('precio_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context

class PrecioTortasUpdateView(UpdateView):
    model = PrecioTortasIngredientes
    form_class = PrecioTortasIngredientesForm
    template_name = 'core/precio_torta_ingrediente_form.html'
    success_url = reverse_lazy('precio_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context

class PrecioTortasDeleteView(DeleteView):
    model = PrecioTortasIngredientes
    template_name = 'core/precio_torta_ingrediente_delete.html'
    success_url = reverse_lazy('precio_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context

class Index(View):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        llave = Llave.objects.first()
        if not llave:
            llave = Llave.objects.create()

        ingredientes = Ingrediente.objects.filter(activo=True)
        tortas = Torta.objects.exclude(ingredientes__activo=False)
        adicionales = Adicional.objects.filter(activo=True)

        max_length = max(len(ingredientes), len(tortas), len(adicionales))

        datos_tabla = []
        for i in range(max_length):
            picante_texto = PICANTE[i][1].replace(' ','')
            picante = picante_texto if i < len(PICANTE) else ''
            fila = {
                'ingrediente': ingredientes[i].nombre if i < len(ingredientes) else '',
                'torta': tortas[i].nombre if i < len(tortas) else '',
                'adicional': adicionales[i].nombre if i < len(adicionales) else '',
                'picante': picante, 
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

def tortas(pedidos):
    tortas = []
    for pedido in pedidos:
        nombre = pedido.nombre
        solicitud = pedido.solicitud
        precio = pedido.precio
        id = pedido.id

        # Primero separamos por guion
        partes_guion = solicitud.split('-')

        cantidad = partes_guion[0].strip()

        resto = partes_guion[1].strip()

        columnas = [x.strip() for x in resto.split('/')]

        contenido = columnas[0]

        if "PICANTE" in columnas[1]:
            adicional = 'SIN Condimentos'
            picante = columnas[1]
            para = columnas[2]
        else:
            adicional = columnas[1]
            picante = columnas[2]
            para = columnas[3]

        torta = {
            "id": id,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio,
            "contenido": contenido,
            "adicional": adicional,
            "picante": picante,
            "para": para,
        }

        tortas.append(torta)

    return tortas

class Elabora(View):
    template_name = 'core/elabora.html'

    def get(self, request, *args, **kwargs):
        llave = Llave.objects.first()
        if not llave:
            llave = Llave.objects.create()

        pedidos = Pedido.objects.filter(activo=1).order_by('modified')

        context = {
            'pedidos_solicitados': pedidos,
            'tortas': tortas(pedidos),
        }
        return render(request, self.template_name, context)

class PideNegocio(View):
    template_name = 'core/pideNegocio.html'

    def get(self, request, *args, **kwargs):
        tortas = Torta.objects.exclude(ingredientes__activo=False).order_by('nombre')
        ingredientes = Ingrediente.objects.filter(activo=True).order_by('nombre')
        adicionales = Adicional.objects.filter(activo=True).order_by('nombre')
        precioingredientes = PrecioTortasIngredientes.objects.filter(activo=True)

        context = {
            'tortas': tortas,
            'ingredientes': ingredientes,
            'adicionales': adicionales,
            'precioingredientes': precioingredientes,
        }

        return render(request, self.template_name, context)
    
    def post(self, request):
        tortas = request.POST.getlist('torta[]')
        valores = request.POST.getlist('valor[]')
        nombre = request.POST.get('nombre')

        
        with transaction.atomic():
            for torta, valor in zip(tortas, valores):
                valorNumerico = valor.replace(',','')
                partes = torta.split('-')
                cantidad = partes[0].strip()
                nuevo_pedido = Pedido.objects.create(
                    nombre=nombre,
                    cantidad=cantidad,
                    solicitud=torta,
                    precio=valorNumerico,
                    activo=1,
                )
                # Aquí puedes guardar en la base de datos si es necesario

        return redirect('pide_negocio')    


class PideCliente(View):
    template_name = 'core/pideCliente.html'

    def get(self, request, *args, **kwargs):
        tortas = Torta.objects.exclude(ingredientes__activo=False).order_by('nombre')
        ingredientes = Ingrediente.objects.filter(activo=True).order_by('nombre')
        adicionales = Adicional.objects.filter(activo=True).order_by('nombre')
        precioingredientes = PrecioTortasIngredientes.objects.filter(activo=True)

        context = {
            'tortas': tortas,
            'ingredientes': ingredientes,
            'adicionales': adicionales,
            'precioingredientes': precioingredientes,
        }

        return render(request, self.template_name, context)
    
    def post(self, request):
        tortas = request.POST.getlist('torta[]')
        valores = request.POST.getlist('valor[]')
        nombre = request.POST.get('nombre')

        
        with transaction.atomic():
            for torta, valor in zip(tortas, valores):
                valorNumerico = valor.replace(',','')
                partes = torta.split('-')
                cantidad = partes[0].strip()
                nuevo_pedido = Pedido.objects.create(
                    nombre=nombre,
                    cantidad=cantidad,
                    solicitud=torta,
                    precio=valorNumerico,
                    activo=1,
                )
                # Aquí puedes guardar en la base de datos si es necesario

        return redirect('pide_cliente')    

def ingredientes_torta(request, pk):
    torta = Torta.objects.get(pk=pk)
    ingredientes = torta.ingredientes.filter(activo=True).values('nombre', 'tipo')
    return JsonResponse(list(ingredientes), safe=False)

class VerificaCliente(View):
    template_name = 'core/verificaCliente.html'

    def get(self, request, *args, **kwargs):
        pedidos = Pedido.objects.filter(activo=0).order_by('modified')

        context = {
            'pedidos': pedidos,
        }

        return render(request, self.template_name, context)
    
    def post(self, request):
        tortas = request.POST.getlist('torta[]')
        valores = request.POST.getlist('valor[]')
        nombre = request.POST.get('nombre')

        
        with transaction.atomic():
            for torta, valor in zip(tortas, valores):
                valorNumerico = valor.replace(',','')
                nuevo_pedido = Pedido.objects.create(
                    nombre=nombre,
                    solicitud=torta,
                    precio=valorNumerico,
                    activo=1
                )
                # Aquí puedes guardar en la base de datos si es necesario

        return redirect('pide_cliente')    
    
@require_POST
def eliminaPedido(request):
    pk = request.POST.get('pk')
    if pk:
        eliminado = Pedido.objects.filter(id=pk).delete()

    return redirect(reverse('verifica_cliente'))

@require_POST
def confirmadoPedido(request):
    pk = request.POST.get('pk')
    if pk:
        pedido = Pedido.objects.get(id=pk)
        pedido.activo = 1
        pedido.save()

    return redirect(reverse('verifica_cliente'))

class Entrega(View):
    template_name = 'core/entrega.html'

    def get(self, request, *args, **kwargs):
        pedidos_para_entrega = Pedido.objects.filter(activo=2).order_by('modified')

        context = {
            'pedidos_para_entrega': pedidos_para_entrega,
            'tortas': tortas(pedidos_para_entrega)
        }

        return render(request, self.template_name, context)

def paga_torta(request):
    if request.method == 'POST':
        pagos = request.POST.getlist('pago')
        importe = request.POST['importe']

        with transaction.atomic():
            pago = Pagos.objects.create(
                importe_real=importe,
            )

            cantidad_total = 0
            pago_total = 0

            for item in pagos:
                clave, paga, cantidad = item.split('|')

                pedido = Pedido.objects.get(id=clave)
                pedido.activo = 3
                pedido.pago = pago
                pedido.save()

                cantidad_total += int(cantidad)
                pago_total += float(paga)

            
            pago.cantidad_torta = cantidad_total
            pago.importe = pago_total

            pago.save()


    url = reverse('entrega')
    return redirect(url)

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

#        Pedido.objects.filter(id=pk).update(activo=activo)

        pedido = Pedido.objects.get(id=pk)
        pedido.activo = activo
        pedido.save()

        if activo == '2' or activo == '9':
            pedidos_solicitados = Pedido.objects.filter(activo=1).values()
            data = {'pedidos_solicitados': list(pedidos_solicitados),}
        else:
            if activo == '3' or activo == '10':
                pedidos_para_entrega = Pedido.objects.filter(activo=2).values()
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
    form_class = IngredienteForm
    success_url = reverse_lazy('ingrediente_list')
    permission_required = 'core.add_ingrediente'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = True
        return context

class IngredienteUpdateView(PermissionRequiredMixin, UpdateView):
    model = Ingrediente
    template_name = 'core/ingrediente_form.html'
    form_class = IngredienteForm
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
