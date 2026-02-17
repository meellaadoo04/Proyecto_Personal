FROM python:3.11-slim

WORKDIR /app

# Copiar archivos
COPY requirements.txt .
COPY script_pyrogram.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando de inicio
CMD ["python", "script_pyrogram.py"]
