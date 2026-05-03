from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField('Imagen de perfil', upload_to='profile_pictures/', blank=True, null=True)
    birth_date = models.DateField(_('Fecha de nacimiento'), null=True, blank=True)
    email = models.EmailField(_('Correo electrónico'), max_length=254, blank=True)
    favoritos = models.ManyToManyField(User, related_name='favoritos', blank=True)
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", through="Follow")


    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return self.user.username
    

class Contact(models.Model):
    nombre = models.CharField(max_length=50, verbose_name=_("Nombre"))
    email = models.EmailField(verbose_name=_("Correo electrónico"))
    comentario = models.TextField(verbose_name=_("Comentario"))
    created_at = models.DateTimeField(verbose_name=_("Fecha de creación"), default=timezone.now)

    def __str__(self):
        return self.nombre
    
class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, verbose_name=_("Seguidores"), on_delete=models.CASCADE, related_name='follower_set')
    following = models.ForeignKey(UserProfile, verbose_name=_("Seguidos"), on_delete=models.CASCADE, related_name='following_set')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Seguido desde"))

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"

    class Meta:
        verbose_name = _('Seguidor')
        verbose_name_plural = _('Seguidores')

