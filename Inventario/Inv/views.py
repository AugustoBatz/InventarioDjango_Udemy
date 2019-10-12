from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Categoria, SubCategoria, Marca, UnidadMedida, Producto
from .forms import CategoriaForm, SubCategoriaForm, MarcaForm, UnidadMedidaForm, ProductoForm
from cmp.models import Lote
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError

# Create your views here.


class CategoriaView(LoginRequiredMixin, generic.ListView):
    model = Categoria
    template_name = "inv/categoria_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'


class CategoriaNew(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model = Categoria
    template_name = "inv/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    login_url = 'bases:login'
    success_url = reverse_lazy('inv:categoria_list')
    success_message = "Categoria creada satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class CategoriaEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Categoria
    template_name = "inv/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    login_url = 'bases:login'
    success_url = reverse_lazy('inv:categoria_list')
    success_message = "Categoria Editada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class SubCategoriaEdit(LoginRequiredMixin, generic.UpdateView):
    model = SubCategoria
    template_name = "inv/subcategoria_form.html"
    context_object_name = "obj"
    form_class = SubCategoriaForm
    login_url = 'bases:login'
    success_url = reverse_lazy('inv:subcategoria_list')

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        try:
            return super(SubCategoriaEdit, self).form_valid(form)
        except IntegrityError:
            form.add_error('categoria', 'Ya existe este registro')
            return self.form_invalid(form)


class SubCategoriaView(LoginRequiredMixin, generic.ListView):
    model = SubCategoria
    template_name = "inv/subcategoria_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'


class SubCategoriaNew(LoginRequiredMixin, generic.CreateView):
    model = SubCategoria
    template_name = "inv/subcategoria_form.html"
    context_object_name = "obj"
    form_class = SubCategoriaForm
    login_url = 'bases:login'
    success_url = reverse_lazy('inv:subcategoria_list')

    def form_valid(self, form):
        form.instance.uc = self.request.user
        try:
            return super(SubCategoriaNew, self).form_valid(form)
        except IntegrityError:
            form.add_error('categoria', 'Ya existe este registro')
            return self.form_invalid(form)


class MarcaView(LoginRequiredMixin, generic.ListView):
    model = Marca
    template_name = "inv/marca_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'


class MarcaNew(LoginRequiredMixin, generic.CreateView):
    model = Marca
    template_name = "inv/marca_form.html"
    context_object_name = "obj"
    form_class = MarcaForm
    login_url = 'bases:login'
    success_url = reverse_lazy('inv:marca_list')

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class MarcaEdit(LoginRequiredMixin, generic.UpdateView):
    model = Marca
    template_name = "inv/marca_form.html"
    context_object_name = "obj"
    form_class = MarcaForm
    login_url = 'bases:login'
    success_url = reverse_lazy('inv:marca_list')

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class UMView(LoginRequiredMixin, generic.ListView):
    model = UnidadMedida
    template_name = "inv/um_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'


class UMNew(LoginRequiredMixin, generic.CreateView):
    model = UnidadMedida
    template_name = "inv/um_form.html"
    context_object_name = "obj"
    form_class = UnidadMedidaForm
    login_url = 'bases:login'
    success_url = reverse_lazy('inv:um_list')

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class UMEdit(LoginRequiredMixin, generic.UpdateView):
    model = UnidadMedida
    template_name = "inv/um_form.html"
    context_object_name = "obj"
    form_class = UnidadMedidaForm
    login_url = 'bases:login'
    success_url = reverse_lazy('inv:um_list')

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


@login_required(login_url='bases:login')
def marca_inactivar(request, id):
    marca = Marca.objects.filter(pk=id).first()
    contexto = {}
    template_name = "inv/categoria_del.html"
    if not marca:
        return redirect("inv:marca_list")

    if(request.method == 'GET'):
        contexto = {'obj': marca}

    if(request.method == 'POST'):
        marca.estado = False
        marca.save()
        messages.success(request, 'Marca Inactivada')
        return redirect("inv:marca_list")
    return render(request, template_name, contexto)


class ProductoView(LoginRequiredMixin, generic.ListView):
    model = Producto
    template_name = "inv/producto_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'


class ProductoNew(LoginRequiredMixin, generic.CreateView):
    model = Producto
    template_name = "inv/producto_form.html"
    context_object_name = "obj"
    form_class = ProductoForm
    login_url = 'bases:login'
    success_url = reverse_lazy('inv:producto_list')

    def form_valid(self, form):
        form.instance.uc = self.request.user
        try:
            return super(ProductoNew, self).form_valid(form)
        except IntegrityError:
            form.add_error('descripcion', 'Ya existe este registro')
            return self.form_invalid(form)


class ProductoEdit(LoginRequiredMixin, generic.UpdateView):
    model = Producto
    template_name = "inv/producto_form.html"
    context_object_name = "obj"
    form_class = ProductoForm
    login_url = 'bases:login'

    success_url = reverse_lazy('inv:producto_list')

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        try:
            return super(ProductoEdit, self).form_valid(form)
        except IntegrityError:
            form.add_error('descripcion', 'Ya existe este registro')
            return self.form_invalid(form)


@login_required(login_url="bases:login")
def verLotes(request, idProd):
    template_name = "inv/lotes_form.html"
    producto = Producto.objects.filter(pk=idProd).first()
    lotes = Lote.objects.filter(producto=producto).order_by('fecha')
    contexto = {'lotes': lotes, 'producto': producto}
    return render(request, template_name, contexto)
