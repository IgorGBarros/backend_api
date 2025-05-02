

---

```markdown
# 🚀 Projeto Django + PostgreSQL com Docker

Este repositório contém um projeto Django integrado com PostgreSQL, rodando de forma isolada usando Docker e Docker Compose.

---

## 📦 Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Git
- Python 3.10+

---

## ✅ Passo a passo: Criação do projeto do zero

### 1. Clone o repositório ou crie a estrutura

```bash
mkdir meu-projeto && cd meu-projeto
git init
```

---

### 2. Crie o diretório `backend` com ambiente Django

```bash
mkdir backend && cd backend
python -m venv venv
source venv/bin/activate
pip install django psycopg2-binary
django-admin startproject core .
```

> Substitua `core` pelo nome do seu projeto.

---

### 3. Gere os arquivos de dependências

```bash
pip freeze > requirements.txt
```

---

## 🐳 Docker: Setup e Execução

### 1. Estrutura esperada

```
.
├── backend/
│   ├── core/
│   ├── manage.py
│   └── requirements.txt
├── .env
├── .env.example
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

### 2. Crie o `.env.example`

```env
DEBUG=True
SECRET_KEY=uma_chave_secreta_segura
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1
POSTGRES_DB=meubanco
POSTGRES_USER=meuusuario
POSTGRES_PASSWORD=senhasecreta
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

---

### 3. Copie para seu `.env`

```bash
cp .env.example .env
```

Edite com suas credenciais.

---

### 4. Dockerfile

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY ./backend /app

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

### 5. docker-compose.yml

```yaml
version: "3.9"

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: .
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  portainer:
    image: portainer/portainer-ce
    container_name: portainer
    ports:
      - "9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    restart: always

  watchtower:
    image: v2tec/watchtower
    container_name: watchtower
    restart: always
    environment:
      - WATCHTOWER_NOTIFICATIONS=slack
      - WATCHTOWER_NOTIFICATION_SLACK_HOOK_URL=https://hooks.slack.com/services/SEU/WEBHOOK
      - WATCHTOWER_NOTIFICATION_SLACK_IDENTIFIER=Servidor Docker
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: --interval 30 --cleanup

volumes:
  pgdata:
  portainer_data:
```

---

## 🚀 Executando o Projeto

### 1. Build dos containers

```bash
docker-compose build
```

### 2. Subindo os serviços

```bash
docker-compose up
```

Acesse:  
- [http://localhost:8000](http://localhost:8000) → Django  
- [http://localhost:9000](http://localhost:9000) → Portainer

---

## 📊 Gerenciamento com Portainer

O **Portainer** é um painel de controle para monitoramento e gerenciamento dos containers Docker via interface web.

### Primeira execução

1. Acesse [http://localhost:9000](http://localhost:9000)
2. Crie seu usuário admin
3. Selecione a opção "Docker local"

Você poderá visualizar, iniciar, parar ou remover containers, volumes e redes com facilidade.

---

## 🔔 Configuração de Notificação com Watchtower e Slack

O **Watchtower** monitorará os containers em execução e irá reiniciá-los automaticamente em caso de falha. Além disso, ele enviará notificações para o Slack em caso de atualizações.

### 1. Criando o Webhook no Slack

1. Acesse seu **Workspace do Slack**.
2. Vá para **Configurações e Administração** → **Gerenciar apps**.
3. Procure por **Incoming Webhooks** e adicione um novo.
4. Selecione o canal desejado e clique em **Adicionar Incoming Webhook**.
5. Copie o **URL do Webhook** gerado.

### 2. Configuração do Watchtower com Slack

No seu arquivo `docker-compose.yml`, a configuração do Watchtower já está incluída, com o webhook do Slack:

```yaml
watchtower:
  image: v2tec/watchtower
  container_name: watchtower
  restart: always
  environment:
    - WATCHTOWER_NOTIFICATIONS=slack
    - WATCHTOWER_NOTIFICATION_SLACK_HOOK_URL=https://hooks.slack.com/services/SEU/WEBHOOK
    - WATCHTOWER_NOTIFICATION_SLACK_IDENTIFIER=Servidor Docker
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock
  command: --interval 30 --cleanup
```

Agora, o Watchtower irá enviar notificações para o Slack sempre que detectar atualizações nos containers.

---

## 🧱 Comandos úteis

### Rodar migrações

```bash
docker-compose exec backend python manage.py migrate
```

### Criar superusuário

```bash
docker-compose exec backend python manage.py createsuperuser
```

### Acessar o shell

```bash
docker-compose exec backend python manage.py shell
```

---

## ⚠️ Segurança `.env`

### Evite comitar seu `.env`

Adicione ao seu `.gitignore`:

```bash
echo ".env" >> .gitignore
```

Se já comitou:

```bash
git rm --cached .env
git commit -m "Remover .env do versionamento"
git push origin main
```

**Para apagar permanentemente:**

```bash
pip install git-filter-repo
git filter-repo --path .env --invert-paths
git push --force
```

> Após isso, **troque todas as senhas e chaves expostas.**

---

## 🧪 Testes

```bash
docker-compose exec backend python manage.py test
```

---

## 🛑 Parar o projeto

```bash
docker-compose down
```

---

## 📌 Dicas de Produção

- Use `DEBUG=False` no `.env`
- Configure `ALLOWED_HOSTS` corretamente
- Use Nginx + Gunicorn
- Use volumes nomeados para persistência
- Proteja variáveis com Vault, AWS Secrets Manager, etc.

---

## 👨‍💻 Autor

**Igor Guimarães Barros**  
Engenheiro Mecatrônico | Desenvolvedor de Software Fullstack | Cientista de Dados  
[LinkedIn](https://www.linkedin.com/in/igor-guimarães-barros)

---

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).
```

---

