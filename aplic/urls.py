from django.urls import path
from .views import (
    IndexView,
    ClienteView,
    EntrarView,
    ListarPlantasView,
    lista_plantas,
    listar_especies,
    index,
    AreaClienteView, LoginView, avaliar_categoria, realizar_compra, SucessoCompraView,
    cadastro, registrar_endereco, SucessoView, CarrinhoView, SucessoCadastroView, adicionar_ao_carrinho, CarrinhoDeCompras, visualizar_carrinho, remover_do_carrinho, limpar_carrinho, fazer_logout, adicionar_avaliacao,
    listar_pedidos
 
)
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static
from aplic.forms import UserLoginForm

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('cliente.html', ClienteView.as_view(), name="cliente"),
    path('entrar.html', EntrarView.as_view(), name="entrar"),
    path('area_cliente.html', AreaClienteView.as_view(), name='area_cliente'),
    path('listar_plantas.html', lista_plantas, name='listar_plantas'),
    path('listar_plantas_class.html', ListarPlantasView.as_view(), name='listar_plantas_class'), 
    path('index.html', index, name='index'), 
    path('login.html', views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm), name='login'),
    path("cadastro.html", cadastro, name="cadastro"),
    path('registrar_endereco.html', registrar_endereco, name='registrar_endereco'),
    path('sucesso_registro.html', SucessoView.as_view(), name ='sucesso_registro' ),
    path('sucesso_cadastro_user.html', SucessoCadastroView.as_view(), name ='sucesso_cadastro_user' ),
     path('sucesso_compra.html', SucessoCompraView.as_view(), name ='sucesso_compra' ),
    path('carrinho.html', CarrinhoView.as_view(), name = 'carrinho'),
    path('adicionar-ao-carrinho/<int:planta_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho.html', CarrinhoDeCompras, name='carrinho'),
    path('visualizar_carrinho/', visualizar_carrinho, name='visualizar_carrinho'),
    path('limpar_carrinho/', limpar_carrinho, name='limpar_carrinho'),
    path('remover_do_carrinho/<int:item_id>/', remover_do_carrinho, name='remover_do_carrinho'),
    path('listar_especies/', listar_especies, name='listar_especies'),
    path('index', fazer_logout, name='fazer_logout'),
    path('avaliacoes.html', avaliar_categoria, name='avaliar_categoria'),
    path('realizar-compra/', realizar_compra, name='realizar_compra'),
    path('adicionar_avaliacao/<int:categoria>/',  adicionar_avaliacao , name='adicionar_avaliacao'),
    path('meus_pedidos.html', listar_pedidos, name='meus_pedidos')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
