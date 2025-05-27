require("dotenv").config();
const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const morgan = require("morgan");

const db = require("./app/config/db_connect");
const routes = require("./app/router/manage_router");

const app = express();

// Middleware'ler
app.use(express.json());
app.use(cors());
app.use(helmet());
app.use(morgan("dev"));

// Rotaları bağla
routes(app);

// Veritabanı bağlantısı
db.connect();

const PORT = process.env.PORT || 8000;
app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
});
