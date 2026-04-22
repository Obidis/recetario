from .models import Receta
from django import forms


class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = [
            "image",
            "recipe_name",
            "recipes"
        ]
