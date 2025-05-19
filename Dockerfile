FROM oraclelinux:8-slim

# Instala Oracle Instant Client via repositórios oficiais
RUN microdnf install -y oracle-release-el8  && microdnf install -y oracle-instantclient23.8-basic oracle-instantclient23.8-sqlplus  && microdnf clean all

ENV LD_LIBRARY_PATH=/usr/lib/oracle/23.8/client64/lib

WORKDIR /app
COPY package.json index.js .env.example .gitignore Dockerfile ./
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]