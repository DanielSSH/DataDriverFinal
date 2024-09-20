# Usa una imagen base de Python
FROM python:3.11-alpine

# Instala las dependencias del sistema necesarias
RUN apk update && apk add --no-cache \
        gcc \
        musl-dev \
        mariadb-dev \
        mariadb-connector-c-dev \
        libffi-dev \
        openssl-dev \
        libxml2-dev \
        libxslt-dev \
        pkgconfig \
        build-base \
        mariadb-client \
        python3 \
        py3-pip  # Instalación de pip para Python 3

# Copia el archivo de requisitos
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . /app

# Establece el directorio de trabajo
WORKDIR /app

# Comando para ejecutar la aplicación
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]






