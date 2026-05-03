from django.contrib import admin
from recetas.models import Receta
from modeltranslation.admin import TranslationAdmin
from .models import Receta

# Register your models here.

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ["user", "recipe_name", "created_at", "valoracion" ]



