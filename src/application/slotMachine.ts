// src/game.ts
import { SymbolType, SpinResult } from "src/interfaces/slotMachineInterface";

const SYMBOLS: SymbolType[] = [
  { id: 'cherry', value: '🍒', multiplier: 2 },
  { id: 'lemon', value: '🍋', multiplier: 3 },
  { id: 'bell', value: '🔔', multiplier: 5 },
  { id: 'diamond', value: '💎', multiplier: 10 },
  { id: 'seven', value: '7️⃣', multiplier: 20 },
];


export function spinSlots(): SpinResult {
  const roleta: SymbolType[] = [];

  for (let i = 0; i < 3; i++) {
    const randomIndex = Math.floor(Math.random() * SYMBOLS.length);
    roleta.push(SYMBOLS[randomIndex]);
  }

  const isWin = roleta[0].id === roleta[1].id && roleta[1].id === roleta[2].id;

  const baseBet = 10; 
  const payout = isWin ? baseBet * roleta[0].multiplier : 0;

  return {
    roleta,
    result: isWin,
    payout,
  };
}