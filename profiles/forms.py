from django import forms
from django.utils.translation import gettext_lazy as _

class FavoriteForm(forms.Form):
    profile_pk = forms.IntegerField(label="Idendtificador del usuario", widget=forms.HiddenInput())
    
class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100, label= _("Nombre"))
    email = forms.EmailField(label="Email")
    comentario = forms.CharField(widget=forms.Textarea, label= _("Comentario"))
    
    def clean_comentario(self):
        comentario = self.cleaned_data["comentario"]
        if len(comentario) < 10:
            raise forms.ValidationError("El comentario debe tener al menos 10 caracteres")
        return comentario

class ProfileFollow(forms.Form):
    profile_pk = forms.IntegerField(widget=forms.HiddenInput())