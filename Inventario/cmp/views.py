from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from .models import Proveedor, FacturaCompra, Lote, Registro_Lote
from cmp.forms import ProveedorForm, FacturaCompraForm
from django.http import HttpResponse
from Inv.models import Producto
import Inv.views as inv
from django.db.models import Sum
from dal import autocomplete
import json
from django.db.models import Q
from django.contrib import messages

# Create your views here.


class ProveedorView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'cmp.can_mark_returned'
    model = Proveedor
    template_name = "cmp/proveedor_list.html"
    context_object_name = "obj"
    login_url = "bases:login"


class ProveedorNew(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cmp.can_mark_returned'
    model = Proveedor
    template_name = "cmp/proveedor_form.html"
    context_object_name = "obj"
    form_class = ProveedorForm
    success_url = reverse_lazy("cmp:proveedor_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class ProveedorEdit(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cmp.can_mark_returned'
    model = Proveedor
    template_name = "cmp/proveedor_form.html"
    context_object_name = "obj"
    form_class = ProveedorForm
    success_url = reverse_lazy("cmp:proveedor_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


@login_required(login_url="bases:login")
def anularCompra(request, id):
    template_name = "cmp/anularFac.html"
    context = {}
    enc = FacturaCompra.objects.filter(pk=id).first()
    det = Registro_Lote.objects.filter(facturacompra_id=id)
    reg = Lote.objects.filter(facturacompra_id=id)
    if not enc:
        return HttpResponse('Proveedor no existe '+str(id))
    if request.method == 'GET':
        context = {'obj': enc}
    if request.method == 'POST':
        validacion = True
        for x in reg:
            if x.cantidad != x.cantidad_inicial:
                validacion = False

        if validacion == False:
            #messages.error(request, "No se puede Anular esta Factura")
            # return render(request, template_name, context)
            return HttpResponse('No se puede Anular esta Factura')

        else:
            for x in det:
                x.estado = False
                x.save()
            for x in reg:
                x.estado = False
                x.save()
            enc.estado = False
            enc.save()

        context = {'obj': 'OK'}
        #messages.error(request, "Factura Anulada")
        return HttpResponse('Factura Anulada')

    return render(request, template_name, context)


@permission_required('cmp.can_mark_returned')
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


class FacturaCompraView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'cmp.can_mark_returned'
    model = FacturaCompra
    template_name = "cmp/compras_list.html"
    context_object_name = "obj"
    login_url = "bases:login"


@login_required(login_url="bases:login")
def compras(request, facturacompra_id=None):
    template_name = "cmp/compras.html"
    prod = Producto.objects.filter(estado=True)
    form_compras = {}
    proveedores = Proveedor.objects.filter(estado=True)
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
        contexto = {'productos': prod, 'encabezado': enc,
                    'detalle': det, 'form_enc': form_compras, 'proveedores': proveedores}
    if request.method == 'POST':

        fecha_compra = request.POST.get("fecha_compra")
        proveedor = request.POST.get("enc_proveedor")
        serie = request.POST.get("serie")
        numero = request.POST.get("numero")
        total = 0
        cantidad_producto = 0
        if not facturacompra_id:
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
            e = {
                'fecha_compra': request.POST.get("fecha_compra"),
                'proveedor': request.POST.get("enc_proveedor"),
                'serie': request.POST.get("serie"),
                'numero': request.POST.get("numero"),
                'cantidad_producto': request.POST.get("cantidad_producto"),
                'total': request.POST.get("total"),
            }
            form_compras = FacturaCompraForm(e)
            form_compras.instance.uc = request.user
            if form_compras.is_valid():
                enc.save()
                facturacompra_id = enc.id
            else:
                return render(request, template_name, {'productos': prod,
                                                       'form_enc': form_compras, 'proveedores': proveedores})

        else:
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
        registro = Lote(
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
                messages.error(request, "Producto Ya Registrado")
            else:
                det.save()
                print("despues del save al detalle")
                total = Lote.objects.filter(
                    facturacompra=facturacompra_id).aggregate(Sum('costo_total'))
                cantidad = Lote.objects.filter(
                    facturacompra=facturacompra_id).aggregate(Sum('cantidad'))
                enc.cantidad_producto = cantidad["cantidad__sum"]
                enc.total = total["costo_total__sum"]
                enc.save()
        return redirect("cmp:compras_edit", facturacompra_id=facturacompra_id)

    return render(request, template_name, contexto)


class CompraDetDelete(generic.DeleteView, PermissionRequiredMixin):
    permission_required = 'cmp.can_mark_returned'
    model = Registro_Lote
    template_name = "cmp/compras_det_del.html"
    context_object_name = 'obj'

    def get_success_url(self):
        facturacompra_id = self.kwargs['facturacompra_id']
        return reverse_lazy('cmp:compras_edit', kwargs={'facturacompra_id': facturacompra_id})


@login_required(login_url="bases:login")
def compras2(request, facturacompra_id=None):
    template_name = 'cmp/comprasV2.html'
    prod = Producto.objects.filter(estado=True)
    form_compras = {}
    proveedores = Proveedor.objects.filter(estado=True)
    contexto = {}
    if request.method == 'GET':
        form_compras = FacturaCompraForm()
        enc = FacturaCompra.objects.filter(pk=facturacompra_id).first()

        if enc:
            det = Registro_Lote.objects.filter(facturacompra=enc)
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
        contexto = {'productos': prod, 'encabezado': enc,
                    'detalle': det, 'form_enc': form_compras, 'proveedores': proveedores, 'source': 'proveedor'}
    if request.method == 'POST':

        fecha_compra = request.POST.get("fecha_compra")
        proveedor = request.POST.get("enc_proveedor")
        serie = request.POST.get("serie")
        numero = request.POST.get("numero")
        total = 0
        cantidad_producto = 0

        if not facturacompra_id:
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
            e = {
                'fecha_compra': request.POST.get("fecha_compra"),
                'proveedor': request.POST.get("enc_proveedor"),
                'serie': request.POST.get("serie"),
                'numero': request.POST.get("numero"),
                'cantidad_producto': request.POST.get("cantidad_producto"),
                'total': request.POST.get("total")
            }
            form_compras = FacturaCompraForm(e)
            if form_compras.is_valid():
                # if enc:
                enc.save()
                facturacompra_id = enc.id
            else:
                return render(request, template_name, {'productos': prod, 'form_enc': form_compras, 'proveedores': proveedores, 'source': 'proveedor'})

        else:
            enc = FacturaCompra.objects.filter(pk=facturacompra_id).first()
            if enc:
                enc.fecha_compra = fecha_compra
                enc.serie = serie
                enc.numero = numero
                enc.um = request.user.id
                enc.save()
        if not facturacompra_id and var_return == True:
            return redirect("cmp:compras_list")

        codigo = request.POST.get("codigo")
        cantidad = request.POST.get("id_cantidad_detalle")
        precio = request.POST.get("id_precio_detalle")
        total = request.POST.get("id_total_detalle")
        print(codigo)
        prod = Producto.objects.get(codigo=codigo)
        print(prod)
        Lotes = Lote.objects.filter(producto_id=prod).order_by(
            '-noLote').values('noLote')[:1]
        noLote = 1
        if Lotes:
            noLote = Lotes[0]
            noLote = noLote['noLote']
            noLote = noLote+1

        print("crear el detalle ante del save")
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
        registro = Registro_Lote(
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
                producto_id=prod, facturacompra_id=facturacompra_id)
            if existe_lote_producto:
                messages.error(request, "Producto Ya Registrado")
            else:
                factura_existe = FacturaCompra.objects.filter(
                    serie=serie, numero=numero)

                if(len(factura_existe) > 1):
                    messages.error(request, "Factura Ya registrada")
                else:
                    registro.save()
                    det.save()
                    total = Lote.objects.filter(
                        facturacompra=facturacompra_id).aggregate(Sum('costo_total'))
                    cantidad = Lote.objects.filter(
                        facturacompra=facturacompra_id).aggregate(Sum('cantidad'))
                    enc.cantidad_producto = cantidad["cantidad__sum"]
                    enc.total = total["costo_total__sum"]
                    enc.save()
        return redirect("cmp:compras_edit", facturacompra_id=facturacompra_id)
    return render(request, template_name, contexto)


class ProductoView(inv.ProductoView, PermissionRequiredMixin):
    permission_required = 'cmp.can_mark_returned'
    template_name = "cmp/buscarProducto.html"
