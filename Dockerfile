# Dockerfile
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    && apt-get clean

# Crear directorio de trabajo
WORKDIR /app

# Copiar el proyecto al contenedor
COPY . /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar la aplicación
CMD ["python", "main.py"]
