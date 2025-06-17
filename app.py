from flask import Flask, jsonify
import oracledb

app = Flask(__name__)
PORT = 3000

@app.route("/produtos")
def produtos():
    try:
        connection = oracledb.connect(
            user="GINGER",
            password="SF6QxMuKe_",
            dsn="dbconnect.megaerp.online:4221/xepdb1",
            mode=oracledb.DEFAULT_AUTH
        )

        cursor = connection.cursor()
        cursor.execute("""
            SELECT p.PRO_IN_CODIGO, p.PRO_ST_DESCRICAO, c.re_custo
            FROM MEGA.gg_vw_composicao@GINGER c
            INNER JOIN MEGA.gg_vw_produtos@GINGER p
                ON c.PRO_IN_CODIGO = p.PRO_IN_CODIGO
            WHERE LOWER(TO_CHAR(c.PRO_IN_CODIGO)) LIKE '%pr%'
        """)

        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify(rows)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
