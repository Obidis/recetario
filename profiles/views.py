from .models import Contact
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _




# Create your views here.

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
