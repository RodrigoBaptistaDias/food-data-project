# Usa a imagem Python 3.12 slim, baseada em Debian (como você pediu)
FROM python:3.12-slim

# Etiqueta de metadados
LABEL maintainer="seu-nome"

# 1. ATUALIZAÇÃO DE SEGURANÇA (usando apt-get)
#    Atualiza a lista de pacotes e instala as últimas correções de segurança.
RUN apt-get update && apt-get upgrade -y && \
    # Instala as dependências de build necessárias para alguns pacotes Python
    apt-get install -y --no-install-recommends gcc libc-dev libffi-dev && \
    # Limpa o cache para manter a imagem pequena
    rm -rf /var/lib/apt/lists/*

# 2. CRIAÇÃO DE UM USUÁRIO NÃO-ROOT
#    A sintaxe do Debian é um pouco diferente da do Alpine.
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# 3. INSTALAÇÃO DE DEPENDÊNCIAS
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4. CÓPIA DO CÓDIGO
COPY . .
RUN chown -R appuser:appgroup /app

# 5. CONFIGURAÇÃO FINAL
#    Troca para o usuário não-root.
USER appuser

# Define a variável de ambiente PORT.
ENV PORT=8080

# Comando para iniciar a aplicação.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "-k", "uvicorn.workers.UvicornWorker", "main:app"]