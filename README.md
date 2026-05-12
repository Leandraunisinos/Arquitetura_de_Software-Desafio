# Arquitetura_de_Software-Desafio

Controle Despesas

Como Executar
Passo 1: Instalar o Python e o Flask
Abra o terminal e execute:

# Instalar o Flask
pip install flask

# Ou se tiver pip3
pip3 install flask

Passo 2: Executar a aplicação

# Navegue até a pasta do projeto
cd controle_despesas

# Execute o arquivo principal
python app.py

# Ou
python3 app.py

Passo 3: Acessar no navegador
Abra seu navegador e acesse: http://localhost:5000

# Funcionalidades Implementadas
----------------------------------------------------------------------------------------------------------------------------- 
Regra de Negócio      	                              Implementação                                  	   Local na Arquitetura
------------------------------------------------------------------------------------------------------------------------------
Toda despesa deve ter descrição e valor              Validação no método validar_despesa()                 Model (models.py)
------------------------------------------------------------------------------------------------------------------------------
Despesa deve ter data                                Validação no método validar_despesa()                 Model (models.py)
------------------------------------------------------------------------------------------------------------------------------
Usuário pode cadastrar despesas                      Método salvar() + rota /cadastrar                    Controller (app.py)
------------------------------------------------------------------------------------------------------------------------------
Usuário pode remover despesas                        Método remover() + rota /remover/<id>                Controller (app.py)
------------------------------------------------------------------------------------------------------------------------------
Sistema calcula total de despesas                    Método calcular_total()                               Model (models.py)
------------------------------------------------------------------------------------------------------------------------------


# Arquitetura MVC Aplicada
┌─────────────────────────────────────────────────────────┐
│                       VIEW (Templates)                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │  base.html  │  │ index.html  │  │ relatorio.html  │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   CONTROLLER (app.py)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│  │   '/'    │ │'/cadastrar'│ │'/remover'│ │'/relatorio'│  │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                     MODEL (models.py)                    │
│  ┌────────────────────────────────────────────────────┐ │
│  │                    Classe Despesa                   │ │
│  │  • validar_despesa()  # RN a e b                   │ │
│  │  • salvar()           # RN c                       │ │
│  │  • remover()          # RN d                       │ │
│  │  • calcular_total()   # RN e                       │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   BANCO DE DADOS                         │
│                      (SQLite)                            │
│                   despesas.db                            │
└─────────────────────────────────────────────────────────┘

# Fluxo de Cadastro de uma Despesa

Usuário → Preenche Formulário → View (index.html)
                                           │
                                           ▼
                              Controller (/cadastrar)
                                           │
                                           ▼
                              Model (valida dados)
                                           │
                              ┌────────────┴────────────┐
                              │           │              │
                           Válido     Inválido        Válido
                              │           │              │
                              ▼           ▼              ▼
                           Salva     Retorna       Salva no
                           no DB      erro         Banco DB
                              │                       │
                              ▼                       ▼
                        Retorna para    ←───   Sucesso/Mensagem
                        página inicial
                              │
                              ▼
                        View atualizada
                        com nova despesa
                              │
                              ▼
                          Usuário vê
                          lista atualizada

# Usuário → Preenche Formulário → View (index.html)
                                           │
                                           ▼
                              Controller (/cadastrar)
                                           │
                                           ▼
                              Model (valida dados)
                                           │
                              ┌────────────┴────────────┐
                              │           │              │
                           Válido     Inválido        Válido
                              │           │              │
                              ▼           ▼              ▼
                           Salva     Retorna       Salva no
                           no DB      erro         Banco DB
                              │                       │
                              ▼                       ▼
                        Retorna para    ←───   Sucesso/Mensagem
                        página inicial
                              │
                              ▼
                        View atualizada
                        com nova despesa
                              │
                              ▼
                          Usuário vê
                          lista atualizada
                          

