#!/bin/bash
set -e

echo "Aguardando o PostgreSQL iniciar..."

# Loop até conseguir conectar na porta 5432 do host 'postgres'
while ! timeout 1 bash -c "</dev/tcp/postgres-service.app-ns.svc.cluster.local/5432" 2>/dev/null; do

  echo "PostgreSQL não está pronto - aguardando..."
  sleep 1
done

echo "PostgreSQL iniciado!"

echo "Aplicando migrações Django..."
python manage.py migrate

echo "Iniciando servidor Gunicorn..."
exec gunicorn Api.wsgi:application --bind 0.0.0.0:8000

