require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const oracledb = require('oracledb');
const axios = require('axios');

const app = express();
app.use(bodyParser.json());

// Configuração do pool Oracle
oracledb.createPool({
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  connectString: process.env.DB_CONNECT,
  poolMin: 1,
  poolMax: 5,
  poolIncrement: 1
});

async function queryFragranciasNotas(palavraChave) {
  const pool = await oracledb.getPool();
  const conn = await pool.getConnection();
  try {
    const sql = `
      SELECT nome
        FROM fr_shelf
       WHERE LOWER(notas) LIKE :kw
    `;
    const { rows } = await conn.execute(
      sql,
      { kw: '%' + palavraChave.toLowerCase() + '%' },
      { outFormat: oracledb.OUT_FORMAT_OBJECT }
    );
    return rows.map(r => r.NOME);
  } finally {
    await conn.close();
  }
}

async function sendWhatsApp(to, text) {
  await axios.post(process.env.ZAPI_URL, {
    phone: to,
    message: text
  }, {
    headers: { 'x-api-key': process.env.ZAPI_TOKEN }
  });
}

app.post('/webhook', async (req, res) => {
  const { from, body } = req.body;
  console.log(`<- ${from}: ${body}`);
  let reply = 'Desculpe, não entendi sua pergunta.';

  const match = body.match(/fragrancias.*notas de (\w+)/i);
  if (match) {
    const nota = match[1];
    try {
      const lista = await queryFragranciasNotas(nota);
      if (lista.length) {
        reply = 'Fragrâncias com nota de ' + nota + ':\n' +
                lista.map((n, i) => `${i+1}. ${n}`).join('\n');
      } else {
        reply = `Nenhuma fragrância com nota de ${nota} encontrada.`;
      }
    } catch (err) {
      console.error(err);
      reply = 'Erro ao consultar o banco: ' + err.message;
    }
  }

  try {
    await sendWhatsApp(from, reply);
    console.log(`-> ${from}: ${reply}`);
    res.sendStatus(200);
  } catch (err) {
    console.error('Erro Z-API:', err.message);
    res.sendStatus(500);
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Bot rodando na porta ${PORT}`));