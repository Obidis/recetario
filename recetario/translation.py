from modeltranslation.translator import  TranslationOptions, register
from recetas.models import Receta

#Registrar modelos para traduccion
@register(Receta)
class RecetaTranslationOptions(TranslationOptions):
    fields = ('recipe_name', 'recipes', 'ingredients')

