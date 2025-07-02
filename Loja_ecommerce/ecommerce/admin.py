from django.contrib import admin
from .models import Perfil, Produto, Cart, CartItem

admin.site.register(Perfil)
admin.site.register(Produto)
admin.site.register(Cart)
admin.site.register(CartItem)
