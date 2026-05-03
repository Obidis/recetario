from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Receta(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="recetas", verbose_name=_("Usuario"))
    recipe_name = models.CharField(max_length=50, blank=True, verbose_name=_("Nombre"))
    image = models.ImageField(upload_to="recetas_images/", verbose_name=_("Imagen"))
    recipes = models.TextField(max_length=3000, blank=True, verbose_name=_("Descripcion"))
    valoracion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True, verbose_name=_("Valoracion"))
    ingredients = models.CharField(max_length=1000, blank=True, verbose_name=_("Ingredientes"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creacion"))
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)
    
    class Meta:
         # Un usuario, una valoración por receta
        unique_together = ('user','recipe_name')
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f"{self.user.username} - {self.recipe_name} - {self.valoracion}" 
    
