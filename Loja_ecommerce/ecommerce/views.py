from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
def cadastro_usuario(request):
    if request.method == "POST":
         form = UserCreationForm(request.POST)
         if form.is_valid():
             form.save()
             username= form.cleaned_data.get('username')
             messages.success(request, f"Conta criada para {username}! faça login agora. ")
             return redirect('login')
    else: 
        form=UserCreationForm()
    
    return render(request, 'ecommerce/cadastro.html', {"form": form})

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user) 
                messages.info(request, f'Você está logado como {username}.')
                return redirect('home') 
            else: 
                messages.error(request, 'Nome de usuário ou senha inválidos.')
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.') 
    else:
        form = AuthenticationForm()
    
    return render(request, 'ecommerce/login.html', {'form': form})


def logout_usuario(request):
    logout(request) 
    messages.info(request, 'Você foi desconectado.')
    return redirect('login')

def home(request):
    return render(request, 'ecommerce/home.html')