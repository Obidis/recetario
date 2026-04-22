from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Receta(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="recetas", verbose_name="Usuario")
    recipe_name = models.CharField(max_length=50, blank=True, verbose_name="Nombre")
    image = models.ImageField(upload_to="recetas_images/", verbose_name="Imagen")
    recipes = models.TextField(max_length=1000, blank=True, verbose_name="Descripcion")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    likes = models.ManyToManyField(User, related_name="liked_recipes", blank=True, verbose_name="Nº de Likes")

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f"{self.user.username} - {self.recipe_name}" 