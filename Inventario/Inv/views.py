from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Categoria, SubCategoria, Marca, UnidadMedida
from .forms import CategoriaForm, SubCategoriaForm, MarcaForm, UnidadMedidaForm
from django.urls import reverse_lazy
# Create your views here.


class CategoriaView(LoginRequiredMixin, generic.ListView):
    model = Categoria
    template_name = "inv/categoria_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'


class CategoriaNew(LoginRequiredMixin, generic.CreateView):
    model = Categoria
    template_name = "inv/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    login_url = 'bases:login'
    success_url = reverse_lazy('inv:categoria_list')

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class CategoriaEdit(LoginRequiredMixin, generic.UpdateView):
    model = Categoria
    template_name = "inv/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    login_url = 'bases:login'
    success_url = reverse_lazy('inv:categoria_list')

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
        return super().form_valid(form)


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
        return super().form_valid(form)


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
        return redirect("inv:marca_list")
    return render(request, template_name, contexto)
