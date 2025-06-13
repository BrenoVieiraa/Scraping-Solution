# 1. Comece com a imagem base do Python
FROM python:3.10-slim

# 2. Defina o diretório de trabalho
WORKDIR /app

# 3. Copie APENAS o requirements.txt
COPY requirements.txt .

# 4. Instale as 3 dependências mínimas
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copie o resto do seu código (que no momento é só o main_fastapi.py de teste)
COPY . .

# 6. Comando para iniciar a API
CMD uvicorn main_fastapi:app --host 0.0.0.0 --port ${PORT}