# Documentação do Projeto Backend

## Visão Geral
Este é um projeto backend desenvolvido em Django, com suporte a Docker e Kubernetes para containerização e orquestração.

## Estrutura do Projeto
```
.
├── Api/                    # Diretório principal da aplicação Django
│   ├── User/              # Módulo de usuários
│   ├── Api/               # Configurações principais do Django
│   ├── manage.py          # Script de gerenciamento do Django
│   ├── requirements.txt   # Dependências do projeto
│   └── Dockerfile        # Configuração do container Docker
├── k8s/                   # Configurações do Kubernetes
├── docker-compose.yml     # Configuração do ambiente Docker
└── README.md             # Documentação principal do projeto
```

## Requisitos do Sistema
- Python 3.x
- Docker
- Docker Compose
- Kubernetes (opcional, para deploy)

## Configuração do Ambiente

### Usando Docker
1. Clone o repositório
2. Execute o comando:
```bash
docker-compose up --build
```

### Desenvolvimento Local
1. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Instale as dependências:
```bash
pip install -r Api/requirements.txt
```

3. Execute as migrações:
```bash
python Api/manage.py migrate
```

4. Inicie o servidor:
```bash
python Api/manage.py runserver
```

## Componentes Principais

### API Django
O projeto utiliza Django como framework principal, com uma estrutura modular que inclui:
- Sistema de autenticação de usuários
- API RESTful
- Banco de dados SQLite (desenvolvimento) / PostgreSQL (produção)

### Containerização
- `Dockerfile`: Define a imagem do container da aplicação
- `docker-compose.yml`: Configura os serviços necessários (API, banco de dados)
- `wait-for-postgres.sh`: Script para garantir que o banco de dados esteja pronto antes de iniciar a aplicação

### Kubernetes
O diretório `k8s/` contém as configurações para deploy em um cluster Kubernetes, incluindo:
- Deployments
- Services
- ConfigMaps
- Secrets

## Desenvolvimento

### Convenções de Código
- Seguir as convenções PEP 8 para Python
- Documentar funções e classes usando docstrings
- Manter o código modular e testável

### Testes
Para executar os testes:
```bash
python Api/manage.py test
```

## Deploy

### Produção
1. Configure as variáveis de ambiente necessárias
2. Execute o deploy usando Kubernetes:
```bash
kubectl apply -f k8s/
```

### Monitoramento
- Logs podem ser acessados via Kubernetes:
```bash
kubectl logs -f deployment/api-deployment
```

## Manutenção

### Backup do Banco de Dados
```bash
python Api/manage.py dumpdata > backup.json
```

### Restauração do Banco de Dados
```bash
python Api/manage.py loaddata backup.json
```

## Suporte
Para questões e suporte, abra uma issue no repositório do projeto. 