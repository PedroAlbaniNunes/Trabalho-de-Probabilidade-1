r"""Extra 2: Mesma Média, Riscos Diferentes (Seção 10 do Edital — até 4 pontos).

Requisitos do edital:
- Construir outra tabela de pagamentos com o mesmo RTP da base (84,00%) e dispersão diferente.
- Conferir analiticamente a igualdade das esperanças (E[P] = 0,84 e E[X] = -0,16).
- Comparar as distribuições teóricas/empíricas e o comportamento dos saldos finais.
"""

from typing import Dict, Any, List
import math
import random

from src.configuracao import (
    SEMENTE_EXP1,
    RODADAS_EXP1,
    SEMENTE_EXP3,
    NUMERO_JOGADORES_EXP3,
    SALDO_INICIAL_EXP3,
    MAX_RODADAS_EXP3,
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
    f_calcularEsperancaTeorica,
    TABELA_BASE,
)
from src.analise.metricas import (
    f_calcularMediaAmostral,
    f_calcularDesvioPadraoAmostral,
    f_calcularMediana,
)
from src.analise.exportador import f_exportarParaCsv
from src.extras.graficos_extras import f_plotarRiscosDiferentesExtra2

# Todas as 3 tabelas abaixo possuem soma dos 5 prêmios exatamente igual a 105 créditos:
# E[P] = 105 / 125 = 0,84 crédito | RTP = 84,00% | E[X] = -0,16 crédito.
TABELA_BAIXA_VOLATILIDADE: Dict[str, float] = {
    "A-A-A": 21.0,  # sem sustos: qualquer trinca paga exatamente 21 créditos
    "B-B-B": 21.0,
    "C-C-C": 21.0,
    "D-D-D": 21.0,
    "E-E-E": 21.0,
}

TABELA_ALTA_VOLATILIDADE: Dict[str, float] = {
    "A-A-A": 1.0,   # prêmio de consolação que só devolve a ficha da aposta
    "B-B-B": 2.0,   # lucro mínimo
    "C-C-C": 2.0,   # outro prêmio mirrado
    "D-D-D": 10.0,  # prêmio intermediário
    "E-E-E": 90.0,  # super jackpot concentrado: a isca perfeita para redes sociais!
}


def f_calcularVarianciaEDesvioTeorico(
    tabelaPagamentos: Dict[str, float],
    custoAposta: float = CUSTO_APOSTA
) -> Dict[str, float]:
    r"""Calcula exatamente a esperança E[X], variância teórica Var(X) e desvio-padrão populacional \sigma_X."""
    teoria = f_calcularEsperancaTeorica(tabelaPagamentos, custoAposta)  # calcula E[P], E[X] e RTP
    esp_x = teoria["esperanca_lucro"]                                   # esperança do lucro (-0,16 nas três tabelas)

    # As 5 triplas premiadas têm probabilidade 1/125 cada; a derrota (X = -custoAposta) tem 120/125.
    var_x = 0.0
    for premio in tabelaPagamentos.values():
        lucro_k = premio - custoAposta                  # lucro líquido associado aquela tripla
        var_x += ((lucro_k - esp_x) ** 2) * (1.0 / 125.0)  # pondera o desvio quadrático por 1/125

    lucro_perda = -custoAposta                          # nas 120 combinações sem prêmio, o lucro é -1
    var_x += ((lucro_perda - esp_x) ** 2) * (120.0 / 125.0)  # soma a parcela de variância das derrotas
    dp_x = math.sqrt(var_x)                             # raiz quadrada para obter o desvio-padrão em créditos

    return {
        "esperanca_premio": teoria["esperanca_premio"],
        "esperanca_lucro": esp_x,
        "rtp_teorico_pct": teoria["rtp_teorico_pct"],
        "variancia_teorica": var_x,
        "dp_teorico": dp_x,
    }


def f_executarExtra2RiscosDiferentes() -> Dict[str, Any]:
    r"""Executa a comparação completa entre tabelas de pagamentos de mesma média e riscos diferentes.

    Avalia os três perfis (Baixa Volatilidade, Base Moderada e Alta Volatilidade):
    1. Analiticamente (conferindo igualdade de E[P]=0,84, E[X]=-0,16 e RTP=84% com diferentes \sigma_X).
    2. Empiricamente nas 10.000 rodadas da semente 2026.
    3. Empiricamente na simulação de 100 jogadores com saldo limitado (B_0 = 100, até 500 giros, semente 42).
    """
    perfis = [
        ("Baixa Volatilidade", TABELA_BAIXA_VOLATILIDADE, "(21, 21, 21, 21, 21)"),
        ("Base (Moderada)", TABELA_BASE, "(5, 10, 15, 25, 50)"),
        ("Alta Volatilidade", TABELA_ALTA_VOLATILIDADE, "(1, 2, 2, 10, 90)"),
    ]

    # 1. Sorteia a sequência canônica de 10.000 linhas centrais da semente 2026 uma única vez
    gerador_10k = random.Random(SEMENTE_EXP1)
    linhas_10k = [f_extrairLinhaCentral(f_sortearTabuleiro3x3(gerador_10k)) for _ in range(RODADAS_EXP1)]

    resumo_perfis: List[Dict[str, Any]] = []
    saldos_por_perfil: Dict[str, List[float]] = {}

    for nome_perfil, tabela, desc_premios in perfis:
        metricas_teo = f_calcularVarianciaEDesvioTeorico(tabela, CUSTO_APOSTA)  # parâmetros teóricos do perfil

        # Avaliação pareada nos 10.000 giros (semente 2026)
        lucros_10k = [
            f_calcularLucroLiquido(f_calcularPremioBruto(lc, tabela), CUSTO_APOSTA)
            for lc in linhas_10k
        ]
        media_obs_10k = f_calcularMediaAmostral(lucros_10k)         # lucro médio observado em 10.000 giros
        dp_obs_10k = f_calcularDesvioPadraoAmostral(lucros_10k)     # dispersão empírica observada
        rtp_obs_10k = (media_obs_10k + CUSTO_APOSTA) * 100.0        # RTP observado na amostra de 10k

        # Simulação de 100 jogadores com saldo inicial B0 = 100 e limite de 500 rodadas (semente 42)
        gerador_jog = random.Random(SEMENTE_EXP3)  # reinicia na semente 42 para comparar os mesmos sorteios base
        saldos_finais: List[float] = []
        rodadas_jogadas_lista: List[int] = []
        n_ruina = 0
        n_ganho = 0

        for _ in range(NUMERO_JOGADORES_EXP3):
            saldo = float(SALDO_INICIAL_EXP3)  # todo jogador começa com 100 créditos
            rodadas = 0
            while rodadas < MAX_RODADAS_EXP3 and saldo >= 1.0:
                lc = f_extrairLinhaCentral(f_sortearTabuleiro3x3(gerador_jog))  # sorteia a linha central
                premio = f_calcularPremioBruto(lc, tabela)                      # aplica a tabela do perfil atual
                saldo += f_calcularLucroLiquido(premio, CUSTO_APOSTA)           # atualiza o saldo
                rodadas += 1
            saldos_finais.append(saldo)
            rodadas_jogadas_lista.append(rodadas)
            if saldo < 1.0:
                n_ruina += 1                   # faliu antes de completar os 500 giros
            if saldo > SALDO_INICIAL_EXP3:
                n_ganho += 1                   # encerrou a sessão no lucro (> 100 créditos)

        saldos_por_perfil[nome_perfil] = saldos_finais

        resumo_perfis.append({
            "nome_perfil": nome_perfil,
            "desc_premios": desc_premios,
            "esperanca_premio": metricas_teo["esperanca_premio"],
            "esperanca_lucro": metricas_teo["esperanca_lucro"],
            "rtp_teorico_pct": metricas_teo["rtp_teorico_pct"],
            "variancia_teorica": metricas_teo["variancia_teorica"],
            "dp_teorico": metricas_teo["dp_teorico"],
            "media_obs_10k": media_obs_10k,
            "dp_obs_10k": dp_obs_10k,
            "rtp_obs_10k": rtp_obs_10k,
            "media_saldo_final": f_calcularMediaAmostral(saldos_finais),
            "mediana_saldo_final": f_calcularMediana(saldos_finais),  #spoiler: a mediana continua 0,00 em todas!
            "dp_saldo_final": f_calcularDesvioPadraoAmostral(saldos_finais),
            "max_saldo_final": max(saldos_finais),
            "media_rodadas": f_calcularMediaAmostral(rodadas_jogadas_lista),
            "taxa_ruina_pct": (n_ruina / NUMERO_JOGADORES_EXP3) * 100.0,
            "prop_ganho_pct": (n_ganho / NUMERO_JOGADORES_EXP3) * 100.0,
        })

    # Conferência analítica de igualdade estrita de esperanças (-0,16 e 84%)
    esperancas_iguais = all(
        math.isclose(p["esperanca_lucro"], -0.16, abs_tol=1e-9)
        and math.isclose(p["rtp_teorico_pct"], 84.0, abs_tol=1e-9)
        for p in resumo_perfis
    )

    cabecalhos = [
        "Perfil de Risco",
        "Prêmios (A..E)",
        "E[X] / RTP Teo.",
        "DP Teórico (σ)",
        "DP Obs. (10k)",
        "Saldo Médio (E3)",
        "Mediana (E3)",
        "Saldo Máx.",
        "Ruína (%)",
        "Ganho (%)",
    ]
    linhas_tabela: List[List[Any]] = []
    for p in resumo_perfis:
        linhas_tabela.append([
            p["nome_perfil"],
            p["desc_premios"],
            f"{p['esperanca_lucro']:+.2f} ({p['rtp_teorico_pct']:.0f}%)",
            f"{p['dp_teorico']:.4f}",
            f"{p['dp_obs_10k']:.4f}",
            f"{p['media_saldo_final']:.2f}",
            f"{p['mediana_saldo_final']:.2f}",
            f"{p['max_saldo_final']:.0f}",
            f"{p['taxa_ruina_pct']:.1f}%",
            f"{p['prop_ganho_pct']:.1f}%",
        ])

    caminho_csv = DIRETORIO_TABELAS_EXTRAS / "extra2_riscos_diferentes.csv"
    f_exportarParaCsv(caminho_csv, cabecalhos, linhas_tabela)  # exporta a tabela comparativa de risco

    caminho_figura = DIRETORIO_FIGURAS_EXTRAS / "extra2_riscos_diferentes.png"
    f_plotarRiscosDiferentesExtra2(saldos_por_perfil, resumo_perfis, caminho_figura)  # plota boxplots e barras

    return {
        "esperancas_iguais": esperancas_iguais,
        "resumo_perfis": resumo_perfis,
        "saldos_por_perfil": saldos_por_perfil,
        "cabecalhos": cabecalhos,
        "linhas_tabela": linhas_tabela,
        "caminho_csv": caminho_csv,
        "caminho_figura": caminho_figura,
    }
