from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Receta
from .forms import RecipeCreateForm
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q


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
    
#Vista para ver el detalle de las recetas
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

#Vista para ver la lista de recetas
@method_decorator(login_required, name="dispatch")
class RecipeListView(ListView):
    model = Receta
    template_name = "recetas/recetas_list.html"
    context_object_name = "recetas"


#Vista para editar las recetas del usuario, solo el propio usuario puede editar sus recetas!
class RecipeUpdateView(UpdateView):
    model = Receta
    template_name = "recetas/recetas_update.html"
    fields = "image", "recipe_name", "recipes", "ingredients"
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, "Receta editada correctamente.")
        return super(RecipeUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('receta_detail', kwargs={'pk': self.object.pk})


#Vista para eliminar las recetas del usuario, solo el propio usuario puede eliminar sus recetas!
@method_decorator(login_required, name="dispatch")
class RecipeDeleteView(DeleteView):
    model = Receta
    template_name = "recetas/recetas_delete.html"
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Receta eliminada correctamente.")
        return super(RecipeDeleteView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('home')
    

class RecipeValoracionView(UpdateView):     
    model = Receta
    template_name = "recetas/recetas_valoracion.html"
    fields = ("valoracion",)
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, "Valoracion creada correctamente.")
        return super(RecipeValoracionView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('receta_detail', kwargs={'pk': self.object.pk})



#buscador de recetas
class SearchView(ListView):
    model = Receta
    template_name = "recetas/search.html"
    context_object_name = "recetas"

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return Receta.objects.filter(
                Q(recipe_name__icontains=query) | Q(recipes__icontains=query)
            ).distinct()
        else:
            return Receta.objects.none()
                