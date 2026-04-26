from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField('Imagen de perfil', upload_to='profile_pictures/', blank=True, null=True)
    birth_date = models.DateField('Fecha de nacimiento', null=True, blank=True)
    email = models.EmailField('Correo electrónico', max_length=254, blank=True)
    favoritos = models.ManyToManyField(User, related_name='favoritos', blank=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return self.user.username
    

class Contact(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    email = models.EmailField(verbose_name='Correo electrónico')
    comentario = models.TextField(verbose_name='Comentario')
    created_at = models.DateTimeField(verbose_name='Fecha de creación', default=timezone.now)

    def __str__(self):
        return self.nombre