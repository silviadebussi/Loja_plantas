# Generated by Django 4.2.4 on 2023-11-29 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(choices=[('Casa', 'Planta de enfeite'), ('Jardim', 'Planta natural')], max_length=100)),
                ('manutencao', models.CharField(max_length=100)),
                ('cultivo', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome')),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('email', models.EmailField(default='seuemail@gmail.com', max_length=254, unique=True)),
                ('user', models.OneToOneField(default='padrao', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Especie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_da_especie', models.CharField(max_length=100)),
                ('descrição', models.CharField(max_length=100)),
                ('Categoria_Botânica', models.CharField(max_length=100)),
                ('Necessidades_de_Luz', models.CharField(max_length=100)),
                ('Usos_da_Espécie', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Espécie',
                'verbose_name_plural': 'Espécies',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(choices=[('AG', 'Aguardando Pagamento'), ('PC', 'Pagamento Confirmado'), ('PE', 'Pedido enviado'), ('PEN', 'Pedido entregue')], default='AG', max_length=3)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Status',
            },
        ),
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('preço', models.FloatField()),
                ('descricao', models.CharField(max_length=100)),
                ('cuidados', models.CharField(max_length=100)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='imagens_plantas/')),
                ('categorias', models.ManyToManyField(related_name='categorias', to='aplic.categorias')),
            ],
            options={
                'verbose_name': 'Planta',
                'verbose_name_plural': 'Plantas',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('AG', 'Aguardando Pagamento'), ('PC', 'Pagamento Confirmado'), ('PE', 'Pedido enviado'), ('PEN', 'Pedido entregue')], max_length=100)),
                ('data_hora', models.DateField()),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='aplic.cliente')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('preço', models.FloatField()),
                ('pedido', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='aplic.pedido')),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplic.planta')),
            ],
            options={
                'verbose_name': 'Item de Pedido',
                'verbose_name_plural': 'Itens de Pedido',
            },
        ),
        migrations.CreateModel(
            name='HistoricoStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplic.pedido')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplic.status')),
            ],
            options={
                'verbose_name': 'Histórico de Status',
                'verbose_name_plural': 'Históricos de Status',
            },
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rua', models.CharField(max_length=100)),
                ('numero', models.IntegerField()),
                ('complemento', models.IntegerField(default=1)),
                ('bairro', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
                ('estado', models.CharField(choices=[('SE', 'Sergipe'), ('AC', 'Acre'), ('SP', 'São Paulo'), ('PE', 'Pernambuco'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('RJ', 'Rio de Janeiro'), ('MG', 'Minas Gerais'), ('GO', 'Goiás'), ('PB', 'Paraíba'), ('BA', 'Bahia'), ('MA', 'Maranhão'), ('MS', 'Mato Grosso do Sul'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('PR', 'Paraná'), ('TO', 'Tocantins'), ('DF', 'Distrito Federal'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('AL', 'Alagoas'), ('MT', 'Mato Grosso'), ('PI', 'Piauí'), ('ES', 'Espirito Santo'), ('CE', 'Ceará')], default='MG', max_length=200)),
                ('cep', models.CharField(max_length=100)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplic.cliente')),
            ],
            options={
                'verbose_name': 'Endereço',
                'verbose_name_plural': 'Endereços',
            },
        ),
        migrations.CreateModel(
            name='AvaliacaoCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avaliacao', models.PositiveIntegerField()),
                ('comentario', models.TextField(blank=True, null=True)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.ManyToManyField(related_name='avaliacoes_categoria', to='aplic.categorias')),
            ],
            options={
                'verbose_name': 'AvaliacaoCategoria',
                'verbose_name_plural': 'AvaliacoesCategorias',
            },
        ),
    ]
