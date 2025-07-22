from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Produto, CartItem, Cart
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe

stripe.api_key= settings.STRIPE_SECRET_KEY

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
    produtos_sugestao = Produto.objects.all()
       
    print(f"Produtos encontrados para a home: {produtos_sugestao}") 
    print(f"Quantidade de produtos: {produtos_sugestao.count()}")

    context = {
        'produtos_sugestao': produtos_sugestao
    }
    return render(request, "ecommerce/home.html", context)


def ver_carrinho(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

   
    total_carrinho = cart.get_cart_total 
    
    context = {
        "cart": cart,
        "cart_items": cart_items,
        "total_carrinho": total_carrinho,
    }
    return render(request, "ecommerce/carrinho.html", context)



def lista_produtos(request):
    produtos = Produto.objects.all()
    context = {"produtos": produtos}
    return render(request, "ecommerce/produtos.html", context)



@login_required
def adicionar_carrinho(request, produto_id):
    if request.method == "POST":
        produto = get_object_or_404(Produto, id=produto_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, product=produto, defaults={"quantity": 1, "price": produto.preco}
        )

        if not item_created:
            
            if cart_item.quantity < produto.estoque:
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request, f"{produto.nome} foi adicionado(a) novamente ao carrinho.")
            else:
                messages.warning(request, f"Estoque insuficiente para adicionar mais {produto.nome}.")
        else:
           
            if produto.estoque > 0:
                messages.success(request, f"{produto.nome} adicionado ao carrinho.")
            else:
              
                cart_item.delete() 
                messages.error(request, f"Estoque esgotado para {produto.nome}.")
        
        return redirect("lista_produtos") 

    return redirect("lista_produtos")


@login_required
def remover_item_carrinho(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        messages.info(
            request, f"{cart_item.product.nome} foi removido do seu carrinho."
        )
        return redirect("ver_carrinho")
    return redirect("ver_carrinho")





@login_required
def checkout(request):
    try:
        carrinho = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "Seu carrinho não foi encontrado. Por favor, adicione produtos novamente.")
        return redirect('lista_produtos')

    total_a_pagar = carrinho.get_cart_total # Usando a propriedade do modelo
    
    if total_a_pagar <= 0:
        messages.warning(request, "Seu carrinho está vazio. Adicione Produtos.")
        return redirect('ver_carrinho')

    if request.method == 'GET':
        try:
            # Multiplica por 100 e converte para int para o Stripe (valores em centavos)
            amount_in_cents = int(round(total_a_pagar * 100)) 

            payment_intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency='brl',
                metadata={
                    'user_id': request.user.id,
                    'cart_id': carrinho.id
                },
                # Opcional: para salvar o cartão para futuras compras (exige mais configuração)
                # setup_future_usage='off_session', 
            )

            context = {
                'carrinho': carrinho, # Passa o objeto carrinho para o template
                'client_secret': payment_intent.client_secret,
                'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            }
            return render(request, 'ecommerce/checkout.html', context)

        except stripe.error.StripeError as e:
            messages.error(request, f"Erro ao processar pagamento com Stripe: {e.user_message}")
            print(f"Stripe Error: {e}")
            return redirect('ver_carrinho')
        except Exception as e:
            messages.error(request, f"Ocorreu um erro inesperado: {e}")
            print(f"Erro inesperado no checkout: {e}")
            return redirect('ver_carrinho')
            
    # Se o método não for GET (por exemplo, um POST direto na URL checkout sem JS, o que não deve acontecer)
    return redirect('ver_carrinho')


@login_required
def pagamento_sucesso(request):
    messages.success(request, "Seu pagamento foi processado com sucesso! Obrigado pela compra!")
    try:
        carrinho = Cart.objects.get(user=request.user)
        carrinho.cartitem_set.all().delete()
       
    except Cart.DoesNotExist:
        print("Carrinho não encontrado para o usuário após pagamento bem-sucedido.")
    
    return render(request, 'ecommerce/pagamento_sucesso.html')


@login_required
def pagamento_sucesso(request):
   
    messages.success(request, "Seu pagamento foi processado com sucesso! Obrigado pela compra!")
  
    return render(request, 'ecommerce/pagamento_sucesso.html')
