
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_clientes, name='lista_clientes'),
    path('cliente/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('cliente/<int:cliente_id>/nuevo-servicio/', views.agregar_servicio, name='agregar_servicio'),
    path('cliente/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('servicio/editar/<int:servicio_id>/', views.editar_servicio, name='editar_servicio'),
    path('cliente/<int:cliente_id>/pdf/', views.generar_pdf_cliente, name='generar_pdf_cliente'),
]
