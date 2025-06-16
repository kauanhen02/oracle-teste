const express = require('express');
const oracledb = require('oracledb');

const app = express();
const PORT = 3000;

app.use((req, res, next) => {
  res.setHeader('ngrok-skip-browser-warning', 'true');
  next();
});

// Oracle Client config
oracledb.initOracleClient({
  libDir: 'C:\\Users\\kauan\\Downloads\\instantclient-basic-windows.x64-23.8.0.25.04\\instantclient_23_8'
});

// Rota GET com filtro "pr"
app.get('/produtos', async (req, res) => {
  let connection;

  try {
    connection = await oracledb.getConnection({
      user: 'GINGER',
      password: 'SF6QxMuKe_',
      connectString: 'dbconnect.megaerp.online:4221/xepdb1'
    });

    const result = await connection.execute(
      `SELECT * FROM MEGA.gg_vw_produtos@GINGER WHERE LOWER(PRO_IN_CODIGO) LIKE '%pr%'`,
      [],
      { outFormat: oracledb.OUT_FORMAT_OBJECT }
    );

    res.json(result.rows);
  } catch (err) {
    console.error('Erro Oracle:', err);
    res.status(500).json({ erro: err.message });
  } finally {
    if (connection) {
      try {
        await connection.close();
      } catch (err) {
        console.error('Erro ao fechar conexão:', err);
      }
    }
  }
});

// Acessível de qualquer rede (se firewall permitir)
const os = require('os');

app.listen(PORT, '0.0.0.0', () => {
  const interfaces = os.networkInterfaces();
  const addresses = [];

  for (let iface of Object.values(interfaces)) {
    for (let config of iface) {
      if (config.family === 'IPv4' && !config.internal) {
        addresses.push(config.address);
      }
    }
  }

  addresses.forEach(addr => {
    console.log(`✅ API acessível em: http://${addr}:${PORT}/produtos`);
  });
});

