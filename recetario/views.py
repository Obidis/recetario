from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from django.views.generic import TemplateView
from recetas.models import Receta
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm

from profiles.models import UserProfile
from django.views.generic import DetailView, UpdateView ,FormView
from recetas.models import Receta
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib import messages




class HomeView(TemplateView):
    template_name = "general/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_recetas = Receta.objects.order_by('-created_at')[:5]
        context['last_recetas'] = last_recetas
       
        return context   
    


class LoginView(FormView):
    template_name = "general/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=usuario, password=password)

        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f'Bienvenido de nuevo {user.username}')
            return HttpResponseRedirect(reverse('home'))

        else:
            messages.add_message(
                self.request, messages.ERROR, 'Usuario no válido o contraseña no válida')
            return super(LoginView, self).form_invalid(form)





@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Se ha cerrado sesión correctamente.")
    return HttpResponseRedirect(reverse('home'))



class RegisterView(CreateView):
    template_name = "general/register.html"
    model = User
    success_url = reverse_lazy('login')
    form_class = RegistrationForm

    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Usuario creado correctamente.")
        return super(RegisterView, self).form_valid(form)

        
    


class LegalView(TemplateView):
    template_name = "general/legal.html"

























# Vista para editar el perfil de usuario, solo el propio usuario puede editar su perfil
@method_decorator(login_required, name="dispatch")
class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = "profiles/profile_update.html"
    context_object_name = "profile"
    fields = ["profile_picture", "email", "birth_date"]

    #comprueba que editas tu usuario y no otro
    def dispatch(self, request, *args, **kwargs):
        user_profile = self.get_object()
        if user_profile.user != self.request.user:
            return HttpResponseRedirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Usuario acutalizado correctamente.")
        return super(ProfileUpdateView, self).form_valid(form)


    def get_success_url(self):
        return reverse("profile_detail", args=[self.object.pk])
    
    



# Vista para mostrar y gestionar las recetas favoritas de un usuario

@login_required
def toggle_favorite(request, pk):
    user = request.user

    if request.method == "POST":
        # POST: pk is a Receta pk — toggle favourite
        receta = get_object_or_404(Receta, pk=pk)
        if user in receta.favourite.all():
            receta.favourite.remove(user)
            messages.add_message(request, messages.INFO, "Receta eliminada de favoritos.")
        else:
            receta.favourite.add(user)
            messages.add_message(request, messages.SUCCESS, "Receta añadida a favoritos.")
        return HttpResponseRedirect(reverse('receta_detail', args=[pk]))

    # GET: pk is a UserProfile pk — show favourites page
    favorite_recetas = Receta.objects.filter(favourite=user)
    return render(request, 'profiles/profile_favorites.html', {
        'favorite_recetas': favorite_recetas,
    })
