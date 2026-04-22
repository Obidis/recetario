from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField('Imagen de perfil', upload_to='profile_pictures/', blank=True, null=True)
    birth_date = models.DateField('Fecha de nacimiento', null=True, blank=True)
    email = models.EmailField('Correo electrónico', max_length=254, blank=True)
   

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return self.user.username