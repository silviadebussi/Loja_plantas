from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Fisica(Cliente):
    cpf = models.IntegerField()

    def __str__(self):
        return f"{self.cpf}"

class Juridica(Cliente):
    cnpf = models.IntegerField()

    def __str__(self):
        return f"{self.cnpj}"


class Endereco(models.Model):
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    cep = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.rua}, {self.numero}, {self.bairro}, {self.cidade}, {self.estado}, {self.cep}"

class Pedido(models.Model):
    codigo = models.CharField(max_length=100)
    cliente = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    data_hora = models.FloatField()

    def __str__(self):
        return f"{self.codigo}, {self.cliente}, {self.status}, {self.data_hora}"

class ItemPedido(models.Model):
    quantidade = models.IntegerField()
    preço = models.FloatField()

    def __str__(self):
        return f"{self.quantidade}, {self.preço}"


class HistoricoStatus(models.Model):
    data = models.DateField()

    def __str__(self):
        return f"{self.data}"

class Status(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome}"

class Planta(models.Model):
    nome = models.CharField(max_length=100)
    preço = models.FloatField()
    descrição = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome}, {self.preço}, {self.descrição}"

class Especie(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome}"

class Categorias(models.Model):
    casaDecoração = models.CharField(max_length=100)
    manutencaoCultivo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.casaDecoração}, {self.manutencaoCultivo}"

# Create your models here.
