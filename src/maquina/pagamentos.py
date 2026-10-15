"""Módulo de pagamentos, premiações e cálculo de lucros.

Regras do edital (Seção 6 e 7):
- Há 5^3 = 125 triplas centrais possíveis e equiprováveis (probabilidade 1/125 = 0,8% para cada).
- Apenas a linha central pode gerar pagamento, e exclusivamente quando os 3 símbolos forem iguais.
- Prêmio bruto (P):
    - Tabela Base:
        A-A-A: 5 créditos  (probabilidade 1/125 = 0,8%)
        B-B-B: 10 créditos (probabilidade 1/125 = 0,8%)
        C-C-C: 15 créditos (probabilidade 1/125 = 0,8%)
        D-D-D: 25 créditos (probabilidade 1/125 = 0,8%)
        E-E-E: 50 créditos (probabilidade 1/125 = 0,8%)
        Qualquer outra combinação: 0 créditos (probabilidade 120/125 = 96,0%)
- Lucro líquido do jogador (X):
    X = P - Aposta (onde Aposta padrão = 1 crédito).
- Valores teóricos canônicos:
    E[P] = (5 + 10 + 15 + 25 + 50) / 125 = 105 / 125 = 0,84 créditos
    E[X] = E[P] - 1 = 0,84 - 1 = -0,16 créditos
    RTP teórico = E[P] / Aposta = 84,0%
    Probabilidade de vitória = 5 / 125 = 4,0%
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
    """Verifica se os três símbolos da linha central são rigorosamente idênticos.

    Argumentos:
        linhaCentral (Tuple[str, str, str]): Tripla de símbolos da linha central (ex: ('A', 'A', 'A')).

    Retorna:
        bool: True se for uma tripla idêntica (premiada), False caso contrário.
    """
    return linhaCentral[0] == linhaCentral[1] == linhaCentral[2]


def f_calcularPremioBruto(linhaCentral: Tuple[str, str, str], tabelaPagamentos: Dict[str, float] = TABELA_BASE) -> float:
    """Calcula o prêmio bruto (P) obtido na rodada de acordo com a tabela de pagamentos fornecida.

    Argumentos:
        linhaCentral (Tuple[str, str, str]): Tripla de símbolos centrais.
        tabelaPagamentos (Dict[str, float]): Dicionário com as recompensas (padrão: TABELA_BASE).

    Retorna:
        float: Valor do prêmio bruto P pago na rodada.
    """
    if f_ehTriplaPremiada(linhaCentral):
        chave = f"{linhaCentral[0]}-{linhaCentral[1]}-{linhaCentral[2]}"
        return float(tabelaPagamentos.get(chave, 0.0))
    return 0.0


def f_calcularLucroLiquido(premioBruto: float, custoAposta: float = 1.0) -> float:
    """Calcula o lucro líquido do jogador (X) na rodada: X = P - custoAposta.

    Argumentos:
        premioBruto (float): Prêmio bruto P recebido na rodada.
        custoAposta (float): Custo cobrado pela rodada (padrão do edital: 1.0 crédito fictício).

    Retorna:
        float: Lucro líquido X da rodada.
    """
    return float(premioBruto - custoAposta)


def f_calcularEsperancaTeorica(tabelaPagamentos: Dict[str, float] = TABELA_BASE, custoAposta: float = 1.0) -> Dict[str, float]:
    """Calcula as métricas probabilísticas teóricas exatas para o modelo da máquina:

    - E[P]: Esperança do prêmio bruto = sum(P_k * (1/125)) para as 5 triplas premiadas.
    - E[X]: Esperança do lucro líquido = E[P] - custoAposta.
    - RTP teórico (%) = (E[P] / custoAposta) * 100.
    - Chance teórica de vitória (%) = (5 / 125) * 100 = 4.0%.

    Argumentos:
        tabelaPagamentos (Dict[str, float]): Dicionário com os pagamentos das triplas.
        custoAposta (float): Custo de entrada na rodada (padrão: 1.0).

    Retorna:
        Dict[str, float]: Dicionário com os parâmetros teóricos calculados.
    """
    soma_premios = sum(tabelaPagamentos.values())
    esperanca_premio = soma_premios / 125.0
    esperanca_lucro = esperanca_premio - custoAposta
    rtp_teorico = (esperanca_premio / custoAposta) * 100.0
    prob_vitoria_pct = (5.0 / 125.0) * 100.0

    return {
        "esperanca_premio": esperanca_premio,
        "esperanca_lucro": esperanca_lucro,
        "rtp_teorico_pct": rtp_teorico,
        "prob_vitoria_pct": prob_vitoria_pct,
    }
