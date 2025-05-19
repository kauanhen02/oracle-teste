FROM node:18-bullseye-slim

# Instala dependências do Oracle Instant Client
RUN apt-get update && apt-get install -y libaio1 unzip wget   && wget https://download.oracle.com/otn_software/linux/instantclient/838000/instantclient-basiclite-linux.x64-23.8.0.0.0dbru.zip   && wget https://download.oracle.com/otn_software/linux/instantclient/838000/instantclient-sdk-linux.x64-23.8.0.0.0dbru.zip   && unzip instantclient-basiclite-linux.x64-23.8.0.0.0dbru.zip -d /opt   && unzip instantclient-sdk-linux.x64-23.8.0.0.0dbru.zip -d /opt   && rm instantclient-*.zip   && ln -s /opt/instantclient_23_8 /opt/instantclient   && echo '/opt/instantclient' > /etc/ld.so.conf.d/oracle-instantclient.conf   && ldconfig

ENV LD_LIBRARY_PATH=/opt/instantclient

WORKDIR /app
COPY package.json index.js .env.example .gitignore Dockerfile ./
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]