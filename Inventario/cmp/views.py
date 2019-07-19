from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Proveedor, FacturaCompra, Lote
from cmp.forms import ProveedorForm, FacturaCompraForm
from django.http import HttpResponse
from Inv.models import Producto
from django.db.models import Sum
from dal import autocomplete
import json
from django.db.models import Q
from django.contrib import messages
# Create your views here.


class ProveedorView(LoginRequiredMixin, generic.ListView):
    model = Proveedor
    template_name = "cmp/proveedor_list.html"
    context_object_name = "obj"
    login_url = "bases:login"


class ProveedorNew(LoginRequiredMixin, generic.CreateView):
    model = Proveedor
    template_name = "cmp/proveedor_form.html"
    context_object_name = "obj"
    form_class = ProveedorForm
    success_url = reverse_lazy("cmp:proveedor_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class ProveedorEdit(LoginRequiredMixin, generic.UpdateView):
    model = Proveedor
    template_name = "cmp/proveedor_form.html"
    context_object_name = "obj"
    form_class = ProveedorForm
    success_url = reverse_lazy("cmp:proveedor_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


def proveedorInactivar(request, id):
    template_name = "cmp/proveedor_inactivar.html"
    context = {}
    prv = Proveedor.objects.filter(pk=id).first()
    if not prv:
        return HttpResponse('Proveedor no existe '+str(id))

    if request.method == 'GET':
        context = {'obj': prv}

    if request.method == 'POST':
        prv.estado = False
        prv.save()
        context = {'obj': 'OK'}
        return HttpResponse('Proveedor Inactivo')

    return render(request, template_name, context)


class FacturaCompraView(LoginRequiredMixin, generic.ListView):
    model = FacturaCompra
    template_name = "cmp/compras_list.html"
    context_object_name = "obj"
    login_url = "bases:login"


@login_required(login_url="bases:login")
def compras(request, facturacompra_id=None):
    template_name = "cmp/compras.html"
    prod = Producto.objects.filter(estado=True)
    form_compras = {}

    contexto = {}

    if request.method == 'GET':
        form_compras = FacturaCompraForm()
        enc = FacturaCompra.objects.filter(pk=facturacompra_id).first()

        if enc:
            det = Lote.objects.filter(facturacompra=enc)
            fecha_compra = datetime.date.isoformat(enc.fecha_compra)
            e = {
                'fecha_compra': fecha_compra,
                'proveedor': enc.proveedor,
                'serie': enc.serie,
                'numero': enc.numero,
                'cantidad_producto': enc.cantidad_producto,
                'total': enc.total
            }
            form_compras = FacturaCompraForm(e)
        else:
            det = None
        context = {'productos': prod, 'encabezado': enc,
                   'detalle': det, 'form_enc': form_compras}
    if request.method == 'POST':
        fecha_compra = request.POST.get("fecha_compra")
        proveedor = request.POST.get("proveedor")
        serie = request.POST.get("serie")
        numero = request.POST.get("numero")
        total = 0
        cantidad_producto = 0
        # print("marcador")
        if not facturacompra_id:
            print("entra al ifnot compra id")
            prov = Proveedor.objects.get(pk=proveedor)
            enc = FacturaCompra(
                fecha_compra=fecha_compra,
                serie=serie,
                numero=numero,
                proveedor=prov,
                uc=request.user,
                total=total,
                cantidad_producto=cantidad_producto
            )
            if enc:
                print("entra al save")
                enc.save()
                facturacompra_id = enc.id
            print("sale del if")

        else:
            print("entra else")
            enc = FacturaCompra.objects.filter(pk=facturacompra_id).first()
            if enc:
                enc.fecha_compra = fecha_compra
                enc.serie = serie
                enc.numero = numero
                enc.um = request.user.id
                enc.save()
        if not facturacompra_id:
            return redirect("cmp:compras_list")

        producto = request.POST.get("id_id_producto")
        cantidad = request.POST.get("id_cantidad_detalle")
        precio = request.POST.get("id_precio_detalle")
        total = request.POST.get("id_total_detalle")
        print("total 2"+str(total))
        prod = Producto.objects.get(pk=producto)
        Lotes = Lote.objects.filter(producto_id=producto).order_by(
            '-noLote').values('noLote')[:1]
        noLote = 1
        if Lotes:
            noLote = Lotes[0]
            noLote = noLote['noLote']
            noLote = noLote+1

        det = Lote(
            facturacompra=enc,
            producto=prod,
            cantidad=cantidad,
            costo_unitario=precio,
            costo_total=total,
            uc=request.user,
            fecha=fecha_compra,
            noLote=noLote
        )
        if det:
            existe_lote_producto = Lote.objects.filter(
                producto_id=producto, facturacompra_id=facturacompra_id)
            if existe_lote_producto:
                print("este producto ya esta registrado")
                messages.error(request, "Producto Ya Registrado")
            else:
                det.save()
                total = Lote.objects.filter(
                    facturacompra=facturacompra_id).aggregate(Sum('costo_total'))
                cantidad = Lote.objects.filter(
                    facturacompra=facturacompra_id).aggregate(Sum('cantidad'))
                enc.cantidad_producto = cantidad["cantidad__sum"]
                enc.total = total["costo_total__sum"]
                enc.save()
        return redirect("cmp:compras_edit", facturacompra_id=facturacompra_id)

    return render(request, template_name, context)


class CompraDetDelete(generic.DeleteView):
    model = Lote
    template_name = "cmp/compras_det_del.html"
    context_object_name = 'obj'

    def get_success_url(self):
        facturacompra_id = self.kwargs['facturacompra_id']
        return reverse_lazy('cmp:compras_edit', kwargs={'facturacompra_id': facturacompra_id})
