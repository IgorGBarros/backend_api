# Usando uma imagem oficial do Python
FROM python:3.12-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copiando todos os arquivos do projeto para o container
COPY . /app/

# Instalando dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o script de espera (wait-for-postgres.sh)
COPY wait-for-postgres.sh /app/wait-for-postgres.sh

# Tornar o script executável
RUN chmod +x /app/wait-for-postgres.sh

# Expondo a porta do Django
EXPOSE 8000

# Comando para rodar o script que espera o PostgreSQL e depois inicia o Django
CMD ["/app/wait-for-postgres.sh"]
