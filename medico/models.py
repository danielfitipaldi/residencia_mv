from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from usuario.models import Usuario


class Medico(models.Model):

    dados_pessoais = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Dados Pessoais')

    crm = models.CharField(max_length=10, blank=False, null=False, verbose_name='CRM')

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('NB', 'Não Binário')
    )
    genero = models.CharField(max_length=2, choices=GENDER_CHOICES, verbose_name='Gênero')

    data_nascimento = models.DateField(verbose_name='Data de Nascimento')

    data_criacao = models.DateTimeField(
        default=timezone.now,
        verbose_name='Data de Criação'
    )

    bairro = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    cidade = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    estado = models.CharField(
        max_length=2,
        choices=(('AC', 'Acre'),
                 ('AL', 'Alagoas'),
                 ('AP', 'Amapá'),
                 ('AM', 'Amazonas'),
                 ('BA', 'Bahia'),
                 ('CE', 'Ceará'),
                 ('DF', 'Distrito Federal'),
                 ('ES', 'Espírito Santo'),
                 ('GO', 'Goiás'),
                 ('MA', 'Maranhão'),
                 ('MT', 'Mato Grosso'),
                 ('MS', 'Mato Grosso do Sul'),
                 ('MG', 'Minas Gerais'),
                 ('PA', 'Pará'),
                 ('PB', 'Paraíba'),
                 ('PR', 'Paraná'),
                 ('PE', 'Pernambuco'),
                 ('PI', 'Piauí'),
                 ('RJ', 'Rio de Janeiro'),
                 ('RN', 'Rio Grande do Norte'),
                 ('RS', 'Rio Grande do Sul'),
                 ('RO', 'Rondônia'),
                 ('RR', 'Roraima'),
                 ('SC', 'Santa Catarina'),
                 ('SP', 'São Paulo'),
                 ('SE', 'Sergipe'),
                 ('TO', 'Tocantins'),
                 ))

    pais = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name='País'
    )

    def __str__(self):
        return f'Dr. {self.dados_pessoais.first_name} {self.dados_pessoais.last_name}'


class MeusPacientes(models.Model):

    paciente = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    medico = models.ForeignKey(Medico, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.paciente.first_name}'

