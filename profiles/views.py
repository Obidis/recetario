from .models import Contact, Follow
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from profiles.models import UserProfile
from django.views.generic.edit import FormView
from .forms import ProfileFollow
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



#Contacto

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
           nombre = form.cleaned_data["nombre"]
           email = form.cleaned_data["email"]
           comentario = form.cleaned_data["comentario"]
           messages.add_message(request, messages.SUCCESS, "Comentario enviado correctamente.")
                    
           #crear un contacto al enviar un email desde contacto en el admin
           Contact.objects.create(nombre=nombre, email=email, comentario=comentario)

           success = send_mail(
                f"Contacto de {nombre}",
                comentario,
                "keosden@gmail.com",
                ["jjsantosfernandez@proton.me"],
                fail_silently=False,
            )
           context = {"form":form, "success": success}
           return render(request,  "general/contact.html", context)
        else:
            context = {
                "formulario":form
            }
            return render(request, "general/contact.html", context)
    else:
        form = ContactForm()
        context = {
            "formulario":form
        }
        return render(request, "general/contact.html", context)


class ProfileDetailView(DetailView, FormView):

    model = UserProfile
    template_name = "general/profile_detail.html"
    context_object_name = "profile"
    form_class = ProfileFollow

    def get_initial(self):
        self.initial['profile_pk'] =  self.get_object().pk
        return super().get_initial()

    def form_valid(self, form):
        profile_pk = form.cleaned_data.get('profile_pk')
        action = form.cleaned_data.get('action')
        following = UserProfile.objects.get(pk=profile_pk)

        if action == "follow":
            Follow.objects.get_or_create(
                follower=self.request.user.profile,
                following=following
            )


        if Follow.objects.filter(
              follower=self.request.user.profile,
              following=following
        ).count():
            Follow.objects.filter(
                  follower=self.request.user.profile,
                  following=following
              ).delete()
            messages.add_message(self.request, messages.SUCCESS, f"Se ha dejado de seguir a {following.user.username}")
        else:
            Follow.objects.get_or_create(
              follower=self.request.user.profile,
              following=following
            )
            messages.add_message(self.request, messages.SUCCESS, f"Se empieza a seguir a {following.user.username}")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile_detail', args=[self.get_object().pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Comprobamos si seguimos al usuario
        following = Follow.objects.filter(follower=self.request.user.profile, following=self.get_object()).exists()
        context['following'] = following
        return context


@method_decorator(login_required, name="dispatch")
class ProfileListView(ListView):
    model = UserProfile
    template_name = "profiles/profile_list.html"
    context_object_name = "profiles"

    #excluirte de la busqueda
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserProfile.objects.all().order_by('user__username').exclude(user=self.request.user)
        return UserProfile.objects.all().order_by('user__username')

    