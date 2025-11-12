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

    def calcular_tempo(self):
        if not self.saida:
            return None
        delta = self.saida - self.entrada
        return int(delta.total_seconds() // 60)

    def tempo_permanencia(self):
        total_minutos = self.calcular_tempo()
        if total_minutos is None:
            return "-"
        horas = total_minutos // 60
        minutos = total_minutos % 60
        return f"{horas}h {minutos}min"

    def calcular_valor(self, tarifa_hora=5.0):
        total_minutos = self.calcular_tempo()
        if total_minutos is None:
            return None
        horas = total_minutos / 60
        horas_arredondadas = max(1, int(horas)) + (1 if horas % 1 > 0 else 0)
        return tarifa_hora * horas_arredondadas

    def finalizar(self, tarifa):
        self.saida = timezone.now()
        self.valor = self.calcular_valor(tarifa)
        self.status = 'finalizada'
        self.vaga.ocupada = False
        self.vaga.save()
        self.save()

    def __str__(self):
        return f"{self.veiculo} - {self.status} ({self.entrada.strftime('%d/%m/%Y %H:%M')})"

class Valor(models.Model):
    valor_hora = models.DecimalField(max_digits=6, decimal_places=2, default=5.00)

    def __str__(self):
        return f"R$ {self.valor_hora:.2f}/hora"
