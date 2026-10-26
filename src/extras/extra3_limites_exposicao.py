r"""Extra 3: Limites de Exposição e Regras de Parada (Seção 10 do Edital — até 3 pontos).

Requisitos do edital:
- Comparar duas (ou mais) regras de parada definidas antes de simular.
- Analisar perdas, ganhos e número de rodadas.
- Distinguir exposição ao risco (número médio de rodadas E[T]) de esperança por rodada (E[X] = -0,16),
  ilustrando a Identidade de Wald: E[B_T - B_0] = E[X] * E[T].
"""

from typing import Dict, Any, List, Optional
import random

from src.configuracao import (
    SEMENTE_EXP3,
    NUMERO_JOGADORES_EXP3,
    SALDO_INICIAL_EXP3,
    CUSTO_APOSTA,
    DIRETORIO_TABELAS_EXTRAS,
    DIRETORIO_FIGURAS_EXTRAS,
)
from src.maquina.rolos import (
    f_sortearTabuleiro3x3,
    f_extrairLinhaCentral,
)
from src.maquina.pagamentos import (
    f_calcularPremioBruto,
    f_calcularLucroLiquido,
    TABELA_BASE,
)
from src.analise.metricas import (
    f_calcularMediaAmostral,
    f_calcularMediana,
)
from src.analise.exportador import f_exportarParaCsv
from src.extras.graficos_extras import f_plotarLimitesExposicaoExtra3


def f_simularRegraDeParada(
    nomeRegra: str,
    nomeCurto: str,
    descricaoRegra: str,
    maxRodadas: int,
    stopWinSaldo: Optional[float],
    stopLossSaldo: float,
    semente: int = SEMENTE_EXP3,
    numJogadores: int = NUMERO_JOGADORES_EXP3,
    saldoInicial: float = SALDO_INICIAL_EXP3
) -> Dict[str, Any]:
    r"""Simula 100 participantes virtuais sob uma regra de parada definida a priori.

    Args:
        nomeRegra (str): Identificação completa da regra.
        nomeCurto (str): Rótulo compacto para eixos de gráficos.
        descricaoRegra (str): Explicação dos gatilhos de interrupção.
        maxRodadas (int): Teto de rodadas por sessão.
        stopWinSaldo (Optional[float]): Saldo-alvo para parada por ganho (None se não houver).
        stopLossSaldo (float): Limiar inferior de parada por perda (ex: 1.0 para ruína total, ou 70.0 para Stop-Loss).
        semente (int): Semente do gerador pseudoaleatório (padrão: 42).
        numJogadores (int): Quantidade de sessões simuladas (padrão: 100).
        saldoInicial (float): Saldo de entrada (padrão: 100.0).

    Returns:
        Dict[str, Any]: Estatísticas de ganho, perda, ruína, exposição média e lucro por rodada.
    """
    gerador = random.Random(semente)  # inicia o gerador na semente 42 para parear o fluxo de sorteios

    saldos_finais: List[float] = []       # guarda o saldo com que cada jogador encerrou a sessão
    rodadas_por_jogador: List[int] = []   # registra quantos giros cada jogador permaneceu exposto
    n_ganho = 0
    n_empate = 0
    n_perda = 0
    n_ruina_total = 0

    for _ in range(numJogadores):
        saldo = float(saldoInicial)  # participante entra com 100 créditos no bolso
        rodadas = 0

        while rodadas < maxRodadas and saldo >= 1.0:
            # Verifica gatilhos de parada definidos a priori antes de arriscar mais uma ficha
            if stopWinSaldo is not None and saldo >= stopWinSaldo:
                break  # bateu a meta de ganho (Stop-Win): levanta da cadeira enquanto está lucrando!
            if saldo <= stopLossSaldo and stopLossSaldo >= 1.0:
                break  # atingiu o limite prudencial de perda (Stop-Loss): freia antes de quebrar a banca

            lc = f_extrairLinhaCentral(f_sortearTabuleiro3x3(gerador))  # sorteia a linha central
            premio = f_calcularPremioBruto(lc, TABELA_BASE)             # verifica o prêmio na Tabela Base
            lucro = f_calcularLucroLiquido(premio, CUSTO_APOSTA)        # desconta 1 crédito da aposta
            saldo += lucro                                              # atualiza o saldo da sessão
            rodadas += 1                                                # incrementa o tempo de exposição

        saldos_finais.append(saldo)
        rodadas_por_jogador.append(rodadas)

        if saldo > saldoInicial:
            n_ganho += 1        # saiu com mais créditos do que entrou
        elif saldo == saldoInicial:
            n_empate += 1       # saiu exatamente no zero a zero
        else:
            n_perda += 1        # saiu no prejuízo

        if saldo < 1.0:
            n_ruina_total += 1  # esgotamento completo do saldo (falência total)

    total_rodadas_acumuladas = sum(rodadas_por_jogador)             # volume total de rodadas de todos os 100 jogadores
    soma_lucro_sessoes = sum(s - saldoInicial for s in saldos_finais)  # resultado líquido agregado das 100 sessões
    lucro_medio_por_rodada_obs = (
        soma_lucro_sessoes / total_rodadas_acumuladas if total_rodadas_acumuladas > 0 else 0.0
    )

    media_rodadas = f_calcularMediaAmostral(rodadas_por_jogador)    # exposição média \bar{T}
    media_saldo_final = f_calcularMediaAmostral(saldos_finais)      # média amostral dos saldos finais
    mediana_saldo_final = f_calcularMediana(saldos_finais)          # mediana dos saldos finais
    perda_esperada_wald = -0.16 * media_rodadas                     # perda média teórica pela Identidade de Wald
    saldo_esperado_wald = saldoInicial + perda_esperada_wald        # saldo médio previsto por 100 - 0,16 * \bar{T}

    return {
        "nome_regra": nomeRegra,
        "nome_curto": nomeCurto,
        "descricao_regra": descricaoRegra,
        "prop_ganho_pct": (n_ganho / numJogadores) * 100.0,
        "prop_empate_pct": (n_empate / numJogadores) * 100.0,
        "prop_perda_pct": (n_perda / numJogadores) * 100.0,
        "taxa_ruina_pct": (n_ruina_total / numJogadores) * 100.0,
        "media_rodadas": media_rodadas,
        "media_saldo_final": media_saldo_final,
        "mediana_saldo_final": mediana_saldo_final,
        "saldo_esperado_wald": saldo_esperado_wald,
        "lucro_medio_por_rodada_obs": lucro_medio_por_rodada_obs,
    }


def f_executarExtra3LimitesExposicao() -> Dict[str, Any]:
    r"""Executa a comparação entre três regras de parada pré-definidas (Extra 3).

    Compara:
    - Regra 1 (Exposição Longa / Padrão E3): Até 500 rodadas ou ruína total (B_t < 1).
    - Regra 2 (Limite Estrito Stop-Win / Stop-Loss): Para se B_t >= 120 (+20%), B_t <= 70 (-30%) ou 200 giros.
    - Regra 3 (Meta Curta Stop-Win Puro): Para se B_t >= 110 (+10%), ruína (B_t < 1) ou 500 giros.
    """
    regras_config = [
        {
            "nome_regra": "Regra 1: Sem Limite (Padrão E3)",
            "nome_curto": "Sem Stop\n(Até 500 giros)",
            "descricao_regra": "T <= 500 ou Ruína (B < 1)",
            "max_rodadas": 500,
            "stop_win": None,
            "stop_loss": 0.0,
        },
        {
            "nome_regra": "Regra 2: Stop-Win (120) + Stop-Loss (70)",
            "nome_curto": "Stop-Win 120\nStop-Loss 70",
            "descricao_regra": "B >= 120, B <= 70 ou T <= 200",
            "max_rodadas": 200,
            "stop_win": 120.0,  # embolsa se fizer +20 créditos
            "stop_loss": 70.0,  # estanca a sangria se perder 30 créditos (zero risco de falência total)
        },
        {
            "nome_regra": "Regra 3: Meta Curta (Stop-Win 110)",
            "nome_curto": "Stop-Win 110\n(Até 500 giros)",
            "descricao_regra": "B >= 110, Ruína (B < 1) ou T <= 500",
            "max_rodadas": 500,
            "stop_win": 110.0,  # qualquer prêmio decente no começo já bate a meta de 110 e encerra
            "stop_loss": 0.0,
        },
    ]

    resultados_regras: List[Dict[str, Any]] = []
    for cfg in regras_config:
        res = f_simularRegraDeParada(
            nomeRegra=cfg["nome_regra"],
            nomeCurto=cfg["nome_curto"],
            descricaoRegra=cfg["descricao_regra"],
            maxRodadas=cfg["max_rodadas"],
            stopWinSaldo=cfg["stop_win"],
            stopLossSaldo=cfg["stop_loss"],
        )
        resultados_regras.append(res)  # acumula o resultado da regra simulada

    cabecalhos = [
        "Regra de Parada",
        "Critério A Priori",
        "Exposição Média (T̄)",
        "Ganho (%)",
        "Perda (%)",
        "Ruína (%)",
        "Saldo Médio (B̄f)",
        "Mediana (Md)",
        "Ref. Wald (100-0,16·T̄)",
        "Lucro/Giro Obs.",
    ]
    linhas_tabela: List[List[Any]] = []
    for r in resultados_regras:
        linhas_tabela.append([
            r["nome_regra"],
            r["descricao_regra"],
            f"{r['media_rodadas']:.2f} giros",
            f"{r['prop_ganho_pct']:.1f}%",
            f"{r['prop_perda_pct']:.1f}%",
            f"{r['taxa_ruina_pct']:.1f}%",
            f"{r['media_saldo_final']:.2f}",
            f"{r['mediana_saldo_final']:.2f}",
            f"{r['saldo_esperado_wald']:.2f}",
            f"{r['lucro_medio_por_rodada_obs']:+.4f}",
        ])

    caminho_csv = DIRETORIO_TABELAS_EXTRAS / "extra3_limites_exposicao.csv"
    f_exportarParaCsv(caminho_csv, cabecalhos, linhas_tabela)  # grava a tabela comparativa em CSV

    caminho_figura = DIRETORIO_FIGURAS_EXTRAS / "extra3_limites_exposicao.png"
    f_plotarLimitesExposicaoExtra3(resultados_regras, caminho_figura)  # gera o gráfico duplo de exposição e desfechos

    return {
        "resultados_regras": resultados_regras,
        "cabecalhos": cabecalhos,
        "linhas_tabela": linhas_tabela,
        "caminho_csv": caminho_csv,
        "caminho_figura": caminho_figura,
    }
