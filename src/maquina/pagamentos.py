"""Módulo de pagamentos, premiações e cálculo de lucros.

Regras do edital (Seção 6 e 7):
- Há 5^3 = 125 triplas centrais possíveis e equiprováveis (probabilidade 1/125 para cada).
- Apenas a linha central pode gerar pagamento, e exclusivamente quando os 3 símbolos forem iguais.
- Prêmio bruto (P):
    - Tabela Base:
        A-A-A: 5 créditos
        B-B-B: 10 créditos
        C-C-C: 15 créditos
        D-D-D: 25 créditos
        E-E-E: 50 créditos
        Qualquer outra tripla: 0 créditos
    - Tabela Prêmios +10% (Experimento 5):
        A-A-A: 5.5 créditos
        B-B-B: 11.0 créditos
        C-C-C: 16.5 créditos
        D-D-D: 27.5 créditos
        E-E-E: 55.0 créditos
- Lucro líquido do jogador (X):
    X = P - Aposta (onde Aposta = 1)
"""

from typing import Tuple, Dict, Any

# Tabelas de pagamentos estipuladas no edital
TABELA_BASE: Dict[str, float] = {
    "A-A-A": 5.0,
    "B-B-B": 10.0,
    "C-C-C": 15.0,
    "D-D-D": 25.0,
    "E-E-E": 50.0,
}

TABELA_BONUS_10: Dict[str, float] = {
    "A-A-A": 5.5,
    "B-B-B": 11.0,
    "C-C-C": 16.5,
    "D-D-D": 27.5,
    "E-E-E": 55.0,
}


def f_ehTriplaPremiada(linhaCentral: Tuple[str, str, str]) -> bool:
    """Verifica se os três símbolos da linha central são rigorosamente iguais.

    Argumentos:
        linhaCentral (Tuple[str, str, str]): Tripla de símbolos (ex: ('A', 'A', 'A')).

    Retorna:
        bool: True se for premiada, False caso contrário.
    """
    pass


def f_calcularPremioBruto(linhaCentral: Tuple[str, str, str], tabelaPagamentos: Dict[str, float] = TABELA_BASE) -> float:
    """Calcula o prêmio bruto (P) obtido na rodada de acordo com a tabela de pagamentos fornecida.

    Argumentos:
        linhaCentral (Tuple[str, str, str]): Tripla da linha central.
        tabelaPagamentos (Dict[str, float]): Dicionário com os pagamentos das triplas.

    Retorna:
        float: Valor do prêmio P (ex: 5.0, 10.0, ..., ou 0.0 caso não haja vitória).
    """
    pass


def f_calcularLucroLiquido(premioBruto: float, custoAposta: float = 1.0) -> float:
    """Calcula o lucro líquido do jogador (X) na rodada: X = P - custoAposta.

    Argumentos:
        premioBruto (float): Prêmio bruto recebido P.
        custoAposta (float): Custo de entrada na rodada (padrão: 1.0).

    Retorna:
        float: Lucro líquido X (ex: 4.0, 9.0, ..., ou -1.0 em rodadas perdedoras).
    """
    pass


def f_calcularEsperancaTeorica(tabelaPagamentos: Dict[str, float] = TABELA_BASE, custoAposta: float = 1.0) -> Dict[str, float]:
    """Calcula matematicamente os valores esperados teóricos para o modelo:

    - E[P]: Esperança do prêmio bruto = sum(P * (1/125))
    - E[X]: Esperança do lucro líquido = E[P] - custoAposta
    - RTP teórico: E[P] / custoAposta
    - Chance de vitória teórica: 5 / 125 = 0.04 (4%)

    Retorna:
        Dict[str, float]: Dicionário com as métricas teóricas calculadas.
    """
    pass
