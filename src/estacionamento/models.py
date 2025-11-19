from django.db import models
from django.utils import timezone
from pessoa.models import Funcionario
from veiculo.models import Veiculo

from django.core.mail import send_mail
from django.template.loader import render_to_string

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

    @property
    def tempo_previsto(self):
        return self.tempo_permanencia()

    @property
    def valor_previsto(self):
        return self.calcular_valor()

    def calcular_tempo(self):
        if self.saida:
            saida = self.saida
        else:
            saida = timezone.now()
        delta = saida - self.entrada
        return int(delta.total_seconds() // 60)

    def tempo_permanencia(self):
        total_minutos = self.calcular_tempo()
        if total_minutos is None:
            return "-"
        horas = total_minutos // 60
        minutos = total_minutos % 60
        return f"{horas}h {minutos}min"

    def calcular_valor(self, tarifa_hora=5.0, saida=None):
        if Valor.objects.first():
            tarifa_hora = Valor.objects.first().valor_hora
        else:
            tarifa_hora = 5.00
        total_minutos = self.calcular_tempo()
        if total_minutos is None:
            return None
        horas = total_minutos / 60
        # horas_arredondadas = max(1, int(horas) + (1 if horas % 1 else 0))
        horas_arredondadas = max(1, (total_minutos + 59) // 60)
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

    def enviar_email(self):
        cliente = self.veiculo.proprietario
        veiculo = self.veiculo
        funcionario = self.funcionario

        email = [cliente.email]

        dados = {
            'cliente': cliente.nome,
            'placa': veiculo.placa,
            'modelo': veiculo.modelo,
            'tempo': self.tempo_permanencia(),
            'funcionario': funcionario.nome,
            'valor': self.valor
        }

        texto_email = render_to_string('emails/texto_email.txt', dados)
        html_email = render_to_string('emails/texto_email.html', dados)

        send_mail(
            subject='Estacionamento - Concluído',
            message=texto_email,
            from_email='henriqueac00@gmail.com',
            recipient_list=email,
            html_message=html_email,
            fail_silently=False,
        )

class Valor(models.Model):
    valor_hora = models.DecimalField(max_digits=6, decimal_places=2, default=5.00)

    def __str__(self):
        return f"R$ {self.valor_hora:.2f}/hora"

class Pagamento(models.Model):
    FORMAS = [('PIX', 'Pix'), ('CARTAO', 'Cartão'), ('DINHEIRO', 'Dinheiro')]
    movimentacao = models.OneToOneField(Movimentacao, on_delete=models.CASCADE, related_name='pagamento')
    forma = models.CharField(max_length=10, choices=FORMAS, default='PIX')
    valor = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.movimentacao} - {self.get_forma_display()} - R$ {self.valor:.2f}"
