#!/bin/bash
# wait-for-postgres.sh

# Loop para verificar se o PostgreSQL está aceitando conexões na porta 5432
while ! nc -z postgres 5432; do
  echo "Aguardando o PostgreSQL iniciar..."
  sleep 1
done

echo "PostgreSQL iniciado!"

# Executar as migrações do Django e iniciar o servidor
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
