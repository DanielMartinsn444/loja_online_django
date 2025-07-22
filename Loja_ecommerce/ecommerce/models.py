# ecommerce/models.py
from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"


class Produto(models.Model):
    nome = models.CharField(max_length=100)

    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)

    imagem = models.ImageField(upload_to="produtos/", blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["nome"]


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrinho de {self.user.username}"

    @property
    def get_cart_total(self):

        cartitems = self.cartitem_set.all()
        total = sum([item.get_total for item in cartitems])
        return total

    class Meta:
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinhos"
        ordering = ["-created_at"]


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):

        return f"{self.quantity} X {self.product.nome} no carrinho de {self.cart.user.username}"

    @property
    def get_total(self):

        return self.quantity * self.price

    class Meta:
        verbose_name = "Item do carrinho"
        verbose_name_plural = "Itens do carrinho"

        unique_together = ("cart", "product")

        ordering = ["cart", "product__nome"]

#colocar as views para atualizar assim que o usuario colocar algo no carrinho, criar view pra finalizar compra através de API