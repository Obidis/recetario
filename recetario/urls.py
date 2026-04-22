from django.contrib import admin
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

from .views import HomeView, LoginView, logout_view, RegisterView, LegalView, ContactView,ProfileDetailView
from recetas.views import RecipeCreateView, RecipeDetailView
 


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('legal/', LegalView.as_view(), name="legal"),
    path('recetas/create/', RecipeCreateView.as_view(), name="recipe_create"),
    path('recetas/<pk>/', RecipeDetailView.as_view(), name="receta_detail"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('profile/<pk>', ProfileDetailView.as_view(), name='profile_detail'),

    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
