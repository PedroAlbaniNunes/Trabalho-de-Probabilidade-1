r"""Módulo de pagamentos, premiações e cálculo de lucros.

Regras do edital (Seção 6 e 7):
- Há 5^3 = 125 triplas centrais possíveis e equiprováveis (probabilidade 1/125 = 0,8% para cada).
- Apenas a linha central pode gerar pagamento, e exclusivamente quando os 3 símbolos forem iguais.
- Prêmio bruto (P):
    - Tabela Base:
        A-A-A: 5 créditos  (probabilidade 1/125 = 0,8%)
        B-B-B: 10 créditos (probabilidade 1/125 = 0,8%)
        C-C-C: 15 créditos (probabilidade 1/125 = 0,8%)
        D-D-D: 25 créditos (probabilidade 1/125 = 0,8%)
        E-E-E: 50 créditos (probabilidade 1/125 = 0,8% - o Grande Jackpot!)
        Qualquer outra combinação: 0 créditos (probabilidade 120/125 = 96,0% - a famosa vala comum)
- Lucro líquido do jogador (X):
    X = P - Aposta (onde Aposta padrão = 1 crédito).
"""

from typing import Tuple, Dict, Any

# Tabelas de pagamentos estipuladas no edital
TABELA_BASE: Dict[str, float] = {
    "A-A-A": 5.0,   # Pagamento modesto
    "B-B-B": 10.0,  # Dá pra comemorar
    "C-C-C": 15.0,  # Pagamento intermediário
    "D-D-D": 25.0,  # Prêmio gordo
    "E-E-E": 50.0,  # O jackpot supremo da máquina!
}

TABELA_BONUS_10: Dict[str, float] = {
    "A-A-A": 5.5,   # Base + 10% de lambuja
    "B-B-B": 11.0,  # Base + 10%
    "C-C-C": 16.5,  # Base + 10%
    "D-D-D": 27.5,  # Base + 10%
    "E-E-E": 55.0,  # Jackpot tunado em 10%
}


def f_ehTriplaPremiada(linhaCentral: Tuple[str, str, str]) -> bool:
    """Verifica se os três símbolos da linha central são rigorosamente idênticos.

    Args:
        linhaCentral (Tuple[str, str, str]): Tripla de símbolos centrais (ex: ('A', 'A', 'A')).

    Returns:
        bool: True se for uma trinca perfeita (bingo!), False se deu mistura de símbolos (perda).
    """
    return linhaCentral[0] == linhaCentral[1] == linhaCentral[2]  # Cravou os 3 iguais? Se sim, solta os fogos! Se não, chora na cama


def f_calcularPremioBruto(linhaCentral: Tuple[str, str, str], tabelaPagamentos: Dict[str, float] = TABELA_BASE) -> float:
    """Calcula o prêmio bruto (P) obtido na rodada conforme a tabela de pagamentos.

    Args:
        linhaCentral (Tuple[str, str, str]): Tripla de símbolos da linha central.
        tabelaPagamentos (Dict[str, float]): Dicionário com as recompensas (padrão: TABELA_BASE).

    Returns:
        float: Valor do prêmio bruto P pago na rodada (0.0 caso não seja tripla).
    """
    if f_ehTriplaPremiada(linhaCentral):  # Se a sorte sorriu e bateu trinca
        chave = f"{linhaCentral[0]}-{linhaCentral[1]}-{linhaCentral[2]}"  # Monta a etiqueta (ex: 'E-E-E') pra puxar o dindin
        return float(tabelaPagamentos.get(chave, 0.0))  # Pega o valor na tabela de premiação
    return 0.0  # Se não deu trinca, a máquina não solta nem um tostão furado


def f_calcularLucroLiquido(premioBruto: float, custoAposta: float = 1.0) -> float:
    """Calcula o lucro líquido do jogador (X) na rodada: X = P - custoAposta.

    Args:
        premioBruto (float): Prêmio bruto P recebido na rodada.
        custoAposta (float): Custo cobrado pela rodada (padrão do edital: 1.0 crédito).

    Returns:
        float: Lucro líquido X (positivo se for vitória, ou -1.0 em rodadas perdedoras).
    """
    return float(premioBruto - custoAposta)  # Desconta o ingresso: o que interessa é o que sobra limpo no bolso


def f_calcularEsperancaTeorica(tabelaPagamentos: Dict[str, float] = TABELA_BASE, custoAposta: float = 1.0) -> Dict[str, float]:
    r"""Calcula as métricas probabilísticas teóricas exatas para o modelo da máquina.

    Calcula matematicamente:
    - E[P] = sum(P_k * (1/125)) para as 5 triplas premiadas.
    - E[X] = E[P] - custoAposta.
    - RTP teórico (%) = (E[P] / custoAposta) * 100.
    - Chance teórica de vitória (%) = (5 / 125) * 100 = 4.0%.

    Args:
        tabelaPagamentos (Dict[str, float]): Dicionário com os pagamentos das triplas.
        custoAposta (float): Custo de entrada na rodada (padrão: 1.0).

    Returns:
        Dict[str, float]: Dicionário com as grandezas teóricas canônicas.
    """
    soma_premios = sum(tabelaPagamentos.values())  # Soma todas as premiações possíveis das 5 trincas
    esperanca_premio = soma_premios / 125.0  # Pondera pela probabilidade 1/125 de cada trinca acontecer
    esperanca_lucro = esperanca_premio - custoAposta  # Subtrai a aposta: o famoso retorno esperado negativo!
    rtp_teorico = (esperanca_premio / custoAposta) * 100.0  # Porcentagem que o jogo teoricamente devolve aos apostadores
    prob_vitoria_pct = (5.0 / 125.0) * 100.0  # Apenas 5 combinações em 125 pagam alguma coisa (ridículos 4%)

    return {
        "esperanca_premio": esperanca_premio,  # Média que a máquina cospe por rodada
        "esperanca_lucro": esperanca_lucro,    # O prejuízo médio do apostador por rodada (-0.16 na base)
        "rtp_teorico_pct": rtp_teorico,        # Retorno ao jogador (84% na base)
        "prob_vitoria_pct": prob_vitoria_pct,  # A chance de levar qualquer prêmio (4%)
    }
