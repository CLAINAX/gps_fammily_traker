# Usa una imagen oficial de Python ligera
FROM python:3.10-slim

# Crea una carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copia los requerimientos y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código de tu proyecto al contenedor
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
