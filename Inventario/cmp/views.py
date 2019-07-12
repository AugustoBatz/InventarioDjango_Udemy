from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Proveedor, FacturaCompra, Lote
from cmp.forms import ProveedorForm, FacturaCompraForm
from django.http import HttpResponse
from Inv.models import Producto
import json

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


def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Producto.objects.filter(name__startswith=q)
        results = []
        print(q)
        for r in search_qs:
            results.append(r.FIELD)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required(login_url="bases:login")
def compras(request, compra_id=None):
    template_name = "cmp/compras.html"
    prod = Producto.objects.filter(estado=True)
    form_compras = {}

    contexto = {}

    if request.method == 'GET':
        form_compras = FacturaCompraForm()
        enc = FacturaCompra.objects.filter(pk=compra_id).first()

        if enc:
            det = Lote.Objtects.filter(compras=enc)
            fecha_compra = datetime.date.isoformat(enc.fecha_compra)
            e = {
                'fecha_compra': fecha_compra,
                'proveedor': enc.proveedor,
                'serie': enc.serie,
                'numero': enc.numero,
                'cantidad_producto': enc.cantidad_producto,
                'total': enc.total
            }
            form_compras = FacturaCompra(e)
        else:
            det = None
        context = {'productos': prod, 'encabezado': enc,
                   'detelle': det, 'form_enc': form_compras}

        return render(request, template_name, context)
