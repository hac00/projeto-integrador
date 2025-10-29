from django.db import models
from django.utils import timezone
from pessoa.models import Funcionario
from veiculo.models import Veiculo

class Vaga(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    ocupada = models.BooleanField(default=False)

    def __str__(self):
        return f"Vaga {self.numero} - {'Ocupada' if self.ocupada else 'Livre'}"


class Movimentacao(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('finalizada', 'Finalizada'),
    ]

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)
    entrada = models.DateTimeField(default=timezone.now)
    saida = models.DateTimeField(null=True, blank=True)
    valor = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativa')

    def calcular_valor(self, tarifa_hora=5.0):
        if not self.saida:
            return None
        delta = self.saida - self.entrada
        horas = delta.total_seconds() / 3600
        horas_arredondadas = int(horas) + (1 if horas % 1 > 0 else 0)
        return tarifa_hora * horas_arredondadas

    def finalizar(self, tarifa_hora=5.0):
        self.saida = timezone.now()
        self.valor = self.calcular_valor(tarifa_hora)
        self.status = 'finalizada'
        self.vaga.ocupada = False
        self.vaga.save()
        self.save()

    def __str__(self):
        return f"{self.veiculo} - {self.status} ({self.entrada.strftime('%d/%m/%Y %H:%M')})"
