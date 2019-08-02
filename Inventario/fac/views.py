from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from .models import Cliente
from django.http import HttpResponse
from .forms import ClienteForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
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
