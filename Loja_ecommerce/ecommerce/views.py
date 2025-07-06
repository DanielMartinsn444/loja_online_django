from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Produto, CartItem, Cart
from django.http import JsonResponse, HttpResponse 
from django.contrib.auth.decorators import login_required

def cadastro_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Conta criada para {username}! faça login agora. "
            )
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "ecommerce/cadastro.html", {"form": form})


def login_usuario(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"Você está logado como {username}.")
                return redirect("home")
            else:
                messages.error(request, "Nome de usuário ou senha inválidos.")
        else:
            messages.error(request, "Nome de usuário ou senha inválidos.")
    else:
        form = AuthenticationForm()

    return render(request, "ecommerce/login.html", {"form": form})


def logout_usuario(request):
    logout(request)
    messages.info(request, "Você foi desconectado.")
    return redirect("login")


def home(request):
    return render(request, "ecommerce/home.html")


@login_required 
def ver_carrinho(request):
   
    cart, created = Cart.objects.get_or_create(user=request.user)

   
    cart_items = CartItem.objects.filter(cart=cart)

    
    total_carrinho = sum(item.get_total for item in cart_items) #criar API de pagamentos no carrinho
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_carrinho': total_carrinho,
    }
    return render(request, 'ecommerce/carrinho.html', context)


def lista_produtos(request):
    produtos = Produto.objects.all()
    context = {'produtos': produtos}
    return render(request, 'ecommerce/produtos.html', context)


@login_required
def adicionar_carrinho(request, produto_id):
    if request.method == "POST":
        produto= get_object_or_404(Produto, id= produto_id)
        cart, created= Cart.objects.get_or_create(user=request.user)
        
        cart_item, item_created= CartItem.objects.get_or_create(
            cart= cart,
            product= produto,
            defaults={'quantity': 1, 'price': produto.preco}
        )
        if not item_created:
         
            if cart_item.quantity < produto.estoque:
                cart_item.quantity += 1
                cart_item.save()
                mensagem = f"{produto.nome} adicionado(s) ao carrinho."
            else:
                mensagem = f"Estoque insuficiente para adicionar mais {produto.nome}."
        else:
            
            if produto.estoque > 0:
                mensagem = f"{produto.nome} adicionado ao carrinho pela primeira vez."
            else:
                cart_item.delete() 
                mensagem = f"Estoque esgotado para {produto.nome}."
                
            return redirect('lista_produtos')
    return redirect('lista_produtos')