from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import HomeView, LoginView, logout_view, RegisterView, LegalView,toggle_favorite
from recetas.views import RecipeCreateView, RecipeDetailView, RecipeListView, RecipeUpdateView, RecipeDeleteView, SearchView, valorar_receta
from profiles.views import contact_view, ProfileListView, ProfileDetailView, ProfileUpdateView
from django.urls import re_path, include #para la traduccion
from django.conf.urls.i18n import i18n_patterns #para la traduccion

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')), #para la traduccion
]


urlpatterns += i18n_patterns(
    re_path(r'^rosetta/', include('rosetta.urls')),
  
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
    path('recetas/valoracion/<pk>/', valorar_receta, name="valorar_receta"),
    path('search/', SearchView.as_view(), name="search"),
    path('contact/', contact_view, name="contact"),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/update/<int:pk>/', ProfileUpdateView.as_view(), name="profile_update"),
    path('profile/list/', ProfileListView.as_view(), name='profile_list'),
    path('profile/favorites/<int:pk>/', toggle_favorite, name="profile_favorites"),
    path('admin/', admin.site.urls),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
