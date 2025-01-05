# Usar uma imagem base com Python
FROM python:3.11-slim

# Definir variáveis de ambiente para evitar interações durante a instalação
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Instalar dependências do sistema necessárias para o Playwright
RUN apt-get update && apt-get install -y \
    wget \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libxss1 \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de requisitos e instalar dependências Python
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar as dependências dos navegadores do Playwright
RUN playwright install --with-deps

# Copiar o código da aplicação
COPY app/ .

# Expor a porta da API
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
