export interface SymbolType {
    id: string; //valor numerico da parada
    value: string; //aparencia só
    multiplier: number; //o quanto ela multiplica seu pagamento
}

export interface SpinResult {
    roleta: SymbolType[]; //a saída na roleta
    result: boolean; // se é vitória ou derrota
    payout: number; //o valor que o caba colocou * o multiplier de cima
}