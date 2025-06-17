from flask import Flask, jsonify
import oracledb
import os # Importar os para variáveis de ambiente
import logging # Importar logging

# Configuração de logs para a API de produtos
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
# É melhor puxar a porta de variáveis de ambiente também, para flexibilidade no deploy
PORT = int(os.environ.get("PORT", 3000))

# Modo thin (sem Oracle Client instalado)
# Geralmente não se chama init_oracle_client() para modo thin sem client instalado.
# oracledb.init_oracle_client() 

# --- INÍCIO DA RECOMENDAÇÃO DE SEGURANÇA (Credenciais via Variáveis de Ambiente) ---
# Você DEVE configurar estas variáveis no Render.com (ou ambiente de deploy)
DB_USER = os.environ.get("DB_USER", "GINGER") # Default para teste local, mas MUDE em prod
DB_PASSWORD = os.environ.get("DB_PASSWORD", "SF6QxMuKe_") # Default para teste local, mas MUDE em prod
DB_DSN = os.environ.get("DB_DSN", "dbconnect.megaerp.online:4221/xepdb1") # Default para teste local, mas MUDE em prod

# Verificação para garantir que as credenciais foram carregadas
if not all([DB_USER, DB_PASSWORD, DB_DSN]):
    logging.error("❌ Variáveis de ambiente DB_USER, DB_PASSWORD ou DB_DSN não definidas. O servidor não iniciará.")
    exit(1)
# --- FIM DA RECOMENDAÇÃO DE SEGURANÇA ---


# Rota principal
@app.route("/produtos")
def produtos():
    connection = None # Inicializa connection para garantir que esteja definida
    cursor = None # Inicializa cursor para garantir que esteja definida
    try:
        logging.info("Attempting to connect to Oracle database...")
        connection = oracledb.connect(
            user=DB_USER,      # Usando variável de ambiente
            password=DB_PASSWORD, # Usando variável de ambiente
            dsn=DB_DSN,          # Usando variável de ambiente
            mode=oracledb.DEFAULT_AUTH
        )
        logging.info("Successfully connected to Oracle database.")

        cursor = connection.cursor()
        logging.info("Executing SQL query...")
        cursor.execute("""
            SELECT p.PRO_IN_CODIGO, p.PRO_ST_DESCRICAO, c.re_custo
            FROM MEGA.gg_vw_composicao@GINGER c  -- <-- CORRIGIDO AQUI
            INNER JOIN MEGA.gg_vw_produtos@GINGER p  -- <-- CORRIGIDO AQUI
            ON c.PRO_IN_CODIGO = p.PRO_IN_CODIGO
            WHERE LOWER(c.PRO_IN_CODIGO) LIKE '%pr%';
        """)

        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        logging.info(f"Query returned {len(rows)} rows.")
        return jsonify(rows)

    except oracledb.Error as e:
        # Erros específicos do Oracle DB
        error_message = f"Erro no banco de dados: {e}"
        logging.error(f"❌ {error_message}", exc_info=True)
        return jsonify({"erro": error_message}), 500
    except Exception as e:
        # Outros erros inesperados
        error_message = f"Erro inesperado na API de produtos: {e}"
        logging.error(f"❌ {error_message}", exc_info=True)
        return jsonify({"erro": error_message}), 500

    finally:
        if cursor:
            cursor.close()
            logging.info("Cursor closed.")
        if connection:
            connection.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    logging.info(f"🚀 API de Produtos iniciada na porta {PORT}")
    app.run(host="0.0.0.0", port=PORT)
