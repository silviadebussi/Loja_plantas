import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django import forms

def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return filename



class Cliente(models.Model):
    nome = models.CharField(_("Nome"), blank=False, max_length=50,)
    cpf = models.CharField(max_length=11, unique=True)

    
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='padrao')
    #=========================================================================================================
    
    USERNAME_FIELD = 'nome'
    REQUIRED_FIELDS = ['nome']

    def __str__(self):
        return self.nome



class Endereco(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    rua = models.CharField(max_length=100, blank=False)
    numero = models.IntegerField()
    complemento = models.IntegerField(default= 1)
    bairro = models.CharField(max_length=100, blank=False)
    cidade = models.CharField(max_length=100, blank=False)
    estado = models.CharField(
        max_length = 200,
        blank=False,
        default = 'MG',
        choices = {
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('ES', 'Espirito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
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
            ('DF', 'Distrito Federal')

        }
    )
    cep = models.CharField(max_length=100, blank=False)
    endereco_padrao = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.rua}, {self.numero}, {self.bairro}, {self.cidade}, {self.estado}, {self.cep}"

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'



class Pedido(models.Model):
    codigo_pedido = models.CharField(max_length=10, unique=True, null = True)
    cliente = models.ForeignKey(Cliente, on_delete= models.CASCADE, null=True)
    status = models.CharField(
    max_length=100,
    choices = {
            ('AG', 'Aguardando Pagamento'),
            ('PC','Pagamento Confirmado'),
            ('PE','Pedido enviado'),
            ('PEN','Pedido entregue')

        }
    )
    data_hora = models.DateField()

    def __str__(self):
        return f" {self.cliente}, {self.status}, {self.data_hora}, {self.codigo_pedido}"
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete= models.CASCADE, null=True, default=1)
    planta = models.ForeignKey('Planta', on_delete= models.CASCADE)
    quantidade = models.IntegerField()
    preço = models.FloatField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=1)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantidade * self.preço
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantidade}, {self.preço}"
    
    class Meta:
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Itens de Pedido'


class Status(models.Model):
    nome = models.CharField(
        max_length = 3,
        blank=False,
        default = 'AG',
        choices = {
            ('AG', 'Aguardando Pagamento'),
            ('PC','Pagamento Confirmado'),
            ('PE','Pedido enviado'),
            ('PEN','Pedido entregue')

        }
        )
    

    def __str__(self):
        return f"{self.nome}"
    
    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'


class HistoricoStatus(models.Model):
    data = models.DateField()
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.data}"
    
    class Meta:
        verbose_name = 'Histórico de Status'
        verbose_name_plural = 'Históricos de Status'



class Planta(models.Model):
    nome = models.CharField(max_length=100)
    preço = models.FloatField()
    descricao = models.CharField(max_length=1000)
    cuidados = models.CharField(max_length=1000)
    categorias = models.ManyToManyField('Categorias', related_name='categorias')
    imagem = models.ImageField(upload_to='imagens_plantas/', null=True, blank=True)


    def __str__(self):
        return f"{self.nome}, {self.preço}, {self.descricao}, {self.cuidados}"

    class Meta:
        verbose_name = 'Planta'
        verbose_name_plural = 'Plantas'

class Especie(models.Model):
    Planta = models.ForeignKey('Planta', on_delete=models.CASCADE, default=1)
    nome_da_especie = models.CharField(max_length=100)
    descrição = models.CharField(max_length=1000)
    Categoria_Botânica = models.CharField(max_length=1000)
    Necessidades_de_Luz = models.CharField(max_length=1000)
    Usos_da_Espécie = models.CharField(max_length=1000)
    imagem = models.ImageField(upload_to='imagens_especies/', null=True, blank=True)

    def __str__(self):
        return f"{self.nome_da_especie}, {self.descrição}, {self.Categoria_Botânica}, {self.Necessidades_de_Luz}, {self.Usos_da_Espécie}"

    class Meta:
        verbose_name = 'Espécie'
        verbose_name_plural = 'Espécies'


class Categorias(models.Model):
    nome = models.CharField(
        max_length=100,
        choices=[
            ('Casa', 'Planta de enfeite'),
            ('Jardim', 'Planta natural'),
        ]
    )
    manutencao = models.CharField(max_length=1000)
    cultivo = models.CharField(max_length=1000)
    

    def __str__(self):
        return f"{self.nome}, {self.manutencao}, {self.cultivo}"

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class AvaliacaoCategoria(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    categoria = models.ManyToManyField('Categorias', related_name='avaliacoes_categoria')
    avaliacao = models.PositiveIntegerField()
    comentario = models.TextField(blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Avaliação de {self.categoria} por {self.cliente}"

    class Meta:
        verbose_name = 'AvaliacaoCategoria'
        verbose_name_plural = 'AvaliacoesCategorias'

class Compra(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    itens = models.ManyToManyField(ItemPedido)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    endereco = models.ForeignKey('Endereco', on_delete=models.CASCADE, null=True)

    
    formas_pagamento = [
        ('cartao_credito', 'Cartão de crédito'),
        ('pix', 'PIX'),
    ]
    metodo_pagamento = models.CharField(max_length=20, choices=formas_pagamento, default='PIX')


    def __str__(self):
         return f"Compra de {self.cliente.user.username} em {self.data}"