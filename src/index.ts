// src/index.ts
import express from 'express';
import { spinSlots } from './application/slotMachine';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static('public'));

// Rota corrigida (removido o 'req' que não era usado)
app.get('/api/spin', (_, res) => {
  const result = spinSlots();
  res.json(result);
});

app.listen(PORT, () => {
  console.log(`🚀 Servidor rodando em http://localhost:${PORT}`);
});