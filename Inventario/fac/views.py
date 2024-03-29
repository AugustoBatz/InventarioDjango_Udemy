import Inv.views as inv
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Cliente, FacturaVenta, LoteVenta
from cmp.models import Lote
from django.http import HttpResponse
from Inv.models import Producto
from cmp.reportes import link_callback
from .forms import ClienteForm, FacturaVentaForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Sum
from django.utils import timezone
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.contrib import messages
import datetime

user_id = 0
inicio = 0
final = 0
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


def descarte(cantidad, producto):
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
                cantidad=0, estado=False)
        else:
            cantidad_aux = cantidad_aux[0]['cantidad']-cantidad
            Lote.objects.filter(pk=ids[0]).update(
                cantidad=cantidad_aux)
    else:
        for id in ids:
            cantidad_aux = Lote.objects.filter(pk=id).values('cantidad')
            if(cantidad == cantidad_aux[0]['cantidad']):
                Lote.objects.filter(pk=id).update(
                    cantidad=0, estado=False)
            if(cantidad > cantidad_aux[0]['cantidad']):
                cantidad = cantidad-cantidad_aux[0]['cantidad']
                Lote.objects.filter(pk=id).update(
                    cantidad=0, estado=False)
            if(cantidad < cantidad_aux[0]['cantidad']):
                cantidad_aux = cantidad_aux[0]['cantidad']-cantidad
                Lote.objects.filter(pk=id).update(
                    cantidad=cantidad_aux)

    return lotes_necesarios


class FacturaVentaView(LoginRequiredMixin, generic.ListView):

    model = FacturaVenta
    template_name = "fac/ventas_list.html"
    context_object_name = "obj"
    login_url = "bases:login"


class FacturaVentaView2(LoginRequiredMixin, generic.ListView):
    model = FacturaVenta
    template_name = "fac/ventas_list_report.html"
    context_object_name = "obj"
    login_url = "bases:login"


@login_required(login_url="bases:login")
def reporte_ventas(request):
    global user_id
    global inicio
    global final

    template_name = "fac/ventas_list_report.html"
    ventas = {}
    users = User.objects.all()
    if request.method == 'GET':
        ventas = FacturaVenta.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('rutero')
        inicio = request.POST.get('fecha_inicio')
        final = request.POST.get('fecha_final')
        user_id = int(user_id)
        print(inicio)
        print(final)
        print(user_id)
        if user_id == 0:
            if not inicio and not final:
                print("no inicio y final xd")
                ventas = FacturaVenta.objects.all()
                return render(request, template_name, {'ventas': ventas, 'fecha1': inicio, 'fecha2': final,  'users': users, 'user': user_id, })
            else:
                ventas = FacturaVenta.objects.filter(
                    fecha_compra__range=[inicio, final])
                return render(request, template_name, {'ventas': ventas, 'fecha1': inicio, 'fecha2': final,  'users': users, 'user': user_id, })

        else:
            if not inicio and not final:
                ventas = FacturaVenta.objects.filter(
                    uc=user_id)
                return render(request, template_name, {'ventas': ventas, 'fecha1': inicio, 'fecha2': final, 'users': users, 'user': user_id, })
            else:
                ventas = FacturaVenta.objects.filter(
                    fecha_compra__range=[inicio, final], uc=user_id)
                return render(request, template_name, {'ventas': ventas, 'fecha1': inicio, 'fecha2': final, 'users': users, 'user': user_id, })

    return render(request, template_name, {'ventas': ventas, 'users': users})


@login_required(login_url="bases:login")
def reporte_ventasPDF(request):
    template_path = 'fac/ventas_print.html'
    today = timezone.now()
    compras = {}
    if user_id == 0:
        print("es igual a 0")
        compras = FacturaVenta.objects.filter(
            fecha_compra__range=[inicio, final])
    else:
        compras = FacturaVenta.objects.filter(
            fecha_compra__range=[inicio, final], uc=user_id)

    context = {
        'obj': compras,
        'today': today,
        'request': request
    }
    response = HttpResponse(content_type='application/pdf')
    response['Conten-Diposition'] = 'inline; filename="todas_ventas.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisaStatus = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
        return HttpResponse('Tenemos algun problema <pre>' + html + '</pre>')
    return response


@login_required(login_url="bases:login")
def ventas2(request, facturaventa_id=None):
    print(inicio)
    print(final)
    template_name = "fac/ventas2.html"
    prod = Producto.objects.filter(estado=True)
    form_ventas = {}
    contexto = {}
    clientes = Cliente.objects.filter(estado=True)
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
                    'detalle': det, 'form_enc': form_ventas, 'clientes': clientes, 'source': 'proveedor'}
    if request.method == 'POST':

        fecha_compra = request.POST.get("fecha_compra")
        cliente = request.POST.get("enc_cliente")
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
            e = {
                'fecha_compra': request.POST.get("fecha_compra"),
                'cliente': request.POST.get("enc_cliente"),
                'serie': request.POST.get("serie"),
                'numero': request.POST.get("numero"),
                'cantidad_producto': request.POST.get("cantidad_producto"),
                'total': request.POST.get("total")
            }
            form_ventas = FacturaVentaForm(e)
            if form_ventas.is_valid():
                # if enc:
                enc.save()
                facturaventa_id = enc.id
            else:
                print(form_ventas.errors)
                return render(request, template_name, {'productos': prod, 'form_enc': form_ventas, 'clientes': clientes, 'source': 'proveedor'})

        else:
            enc = FacturaVenta.objects.filter(pk=facturaventa_id).first()
            if enc:
                factura_existe = FacturaVenta.objects.filter(
                    serie=serie, numero=numero)

                if(len(factura_existe) > 1):
                    messages.error(
                        request, "Error al editar, ya esta registrada esta factura")
                    return redirect("fac:ventas_edit", facturaventa_id=facturaventa_id)
                else:
                    enc.fecha_compra = fecha_compra
                    enc.serie = serie
                    enc.numero = numero
                    enc.um = request.user.id
                    enc.save()

        if not facturaventa_id:
            return redirect("fac:ventas_list")

        # producto = request.POST.get("id_id_producto")
        cantidad = request.POST.get("id_cantidad_detalle")
        codigo = request.POST.get("codigo")
        precio = request.POST.get("id_precio_detalle")
        total = request.POST.get("id_total_detalle")
        prod = Producto.objects.get(codigo=codigo)
        disponible = prod.existencia
        metodo=request.POST.get("RD")
        if(metodo=="mercado"):
            if(int(cantidad, 10) > disponible):
                messages.error(request, "No existe stock suficiente")
                return redirect("fac:ventas_edit", facturaventa_id=facturaventa_id)
            else:
                # apartado para lote venta
                lotesV = LoteVenta.objects.filter(producto_id=prod).order_by(
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
                        producto_id=prod, facturaventa_id=facturaventa_id)
                    if existe_lote_producto:
                        messages.error(request, "Producto Ya Registrado")
                    else:
                        det.save()
                        descarte(int(cantidad, 10), prod)
                        total = LoteVenta.objects.filter(
                            facturaventa=facturaventa_id).aggregate(Sum('costo_total'))
                        cantidad = LoteVenta.objects.filter(
                            facturaventa=facturaventa_id).aggregate(Sum('cantidad'))
                        enc.cantidad_producto = cantidad["cantidad__sum"]
                        enc.total = total["costo_total__sum"]
                        enc.save()
                return redirect("fac:ventas_edit", facturaventa_id=facturaventa_id)
                
        else:
            print("no existe metodo")
    return render(request, template_name, contexto)


class ProductoView(inv.ProductoView):
    template_name = "fac/buscarProducto.html"


def cuantoLotes(cantidad, producto):
    ids = []
    aux_cantidad = cantidad
    lotes_necesarios = 0
    precios = 0
    cantidad_en_lote = Lote.objects.filter(
        producto_id=producto, estado=True).order_by('fecha').values('cantidad', 'id')
    while(cantidad > 0):
        cantidad -= cantidad_en_lote[lotes_necesarios]['cantidad']
        ids.append(cantidad_en_lote[lotes_necesarios]['id'])
        lotes_necesarios += 1
    cantidad = aux_cantidad

    if(lotes_necesarios == 1):
        precios = 0
        cantidad_aux = Lote.objects.filter(pk=ids[0]).values('cantidad','precio_unitario')
        if(cantidad == cantidad_aux[0]['cantidad']):
            precio_total = cantidad_aux[0]['cantidad']*cantidad_aux[0]['precio_unitario']
            precios=precios+precio_total
            
            
        else:
            precio_total = cantidad*cantidad_aux[0]['precio_unitario']
            precios=precios+precio_total
    else:
        precios = 0
        print(ids)
        for id in ids:
            print("for "+str(id))
            cantidad_aux = Lote.objects.filter(pk=id).values('cantidad','precio_unitario')
            if(cantidad == cantidad_aux[0]['cantidad']):
                precio_total = cantidad_aux[0]['cantidad']*cantidad_aux[0]['precio_unitario']
                precios=precios+precio_total
                cantidad = cantidad-cantidad_aux[0]['cantidad']
                print("=")
                print("cantidad"+str(cantidad))
                print(precios)
            elif(cantidad > cantidad_aux[0]['cantidad']):
                #cantidad_aux2 = Lote.objects.filter(pk=id).values('cantidad','precio_unitario')
                precio_total = cantidad_aux[0]['cantidad']*cantidad_aux[0]['precio_unitario']
                precios=precios+precio_total
                cantidad = cantidad-cantidad_aux[0]['cantidad']
                print(">")
                print("cantidad"+str(cantidad))
                print(precios)
                #Lote.objects.filter(pk=id).update(
                    #cantidad=0, estado=False)
            elif(cantidad < cantidad_aux[0]['cantidad']):
                precio_total = cantidad*cantidad_aux[0]['precio_unitario']
                precios=precios+precio_total
                print("<")
                print("cantidad"+str(cantidad))
                print(precios)
                #Lote.objects.filter(pk=id).update(
                    #cantidad=cantidad_aux)

    #print(precios)
    return precios


def precio_dinamico(request):
    from django.http import JsonResponse
    codigo = request.GET.get('codigo', None)
    cantidad = request.GET.get('cantidad', None)
    producto = Producto.objects.get(codigo=codigo)
    cantidad_producto = producto.existencia
    data = {}
    if cantidad != '':
        if cantidad_producto < int(cantidad):

            data = {
                'error': "Cantidad Insuficiente en Stock"
            }
        else:
            lotes = cuantoLotes(int(cantidad), producto)
            data = {
                'success': lotes
            }
    return JsonResponse(data)
