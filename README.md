

Este é um projeto de e-commerce desenvolvido com o framework Django, projetado para ser uma plataforma robusta e escalável para vendas online. O objetivo principal foi criar uma aplicação web completa, desde o gerenciamento de produtos até o sistema de autenticação de usuários e carrinho de compras.

## Visão Geral do Projeto

A **Wareshop** é uma aplicação web que simula um ambiente de e-commerce, permitindo que usuários naveguem por produtos, adicionem itens ao carrinho e gerenciem suas contas. O projeto foi construído com foco em boas práticas de desenvolvimento, modularidade e responsividade, garantindo uma experiência de usuário fluida tanto em desktops quanto em dispositivos móveis.

A interface principal apresenta um design limpo e intuitivo, com destaque para a seção de "Sugestões para Você", que inicialmente exibe "Nenhuma sugestão de produto disponível no momento" em um ambiente recém-implantado.



Para interagir com o carrinho de compras ou realizar uma compra, é necessário criar uma conta ou fazer login, garantindo uma experiência personalizada e segura para o usuário. Quando o usuário não está logado, a navegação exibe opções genéricas. **No entanto, ao realizar o login, o site saúda o usuário com seu nome registrado, personalizando a experiência.**

## Funcionalidades Principais

* **Catálogo de Produtos:** Exibição de produtos com detalhes como nome, preço e descrição. Embora a seção de sugestões esteja inicialmente vazia (após um deploy limpo), os produtos aparecem normalmente quando cadastrados.
* **Carrinho de Compras Personalizado:** Cada usuário logado possui um carrinho de compras **único e exclusivo (relação one-to-one)**, onde pode adicionar e remover produtos. Os itens são armazenados individualmente para cada sessão de usuário.
* **Lista de Produtos Salvos (para o Usuário):** Similar ao carrinho, há uma funcionalidade (implícita na descrição "lista de produtos que exibe tudo que você salvou") que permite ao usuário visualizar produtos de seu interesse ou que foram adicionados anteriormente, mantendo essa lista **única para cada conta**.
* **Autenticação de Usuários:** Sistema completo de registro (`/cadastro/`), login (`/login/`) e logout. O sistema reconhece o usuário e personaliza a interface com o nome após o login.
* **Navegação Simplificada:** Inclui um botão "Home" para fácil retorno à página principal, garantindo uma navegação intuitiva.
* **Painel Administrativo:** Acesso a um painel robusto para gerenciamento de produtos, usuários e pedidos (acessível via `/admin/` após a criação de um superusuário).
* **Design Responsivo:** Interface otimizada para diferentes tamanhos de tela (desktop, tablet, mobile), com um layout que se adapta perfeitamente, sem quebras.

## Tecnologias Utilizadas

* **Backend:** ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ,![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
* **Banco de Dados:** SQLite (em desenvolvimento), PostgreSQL (em produção no Render.com)
* **Frontend:** ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white), ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white), ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
* **Hospedagem/Deploy:** Render.com

## Acesso à Aplicação Online

Você pode acessar a versão live deste projeto através do seguinte link:

[**Acessar Loja Online Django**](https://loja-online-django.onrender.com)

## Como Rodar o Projeto Localmente

Para configurar e rodar este projeto em sua máquina local, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
    cd SEU_REPOSITORIO
    ```
    *(Lembre-se de substituir `SEU_USUARIO` e `SEU_REPOSITORIO` pelos dados corretos do seu GitHub)*

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o banco de dados:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Crie um superusuário (para acessar o painel admin):**
    ```bash
    python manage.py createsuperuser
    ```
    Siga as instruções para criar seu nome de usuário, e-mail e senha.

6.  **Colete os arquivos estáticos:**
    ```bash
    python manage.py collectstatic --noinput
    ```

7.  **Inicie o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

Agora você pode acessar a aplicação em seu navegador através de `http://127.0.0.1:8000/`.

## Contribuição

Contribuições são bem-vindas! Se você tiver sugestões ou quiser reportar um bug, por favor, abra uma issue ou envie um pull request.

## Licença

Este projeto está licenciado sob a [Licença MIT](LINK_PARA_LICENCA_MIT_SE_TIVER).

---
