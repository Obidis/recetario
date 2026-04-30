from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import HomeView, LoginView, logout_view, RegisterView, LegalView, ProfileUpdateView, toggle_favorite
from recetas.views import RecipeCreateView, RecipeDetailView, RecipeListView, RecipeUpdateView, RecipeDeleteView, RecipeValoracionView
from profiles.views import contact_view, ProfileListView, ProfileDetailView


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('legal/', LegalView.as_view(), name="legal"),
    path('recetas/create/', RecipeCreateView.as_view(), name="recipe_create"),
    path('recetas/<pk>/', RecipeDetailView.as_view(), name="receta_detail"),
    path('receta/list/', RecipeListView.as_view(), name="receta_list"),
    path('recetas/update/<pk>/', RecipeUpdateView.as_view(), name="recetas_update"),
    path('recetas/delete/<pk>/', RecipeDeleteView.as_view(), name="recetas_delete"),
    path('recetas/valoracion/<pk>/', RecipeValoracionView.as_view(), name="recetas_valoracion"),
    path('contact/', contact_view, name="contact"),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/update/<int:pk>/', ProfileUpdateView.as_view(), name="profile_update"),
    path('profile/list/', ProfileListView.as_view(), name='profile_list'),
    path('profile/favorites/<int:pk>/', toggle_favorite, name="profile_favorites"),

    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
