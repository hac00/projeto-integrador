from django.db import models
from pessoa.models import Cliente  # assumindo que Cliente já existe

class Veiculo(models.Model):
    TIPO_CHOICES = [
        ('Carro', 'Carro'),
        ('Moto', 'Moto'),
        ('Outro', 'Outro'),
    ]

    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=50)
    cor = models.CharField(max_length=30)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='Carro')
    proprietario = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.placa} - {self.modelo}"
