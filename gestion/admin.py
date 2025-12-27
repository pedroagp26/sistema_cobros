from django.contrib import admin
from .models import Cliente, Servicio

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'ci', 'celular')
    search_fields = ('nombre_completo', 'ci')

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('tipo_servicio', 'empresa', 'cliente', 'num_servicio')
    list_filter = ('tipo_servicio', 'empresa')