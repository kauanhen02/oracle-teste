# WP-Oracle-Bot

Bot de WhatsApp que consulta o banco Oracle do Mega ERP via Z-API.

## Arquivos

- `index.js` – aplicação Node.js principal.
- `.env.example` – variáveis de ambiente.
- `Dockerfile` – container Docker com Oracle Instant Client via Oracle Linux.
- `.gitignore` – para ignorar node_modules e .env.
- `package.json` – dependências e scripts.

## Configuração

1. Copie `.env.example` para `.env` e preencha:
   - `ZAPI_INSTANCE`, `ZAPI_TOKEN`
   - `DB_USER`, `DB_PASSWORD`, `DB_CONNECT`

2. Build e run Docker:
   ```bash
   docker build -t wp-oracle-bot .
   docker run -d --name wporaclebot --env-file .env -p 3000:3000 wp-oracle-bot
   ```

3. Configure webhook na Z-API apontando para `http://SEU_IP:3000/webhook`.

4. Envie mensagem pelo WhatsApp para testar.
