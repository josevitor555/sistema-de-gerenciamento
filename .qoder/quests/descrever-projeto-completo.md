# Sistema de Gerenciamento de Produtos

## Visão Geral

O Sistema de Gerenciamento de Produtos é uma aplicação web desenvolvida em Django que permite o controle completo de um catálogo de produtos, incluindo categorização, gestão de pedidos e autenticação de usuários. O sistema oferece uma interface intuitiva para administradores gerenciarem produtos, categorias e pedidos de forma eficiente.

### Objetivos Principais
- Gerenciar catálogo de produtos com categorização
- Controlar estoque e disponibilidade
- Processar pedidos e itens
- Autenticar e autorizar usuários
- Fornecer interface web responsiva

## Stack Tecnológica

### Backend Framework
- **Django 5.1**: Framework web principal
- **Python**: Linguagem de programação

### Banco de Dados
- **MySQL**: Sistema de gerenciamento de banco de dados relacional
- **PyMySQL**: Driver para conexão Python-MySQL

### Armazenamento de Mídia
- **Cloudinary**: Serviço de armazenamento e otimização de imagens na nuvem

### Autenticação Social
- **Django Allauth**: Autenticação com provedores externos
- **Social Django**: Integração com redes sociais (Google OAuth2)

### Deploy e Hospedagem
- **Vercel**: Plataforma de deploy
- **WhiteNoise**: Servir arquivos estáticos em produção

## Arquitetura do Sistema

### Padrão Arquitetural
O sistema segue o padrão **MTV (Model-Template-View)** do Django:

```mermaid
graph TB
    A[Cliente/Browser] --> B[URLs/Routing]
    B --> C[Views]
    C --> D[Models]
    D --> E[Banco de Dados MySQL]
    C --> F[Templates]
    F --> A
    C --> G[Forms]
    G --> C
    D --> H[Cloudinary Storage]
```

### Estrutura de Diretórios

```
sistema-de-gerenciamento/
├── gerenciamento_de_produto/    # Configurações do projeto
│   ├── settings.py             # Configurações gerais
│   ├── urls.py                 # URLs principais
│   ├── wsgi.py                 # Interface WSGI
│   └── asgi.py                 # Interface ASGI
├── produtos/                   # App principal
│   ├── models.py              # Modelos de dados
│   ├── views.py               # Lógica de negócio
│   ├── forms.py               # Formulários
│   ├── urls.py                # URLs do app
│   ├── admin.py               # Interface admin
│   ├── templates/             # Templates HTML
│   └── migrations/            # Migrações de BD
├── api/                       # API endpoint
├── staticfiles/               # Arquivos estáticos
├── manage.py                  # Gerenciador Django
└── vercel.json               # Configuração Vercel
```

## Modelos de Dados

### Diagrama Entidade-Relacionamento

```mermaid
erDiagram
    Usuario {
        int id PK
        string email UK
        string nome
        string password
        boolean is_staff
        boolean is_active
        boolean is_superuser
    }
    
    Categoria {
        int id PK
        string nome UK
    }
    
    Produto {
        int id PK
        string nome
        text descricao
        string marca
        int quantidade
        decimal valor
        string imagem
        string adicional
        datetime updated_at
    }
    
    ProdutoCategoria {
        int id PK
        int produto_id FK
        int categoria_id FK
    }
    
    Pedido {
        int id PK
    }
    
    ItemPedido {
        int id PK
        int pedido_id FK
        int produto_id FK
        int quantidade
    }
    
    Usuario ||--o{ Pedido : "pode criar"
    Produto ||--o{ ProdutoCategoria : "pertence"
    Categoria ||--o{ ProdutoCategoria : "contém"
    Produto ||--o{ ItemPedido : "incluído em"
    Pedido ||--o{ ItemPedido : "contém"
```

### Descrição dos Modelos

#### Usuario (Modelo de Autenticação Customizado)
- **email**: Email único para login
- **nome**: Nome completo do usuário
- **password**: Senha criptografada
- **is_staff**: Permissão de acesso ao admin
- **is_active**: Status ativo/inativo
- **is_superuser**: Permissões de superusuário

#### Categoria
- **nome**: Nome único da categoria
- Métodos especiais para criação de categorias iniciais

#### Produto
- **nome**: Nome do produto
- **descricao**: Descrição detalhada
- **marca**: Marca do produto (opcional)
- **quantidade**: Estoque disponível
- **valor**: Preço com duas casas decimais
- **imagem**: Imagem armazenada no Cloudinary
- **adicional**: Status (disponível/não disponível)
- **updated_at**: Timestamp de última atualização
- **categorias**: Relacionamento many-to-many com Categoria

#### ProdutoCategoria (Modelo Intermediário)
- Tabela de junção para relacionamento many-to-many
- **produto_id**: Referência ao produto
- **categoria_id**: Referência à categoria

#### Pedido
- Agregador de itens de pedido
- Método para calcular total do pedido

#### ItemPedido
- **pedido_id**: Referência ao pedido
- **produto_id**: Referência ao produto
- **quantidade**: Quantidade do produto no pedido

## Funcionalidades do Sistema

### Autenticação e Autorização

#### Registro de Usuários
- Cadastro com email, nome e senha
- Validação de senha e confirmação
- Verificação de email único
- Criptografia automática de senhas

#### Login/Logout
- Autenticação por email e senha
- Backend customizado para autenticação por email
- Redirecionamento após login/logout
- Controle de sessão

#### Recuperação de Senha
- Sistema de redefinição de senha
- Validação de email existente
- Interface para nova senha

### Gerenciamento de Produtos

#### Cadastro de Produtos
- Formulário completo com validação
- Upload de imagens via Cloudinary
- Seleção de categorias
- Controle de estoque
- Status de disponibilidade

#### Listagem e Busca
- Listagem paginada (10 produtos por página)
- Filtros por categoria e status
- Busca por nome do produto
- Ordenação por data de atualização

#### Edição e Exclusão
- Formulário de edição com dados preenchidos
- Atualização de categorias via modelo intermediário
- Confirmação antes da exclusão
- Mensagens de feedback

### Gerenciamento de Categorias

#### CRUD Completo
- Listagem de todas as categorias
- Criação via formulário ou AJAX
- Edição usando Class-Based Views
- Exclusão com confirmação

#### Funcionalidades Especiais
- Criação de categorias iniciais automaticamente
- Método para buscar ou criar categoria
- Validação de nome único

### Sistema de Pedidos

#### Criação de Pedidos
- Seleção de produtos disponíveis
- Definição de quantidades
- Cálculo automático de totais
- Persistência em sessão

#### Gerenciamento de Itens
- Adição de produtos ao pedido
- Incremento/decremento de quantidades
- Remoção de itens
- Visualização do carrinho

## Interface de Usuário

### Templates e Layout

#### Base Template
- Layout responsivo comum
- Menu de navegação
- Sistema de mensagens
- Inclusão de estilos CSS

#### Templates Específicos
- **login.html**: Formulário de login/registro
- **produto.html**: Listagem de produtos
- **cadastro.html**: Cadastro de produtos
- **editar_produto.html**: Edição de produtos
- **pesquisa.html**: Busca de produtos
- **pedido.html**: Criação de pedidos
- **categoria_*.html**: CRUD de categorias

### Funcionalidades de UI
- Paginação automática
- Filtros dinâmicos
- Mensagens de feedback
- Formulários com validação
- Upload de imagens com preview

## Configurações e Deploy

### Configurações de Banco de Dados
```python
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        default='mysql://cardapio:20232024@localhost:3306/gerenciamento_de_produto'
    )
}
```

### Configurações de Mídia
- Armazenamento via Cloudinary
- Variáveis de ambiente para credenciais
- Fallback para armazenamento local em desenvolvimento

### Deploy na Vercel
- Configuração via `vercel.json`
- Aplicação WSGI em `vercel_app.py`
- Servir arquivos estáticos com WhiteNoise
- Configuração de variáveis de ambiente

## URLs e Roteamento

### Rotas Principais
- `/login/` - Autenticação
- `/cadastro/` - Registro de usuários
- `/produtos/` - Listagem de produtos
- `/produto_novo/` - Cadastro de produtos
- `/pesquisa/` - Busca de produtos
- `/pedido_novo/` - Criação de pedidos
- `/categorias/` - Gerenciamento de categorias
- `/admin/` - Interface administrativa

### Padrões de URL
- Views baseadas em função para operações CRUD básicas
- Class-Based Views para operações de categoria
- Parâmetros dinâmicos para IDs de entidades
- Redirecionamentos automáticos

## Requisitos Funcionais

### RF001 - Autenticação de Usuários
- O sistema deve permitir registro de novos usuários
- O sistema deve autenticar usuários por email e senha
- O sistema deve permitir recuperação de senha

### RF002 - Gerenciamento de Produtos
- O sistema deve permitir cadastro de produtos com todos os atributos
- O sistema deve permitir edição de produtos existentes
- O sistema deve permitir exclusão de produtos
- O sistema deve permitir busca e filtros de produtos

### RF003 - Gerenciamento de Categorias
- O sistema deve permitir criação de categorias
- O sistema deve permitir edição e exclusão de categorias
- O sistema deve associar produtos a múltiplas categorias

### RF004 - Sistema de Pedidos
- O sistema deve permitir criação de pedidos
- O sistema deve calcular totais automaticamente
- O sistema deve gerenciar itens de pedido

### RF005 - Upload e Gerenciamento de Imagens
- O sistema deve permitir upload de imagens de produtos
- O sistema deve armazenar imagens na nuvem (Cloudinary)

## Requisitos Não Funcionais

### RNF001 - Performance
- Tempo de resposta inferior a 3 segundos para operações básicas
- Paginação para listagens com mais de 10 itens
- Otimização de consultas ao banco de dados

### RNF002 - Segurança
- Senhas criptografadas com hash seguro
- Validação de entrada em todos os formulários
- Proteção CSRF ativada
- Autenticação obrigatória para operações sensíveis

### RNF003 - Usabilidade
- Interface responsiva para dispositivos móveis
- Mensagens de feedback claras
- Formulários com validação client-side e server-side
- Navegação intuitiva

### RNF004 - Confiabilidade
- Backup automático via serviços de nuvem
- Logs de erro para debugging
- Tratamento de exceções em todas as operações

### RNF005 - Manutenibilidade
- Código organizado seguindo padrões Django
- Documentação de APIs e modelos
- Migrações de banco de dados versionadas
- Testes unitários para componentes críticos

### RNF006 - Portabilidade
- Deploy em múltiplas plataformas (Vercel, Heroku)
- Configuração via variáveis de ambiente
- Banco de dados configurável (MySQL, PostgreSQL)

### RNF007 - Escalabilidade
- Arquitetura preparada para crescimento
- Armazenamento de mídia externa (Cloudinary)
- Configuração para servidores de produção

## Fluxos de Processo

### Fluxo de Cadastro de Produto

```mermaid
flowchart TD
    A[Usuário Logado] --> B[Acessa Cadastro de Produto]
    B --> C[Preenche Formulário]
    C --> D{Dados Válidos?}
    D -->|Não| E[Exibe Erros]
    E --> C
    D -->|Sim| F[Salva Produto]
    F --> G[Associa Categoria]
    G --> H[Upload Imagem Cloudinary]
    H --> I[Exibe Sucesso]
    I --> J[Volta para Listagem]
```

### Fluxo de Criação de Pedido

```mermaid
flowchart TD
    A[Usuário Logado] --> B[Acessa Criação de Pedido]
    B --> C{Pedido Existe na Sessão?}
    C -->|Não| D[Cria Novo Pedido]
    C -->|Sim| E[Carrega Pedido Existente]
    D --> F[Seleciona Produto]
    E --> F
    F --> G[Define Quantidade]
    G --> H[Adiciona Item ao Pedido]
    H --> I[Atualiza Total]
    I --> J{Mais Produtos?}
    J -->|Sim| F
    J -->|Não| K[Finaliza Pedido]
```

## Testing

### Estratégia de Testes
- Testes unitários para modelos de dados
- Testes de integração para views
- Testes de formulários e validações
- Testes de autenticação e autorização

### Ferramentas de Teste
- Django TestCase para testes unitários
- Django Client para testes de views
- Factory Boy para criação de dados de teste
- Coverage.py para cobertura de código