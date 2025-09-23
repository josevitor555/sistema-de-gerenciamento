from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


# Registre o modelo User no admin
class UsuarioAdmin(admin.ModelAdmin): 
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Usuario, UsuarioAdmin)
