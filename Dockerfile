FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && \
    apt-get install -y unzip libaio1 curl && \
    apt-get clean

# Baixar Oracle Instant Client
RUN curl -O https://download.oracle.com/otn_software/linux/instantclient/2111000/instantclient-basiclite-linux.x64-21.11.0.0.0dbru.zip && \
    unzip instantclient-basiclite-linux.x64-21.11.0.0.0dbru.zip -d /opt/oracle && \
    rm instantclient-basiclite-linux.x64-21.11.0.0.0dbru.zip && \
    ln -s /opt/oracle/instantclient_21_11 /opt/oracle/instantclient

ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_21_11

# Instalar Python libs
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar app
COPY . .

# Expor porta
EXPOSE 10000
CMD ["python", "app.py"]
