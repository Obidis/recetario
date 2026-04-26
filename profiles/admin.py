from django.contrib import admin
from .models import UserProfile, Contact

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "birth_date"]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ["nombre", "email","created_at"]