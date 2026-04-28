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
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", through="Follow")


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
    
class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, verbose_name='Seguidores ', on_delete=models.CASCADE, related_name='follower_set')
    following = models.ForeignKey(UserProfile, verbose_name='Seguidos ', on_delete=models.CASCADE, related_name='following_set')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Seguido desde')

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"

    class Meta:
        verbose_name = 'Seguidor'
        verbose_name_plural = 'Seguidores'

