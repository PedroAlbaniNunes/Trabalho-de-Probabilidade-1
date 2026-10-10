// src/cli.ts
import { spinSlots } from './application/slotMachine';
import * as readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

console.log('🎰 ======================================== 🎰');
console.log('      BEM-VINDO AO CAÇA-NÍQUEL DO TCC       ');
console.log('🎰 ======================================== 🎰\n');
console.log('Pressione [ENTER] para girar ou digite "sair" para fechar.\n');

function promptUser() {
  rl.question('👉 Pressione ENTER para jogar...', (answer) => {
    if (answer.toLowerCase() === 'sair' || answer.toLowerCase() === 'q') {
      console.log('\nSaindo do jogo. Até logo!');
      rl.close();
      return;
    }

    // Executa a lógica do jogo que criamos
    const result = spinSlots();
    
    // Exibe o resultado formatado no terminal
    console.log('\n----------------------------------------');
    console.log(` 🎲 Resultado: [ ${result.roleta.map(s => s.value).join(' | ')} ]`);
    
    if (result.result) {
      console.log(` 🎉 VITÓRIA! Você ganhou ${result.payout} pontos! 🎉`);
    } else {
      console.log(' ❌ Não foi dessa vez! Tente novamente.');
    }
    console.log('----------------------------------------\n');

    // Repete o ciclo
    promptUser();
  });
}

promptUser();