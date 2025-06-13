# Usar uma imagem base leve do Python 3.10
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# --- NOVO: Instala o Google Chrome e suas dependências ---
# Atualiza a lista de pacotes e instala as ferramentas necessárias
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    # Adiciona a chave de assinatura do Google
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    # Adiciona o repositório oficial do Chrome
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    # Atualiza a lista de pacotes novamente para incluir o do Chrome
    && apt-get update \
    # Instala a versão estável do Google Chrome
    && apt-get install -y google-chrome-stable \
    # Limpa o cache para manter a imagem do container menor
    && rm -rf /var/lib/apt/lists/*
# --- FIM DA SEÇÃO NOVA ---

# Copia o arquivo de dependências primeiro
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código da sua aplicação para o container
COPY . .

# Expõe a porta que o Uvicorn usará
EXPOSE 8000

# Comando para iniciar a aplicação quando o container iniciar
CMD uvicorn main_fastapi:app --host 0.0.0.0 --port ${PORT}