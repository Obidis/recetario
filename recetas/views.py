from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Receta, Valoracion
from .forms import RecipeCreateForm
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from deep_translator import GoogleTranslator
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Avg

# Creacion de recetas, solo los usuarios registrados pueden crear recetas
@method_decorator(login_required, name="dispatch")
class RecipeCreateView(CreateView):
    template_name = "recetas/recetas_create.html"
    model = Receta
    form_class = RecipeCreateForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user

        messages.add_message(self.request, messages.SUCCESS, _('Receta creada correctamente.'))
        return super(RecipeCreateView, self).form_valid(form)
    

#Vista para ver el detalle de las recetas
@method_decorator(login_required, name="dispatch")
class RecipeDetailView(DetailView):
    template_name = "recetas/recetas_detail.html"
    model = Receta
    context_object_name = 'receta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receta = self.object
        idioma_usuario = self.request.LANGUAGE_CODE

        # Normalizar código de idioma (ej: 'es-es' -> 'es')
        idioma_corto = idioma_usuario.split('-')[0]
        #Traducir el nombre de la receta
        try:
            if receta.recipe_name:
                context['nombre_traducido'] = GoogleTranslator(
                    source='auto', target=idioma_corto
                ).translate(receta.recipe_name)
            else:
                context['nombre_traducido'] = ''
        except Exception:
            context['nombre_traducido'] = receta.recipe_name or ''

        # Traducir la descripción de la receta
        try:
            if receta.recipes:
                context['receta_traducida'] = GoogleTranslator(
                    source='auto', target=idioma_corto
                ).translate(receta.recipes)
                #Separar saltos de línea
                context['receta_traducida'] = context['receta_traducida'].replace('\n', ' ')
             
            else:
                context['receta_traducida'] = ''
        except Exception:
            context['receta_traducida'] = receta.recipes or ''

        # Traducir los ingredientes y pasarlos como lista
        try:
            if receta.ingredients:
                ingredientes_texto = GoogleTranslator(
                    source='auto', target=idioma_corto
                ).translate(receta.ingredients)
                # Separar por comas o saltos de línea
                context['ingredientes'] = [
                    ing.strip() for ing in ingredientes_texto.replace('\n', ',').split(',')
                    if ing.strip()
                ]
            else:
                context['ingredientes'] = []
        except Exception:
            # Si falla la traducción, mostrar los ingredientes originales
            if receta.ingredients:
                context['ingredientes'] = [
                    ing.strip() for ing in receta.ingredients.replace('\n', ',').split(',')
                    if ing.strip()
                ]
            else:
                context['ingredientes'] = []

        return context


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
        messages.add_message(self.request, messages.SUCCESS, _('Receta editada correctamente.'))
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
        messages.add_message(self.request, messages.SUCCESS, _('Receta eliminada correctamente.'))
        return super(RecipeDeleteView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('home')
    


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
                


#Vista para valorar las recetas, el usuario solo puede valorar una vez cada receta, si vuelve a valorar la misma receta se actualiza la valoración
@login_required
def valorar_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)

    if request.method == 'POST':
        puntos = request.POST.get('puntos')

        if puntos:
            valoracion_obj, created = Valoracion.objects.get_or_create(
                usuario=request.user,
                receta=receta,
                defaults={'puntos': int(puntos)}
            )
            if not created:
                valoracion_obj.puntos = int(puntos)
                valoracion_obj.save()
                messages.add_message(request, messages.SUCCESS, _('Valoración actualizada correctamente.'))
            else:
                messages.add_message(request, messages.SUCCESS, _('Valoración creada correctamente.'))
        else:
            messages.add_message(request, messages.ERROR, _('No se proporcionó una valoración válida.'))
        return redirect('receta_detail', pk=pk)

       
    return render(request, 'recetas/recetas_valoracion.html' , {'receta': receta})
    
    
    

    
    #solo una valoracion por usuario si el usuario ya ha valorado la receta se muestra su valoración actual y un mensaje indicando que ya ha valorado la receta
   
  