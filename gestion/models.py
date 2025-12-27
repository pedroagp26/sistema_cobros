from django.db import models

class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=200)
    ci = models.CharField(max_length=20, unique=True, verbose_name="Cédula de Identidad")
    celular = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre_completo

class Servicio(models.Model):
    TIPO_CHOICES = [
        ('LUZ', 'Luz'),
        ('AGUA', 'Agua'),
        ('TELEFONO', 'Teléfono'),
        ('INTERNET', 'Internet'),
        ('GAS', 'Gas Domiciliario'),
        ('ASEO', 'Tasa de Aseo'),
        ('CUENTA', 'Cuenta Bancaria'),
    ]

    # La relación: un cliente tiene muchos servicios
    # Usamos related_name='servicios' para facilitar el acceso en el HTML
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='servicios')
    
    tipo_servicio = models.CharField(max_length=100, choices=TIPO_CHOICES) 
    empresa = models.CharField(max_length=100)      # Ej: CRE, Tigo
    num_servicio = models.CharField(max_length=50)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_servicio} ({self.empresa}) - {self.cliente.nombre_completo}"