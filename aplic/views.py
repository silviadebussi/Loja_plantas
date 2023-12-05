from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Planta, Cliente, User, Endereco, Pedido, ItemPedido, Especie, AvaliacaoCategoria, Categorias, Compra
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect,get_object_or_404
from django.shortcuts import render
from .forms import EnderecoForm, AvaliacaoCategoriaForm
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CompraForm
from django.contrib import messages
from django.utils import timezone

class IndexView(TemplateView):
    template_name = 'index.html'

class ClienteView(TemplateView):
    template_name = 'cliente.html'

class EntrarView(TemplateView):
    template_name = 'entrar.html'

class CadastroView(TemplateView):
    template_name = 'cadastro.html'

class CadastroPageView(TemplateView):
    template_name = 'cadastrar.html'

class ListarPlantasView(TemplateView):
    template_name = 'listar_plantas.html'

class AreaClienteView(TemplateView):
    template_name = 'area_cliente.html'

class SucessoView(TemplateView):
    template_name = 'sucesso_registro.html'

class SucessoCadastroView(TemplateView):
    template_name = 'sucesso_cadastro_user.html'

class SucessoCompraView(TemplateView):
    template_name = 'sucesso_compra.html'

class CarrinhoView(TemplateView):
    template_name = 'carrinho.html'

class EspecieView(TemplateView):
    template_name = 'especies.html'

class LoginView(TemplateView):
    template_name = 'login.html'

class Meus_PedidosView(TemplateView):
    template_name = 'meus_pedidos.html'

def lista_plantas(request):
    plantas = Planta.objects.all()

    search_term = request.GET.get('search', '')

    if search_term:
        plantas = plantas.filter(nome__icontains=search_term)

    context = {'plantas': plantas, 'termo_de_busca': search_term}


    return render(request, 'listar_plantas.html', context)

def index(request):
    plantas = Planta.objects.all()
    return render(request, 'index.html', {'plantas': plantas})

def cliente_login(request):
    if request.method == 'POST':
        nome = request.POST.get('username')
        senha = request.POST.get('password')
        cliente = authenticate(request, username=nome, password=senha)

        if cliente is not None:
            login(request, cliente)
            return redirect('area_cliente') 

def cadastro (request):
    if request.method == "GET":
        return render(request, "cadastro.html")
    else:
       
        nome = request.POST.get("nome")
        cpf = request.POST.get("cpf")
        
        username = request.POST.get('username')
        password = request.POST.get('senha')

        
        cliente = Cliente.objects.filter(cpf=cpf).first()

        if cliente:
            return HttpResponse("Já existe usuario com esse cpf")
        
        
        user = User.objects.create_user(username=username, password=password)
       
      
        cliente = Cliente.objects.create(nome=nome, cpf=cpf, user=user)
        cliente.save()

        return redirect('sucesso_cadastro_user')

@login_required   
def registrar_endereco(request):
    if request.method == 'POST':
        formulario = EnderecoForm(request.user, request.POST)
        if formulario.is_valid():
         
            rua = formulario.cleaned_data['rua']
            cidade = formulario.cleaned_data['cidade']
            estado = formulario.cleaned_data['estado']
            numero = formulario.cleaned_data['numero']
            cep = formulario.cleaned_data['cep']

            
            endereco = Endereco.objects.create(
                cliente=request.user.cliente,
                rua=rua,
                cidade=cidade,
                estado=estado,
                numero=numero,
                cep=cep
            )

        
            return redirect('sucesso_registro')
    
    else:
        formulario = EnderecoForm(request.user)

    return render(request, 'registrar_endereco.html', {'formulario': formulario})

class CarrinhoDeCompras:
    def __init__(self, session):
        self.session = session
        if 'carrinho' not in session:
            session['carrinho'] = []

    def adicionar_item(self, item_id):
        self.session['carrinho'].append(item_id)

    def calcular_total(self):
        itens = ItemPedido.objects.filter(id__in=self.session['carrinho'])
        total = sum(item.subtotal for item in itens)
        return total
    
    def limpar_carrinho(self):
        self.session['carrinho'] = []

    def remover_item(self, item_id):
        self.session['carrinho'] = [item for item in self.session['carrinho'] if item != item_id]

@login_required
def adicionar_ao_carrinho(request, planta_id):
    planta = get_object_or_404(Planta, pk=planta_id)

    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 155))
        user = request.user

      
        cliente, _ = Cliente.objects.get_or_create(user=user)

       
        pedido, _ = Pedido.objects.get_or_create(
            cliente=cliente,
            defaults={'data_hora': timezone.now()}
        )

        itemPedido = ItemPedido.objects.filter(
            planta=planta,
            pedido=pedido
        ).first()

        if itemPedido is not None:
          
            itemPedido.quantidade = quantidade
            itemPedido.save()
        else:
           
            itemPedido = ItemPedido.objects.create(
                planta=planta,
                quantidade=quantidade,
                preço=float(planta.preço),
                pedido=pedido
            )

        carrinho = CarrinhoDeCompras(request.session)
        carrinho.adicionar_item(item_id=itemPedido.id)

        request.session.save()

        return redirect('visualizar_carrinho')

    return render(request, 'carrinho.html', {'planta': planta})


def visualizar_carrinho(request):
    if not request.user.is_authenticated:
        
        return redirect('login')

    carrinho = CarrinhoDeCompras(request.session)
    total = carrinho.calcular_total()

    itens_ids = request.session.get('carrinho', [])
    itens = ItemPedido.objects.filter(id__in=itens_ids)
    
    print(f"Sessão carrinho IDs: {itens_ids}")
    print(f"Itens no carrinho: {itens}")

    return render(request, 'carrinho.html', {'itens': itens, 'total': total})

def limpar_carrinho(request):
    carrinho = CarrinhoDeCompras(request.session)
    carrinho.limpar_carrinho()
    request.session.save()
    return redirect('visualizar_carrinho')

def remover_do_carrinho(request, item_id):
    carrinho = CarrinhoDeCompras(request.session)
    carrinho.remover_item(item_id)
    request.session.save()
    return redirect('visualizar_carrinho')

def listar_especies(request):
    especies = Especie.objects.all()
    return render(request, 'especies.html', {'especies': especies})

def fazer_logout(request):
    logout(request)
    return redirect('index')

def avaliar_categoria(request):
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        avaliacao = request.POST.get('avaliacao')
        comentario = request.POST.get('comentario', '')

        categoria = Categorias.objects.get(pk=categoria_id)


        avaliacao_categoria = AvaliacaoCategoria.objects.create(
            avaliacao=avaliacao,
            comentario=comentario
        )
        
      
        avaliacao_categoria.categoria.set([categoria])

        return redirect('area_cliente') 
    categorias = Categorias.objects.all()

    return render(request, 'avaliacoes.html', {'categorias': categorias})

def realizar_compra(request):
    cliente_atual = request.user.cliente
    itens_ids = request.session.get('carrinho', [])

    endereco_cliente = Endereco.objects.filter(cliente=cliente_atual).first()

    itens_carrinho = ItemPedido.objects.filter(id__in=itens_ids, pedido__cliente=cliente_atual)
    total_fixo = sum(item.subtotal for item in itens_carrinho)

    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():

            compra = form.save(commit=False)


            compra.cliente = cliente_atual
            compra.total = total_fixo
            compra.endereco = endereco_cliente

            compra.save()

            compra.itens.set(ItemPedido.objects.filter(id__in=itens_ids, pedido__cliente=cliente_atual))

            request.session['carrinho'] = []

            return redirect('sucesso_compra')
        else:
            messages.error(request, 'Erro ao processar o formulário. Verifique os campos.')
    else:
        form = CompraForm(initial={'cliente': cliente_atual, 'endereco': endereco_cliente})

    itens_da_compra = ItemPedido.objects.filter(pedido__cliente=cliente_atual)

    return render(request, 'realizar_compra.html', {'form': form, 'total_fixo': total_fixo, 'itens_da_compra': itens_da_compra})

def area_cliente(request):
    categorias = Categorias.objects.all()
    pedidos = Pedido.objects.filter(cliente=request.user)
    
    if request.method == 'POST':
        form = AvaliacaoCategoriaForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.cliente = request.user
            avaliacao.save()
    else:
        form = AvaliacaoCategoriaForm()

    context = {
        'pedidos': pedidos,
        'categorias': categorias,
        'form': form,
    }


    return render(request, 'area_cliente.html', context)

@login_required
def adicionar_avaliacao(request, categoria_id):
    categoria = get_object_or_404(Categorias, pk=categoria_id)

    if request.method == 'POST':
        form = AvaliacaoCategoriaForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.categoria = categoria
            avaliacao.cliente = request.user
            avaliacao.save()
            return redirect('area_cliente')  

    else:
        form = AvaliacaoCategoriaForm()
    return render(request, 'adicionar_avaliacao.html', {'form': form, 'categoria': categoria})



def abrir_descricao(request):
    descricao = request.GET.get('descricao', '')
    return render(request, 'abrir_descricao.html', {'descricao': descricao})
