from django.urls import path
from . import views

urlpatterns = [
    path("cadastro/", views.cadastro_usuario, name="cadastro"),
    path("login/", views.login_usuario, name="login"),
    path("logout/", views.logout_usuario, name="logout"),
    path("", views.home, name="home"),
    path("produtos/", views.lista_produtos, name="lista_produtos"),
    path(
        "adicionar_carrinho/<int:produto_id>/",
        views.adicionar_carrinho,
        name="adicionar_carrinho",
    ),
    path("carrinho/", views.ver_carrinho, name="ver_carrinho"),
    path(
        "carrinho/remover/<int:item_id>/",
        views.remover_item_carrinho,
        name="remover_item_carrinho",
    ),
    path("checkout/", views.checkout, name="checkout"),
    path("pagamento/sucesso/", views.pagamento_sucesso, name="pagamento_sucesso"),
]
