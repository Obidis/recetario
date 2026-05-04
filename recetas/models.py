from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Receta(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="recetas", verbose_name=_("Usuario"))
    recipe_name = models.CharField(max_length=50, blank=True, verbose_name=_("Nombre"))
    image = models.ImageField(upload_to="recetas_images/", verbose_name=_("Imagen"))
    recipes = models.TextField(max_length=3000, blank=True, verbose_name=_("Descripcion"))
    ingredients = models.CharField(max_length=1000, blank=True, verbose_name=_("Ingredientes"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creacion"))
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)
    
    class Meta:
         # Un usuario, una valoración por receta
        unique_together = ('user','recipe_name')
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    @property
    def promedio_valoracion(self):
        """Calcula la media de las valoraciones de la receta."""
        avg = self.valoraciones.aggregate(media=Avg('puntos'))['media']
        return avg if avg is not None else 0

    @property
    def num_valoraciones(self):
        """Devuelve el número total de valoraciones."""
        return self.valoraciones.count()
    

    def __str__(self):
        return f"{self.user.username} - {self.recipe_name}"
    
class Valoracion(models.Model):
    receta = models.ForeignKey(Receta, related_name='valoraciones', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    puntos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True,verbose_name=_("Puntos"))

    class Meta:
        unique_together = ('receta', 'usuario') # Un usuario, una valoración por receta