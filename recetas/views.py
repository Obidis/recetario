from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Receta
from .forms import RecipeCreateForm
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404

# Create your views here.

@method_decorator(login_required, name="dispatch")
class RecipeCreateView(CreateView):
    template_name = "recetas/recetas_create.html"
    model = Receta
    form_class = RecipeCreateForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user

        messages.add_message(self.request, messages.SUCCESS, "Receta creada correctamente.")
        return super(RecipeCreateView, self).form_valid(form)
    

@method_decorator(login_required, name="dispatch")
class RecipeDetailView(DetailView):
    template_name = "recetas/recetas_detail.html"
    model = Receta
    context_object_name = 'receta'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = get_object_or_404(Receta, pk=self.kwargs['pk']).pk
        context['ingredientes'] = Receta.objects.get(pk=pk).ingredients.split(',')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = self.get_object()
        return super(RecipeDetailView, self).form_valid(form)
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Comentario creado correctamente.")
        return reverse('receta_detail', kwargs={'pk': self.object.pk})         


@method_decorator(login_required, name="dispatch")
class RecipeListView(ListView):
    model = Receta
    template_name = "recetas/recetas_list.html"
    context_object_name = "recetas"

   