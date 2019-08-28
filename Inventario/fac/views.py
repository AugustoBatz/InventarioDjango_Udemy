from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from .models import Cliente, FacturaVenta, LoteVenta
from cmp.models import Lote
from django.http import HttpResponse
from Inv.models import Producto
from .forms import ClienteForm, FacturaVentaForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Sum
from django.contrib import messages
import datetime
# Create your views here.


class ClienteView(LoginRequiredMixin, generic.ListView):
    model = Cliente
    template_name = "fac/clientes_list.html"
    context_object_name = "obj"
    login_url = "bases:login"


class VistaBaseCreate(SuccessMessageMixin, generic.CreateView):
    context_object_name = "obj"
    success_message = "Cliente Nuevo Agregado"

    def form_valid(self, form):

        form.instance.uc = self.request.user
        return super().form_valid(form)


class VistaBaseEdit(SuccessMessageMixin, generic.UpdateView):
    context_object_name = "obj"
    success_message = "Cliente Nuevo Actualizado"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class ClienteNew(VistaBaseCreate):
    model = Cliente
    template_name = "fac/cliente_form.html"
    form_class = ClienteForm
    success_url = reverse_lazy("fac:cliente_list")


class ClienteEdit(VistaBaseEdit):
    model = Cliente
    template_name = "fac/cliente_form.html"
    form_class = ClienteForm
    success_url = reverse_lazy("fac:cliente_list")


@login_required(login_url="/login/")
def clienteInactivar(request, id):
    cliente = Cliente.objects.filter(pk=id).first()
    if request.method == 'POST':
        if cliente:
            cliente.estado = not cliente.estado
            cliente.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    return HttpResponse("FAIL")


@login_required(login_url="bases:login")
def ventas(request, facturaventa_id=None):
    template_name = "fac/ventas.html"
    prod = Producto.objects.filter(estado=True)
    form_ventas = {}
    contexto = {}
    if request.method == 'GET':
        form_ventas = FacturaVentaForm()
        enc = FacturaVenta.objects.filter(pk=facturaventa_id).first()

        if enc:
            det = LoteVenta.objects.filter(facturaventa=enc)
            fecha_compra = datetime.date.isoformat(enc.fecha_compra)
            e = {
                'fecha_compra': fecha_compra,
                'cliente': enc.cliente,
                'serie': enc.serie,
                'numero': enc.numero,
                'cantidad_producto': enc.cantidad_producto,
                'total': enc.total
            }
            form_ventas = FacturaVentaForm(e)
        else:
            det = None
        contexto = {'productos': prod, 'encabezado': enc,
                    'detalle': det, 'form_enc': form_ventas}
    if request.method == 'POST':
        print("entra al POST")
        fecha_compra = request.POST.get("fecha_compra")
        cliente = request.POST.get("cliente")
        serie = request.POST.get("serie")
        numero = request.POST.get("numero")
        total = 0
        cantidad_producto = 0

        if not facturaventa_id:
            clien = Cliente.objects.get(pk=cliente)
            enc = FacturaVenta(
                fecha_compra=fecha_compra,
                serie=serie,
                numero=numero,
                cliente=clien,
                uc=request.user,
                total=total,
                cantidad_producto=cantidad_producto
            )
            if enc:
                enc.save()
                facturaventa_id = enc.id
        else:
            enc = FacturaVenta.objects.filter(pk=facturaventa_id).first()
            if enc:
                enc.fecha_compra = fecha_compra
                enc.serie = serie
                enc.numero = numero
                enc.um = request.user.id
                enc.save()

        if not facturaventa_id:
            return redirect("fac:ventas_list")

        producto = request.POST.get("id_id_producto")
        cantidad = request.POST.get("id_cantidad_detalle")
        precio = request.POST.get("id_precio_detalle")
        total = request.POST.get("id_total_detalle")
        prod = Producto.objects.get(pk=producto)
        disponible = prod.existencia
        if(int(cantidad, 10) > disponible):
            messages.error(request, "No existe stock suficiente")
            return redirect("fac:ventas_edit", facturaventa_id=facturaventa_id)
        else:
            # apartado para lote venta
            lotesV = LoteVenta.objects.filter(producto_id=producto).order_by(
                '-noLote').values('noLote')[:1]
            noLote = 1
            if lotesV:
                noLote = lotesV[0]
                noLote = noLote['noLote']
                noLote = noLote+1
            det = LoteVenta(
                facturaventa=enc,
                producto=prod,
                cantidad=cantidad,
                costo_unitario=precio,
                costo_total=total,
                uc=request.user,
                fecha=fecha_compra,
                noLote=noLote
            )
            if det:
                existe_lote_producto = LoteVenta.objects.filter(
                    producto_id=producto, facturaventa_id=facturaventa_id)
                if existe_lote_producto:
                    messages.error(request, "Producto Ya Registrado")
                else:
                    det.save()
                    descarte(int(cantidad, 10), producto, det.id)
                    total = LoteVenta.objects.filter(
                        facturaventa=facturaventa_id).aggregate(Sum('costo_total'))
                    cantidad = LoteVenta.objects.filter(
                        facturaventa=facturaventa_id).aggregate(Sum('cantidad'))
                    enc.cantidad_producto = cantidad["cantidad__sum"]
                    enc.total = total["costo_total__sum"]
                    enc.save()
            return redirect("fac:ventas_edit", facturaventa_id=facturaventa_id)

        # desde aqui el metodo peps

    return render(request, template_name, contexto)


def descarte(cantidad, producto, det):
    cantidad_aux = cantidad
    lotes_necesarios = 0
    ids = []
    cantidad_en_lote = Lote.objects.filter(
        producto_id=producto, estado=True).order_by('fecha').values('cantidad', 'id')
    while(cantidad > 0):
        cantidad -= cantidad_en_lote[lotes_necesarios]['cantidad']
        ids.append(cantidad_en_lote[lotes_necesarios]['id'])
        lotes_necesarios += 1
    cantidad = cantidad_aux
    if(lotes_necesarios == 1):
        cantidad_aux = Lote.objects.filter(pk=ids[0]).values('cantidad')
        if(cantidad == cantidad_aux[0]['cantidad']):
            Lote.objects.filter(pk=ids[0]).update(
                cantidad=0, estado=False, loteventa_id=det)
        else:
            cantidad_aux = cantidad_aux[0]['cantidad']-cantidad
            Lote.objects.filter(pk=ids[0]).update(
                cantidad=cantidad_aux,  loteventa_id=det)
    else:
        for id in ids:
            cantidad_aux = Lote.objects.filter(pk=id).values('cantidad')
            if(cantidad == cantidad_aux[0]['cantidad']):
                Lote.objects.filter(pk=id).update(
                    cantidad=0, estado=False,  loteventa_id=det)
            if(cantidad > cantidad_aux[0]['cantidad']):
                cantidad = cantidad-cantidad_aux[0]['cantidad']
                Lote.objects.filter(pk=id).update(
                    cantidad=0, estado=False, loteventa_id=det)
            if(cantidad < cantidad_aux[0]['cantidad']):
                cantidad_aux = cantidad_aux[0]['cantidad']-cantidad
                Lote.objects.filter(pk=id).update(
                    cantidad=cantidad_aux, loteventa_id=det)

    return lotes_necesarios


class FacturaVentaView(LoginRequiredMixin, generic.ListView):
    model = FacturaVenta
    template_name = "fac/ventas_list.html"
    context_object_name = "obj"
    login_url = "bases:login"
