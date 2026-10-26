r"""Extra 4: Análise de Sensibilidade (Seção 10 do Edital — até 3 pontos).

Requisitos do edital:
- Variar pagamentos ou probabilidades em pelo menos cinco cenários (implementamos 7 cenários).
- Explicar como a esperança matemática (E[P], E[X]) e o RTP mudam em cada configuração.
- Ir além das duas tabelas do Experimento 5, explorando tanto variações escalares de pagamentos
  (incluindo o ponto de equilíbrio E[X]=0 e cenário favorável E[X]>0) quanto alterações estruturais
  nas probabilidades dos rolos.
"""

from typing import Dict, Any, List, Sequence
import random

from src.configuracao import (
    SEMENTE_EXP1,
    RODADAS_EXP1,
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
)
from src.analise.exportador import f_exportarParaCsv
from src.extras.graficos_extras import f_plotarAnaliseSensibilidadeExtra4


def f_simularRoloCustomizado(
    simbolosRolo: Sequence[str],
    tabelaPagamentos: Dict[str, float],
    semente: int = SEMENTE_EXP1,
    nRodadas: int = RODADAS_EXP1
) -> Dict[str, float]:
    r"""Simula N rodadas para um rolo circular customizado de tamanho M e calcula as métricas observadas."""
    gerador = random.Random(semente)  # inicializa o gerador na semente 2026
    m = len(simbolosRolo)             # comprimento da nova fita circular do rolo
    lucros: List[float] = []
    premios: List[float] = []
    n_premiadas = 0

    for _ in range(nRodadas):
        # Para cada um dos 3 rolos independentes, sorteia parada K in {0, ..., m-1}
        # e observa o símbolo central R_{(K+1) mod m}
        linha_central = (
            simbolosRolo[(gerador.randint(0, m - 1) + 1) % m],
            simbolosRolo[(gerador.randint(0, m - 1) + 1) % m],
            simbolosRolo[(gerador.randint(0, m - 1) + 1) % m],
        )
        p = f_calcularPremioBruto(linha_central, tabelaPagamentos)  # apura o prêmio bruto conforme a tabela
        x = f_calcularLucroLiquido(p, CUSTO_APOSTA)                 # subtrai 1 crédito da aposta
        if p > 0.0:
            n_premiadas += 1                                        # contabiliza rodada premiada
        premios.append(p)
        lucros.append(x)

    media_p = f_calcularMediaAmostral(premios)                      # prêmio bruto médio observado
    media_x = f_calcularMediaAmostral(lucros)                       # lucro líquido médio observado
    return {
        "freq_premio_pct": (n_premiadas / nRodadas) * 100.0,
        "premio_medio_obs": media_p,
        "lucro_medio_obs": media_x,
        "rtp_observado_pct": (media_p / CUSTO_APOSTA) * 100.0,
    }


def f_executarExtra4AnaliseSensibilidade() -> Dict[str, Any]:
    r"""Executa a Análise de Sensibilidade em 7 cenários distintos (Extra 4).

    Cenários 1 a 5 (Variação de Pagamentos sobre a mesma sequência de 10.000 rodadas da semente 2026):
    - C1: Prêmios -20% (fator 0,80) -> RTP = 67,20%, E[X] = -0,3280
    - C2: Tabela Base (fator 1,00)  -> RTP = 84,00%, E[X] = -0,1600
    - C3: Prêmios +10% (fator 1,10) -> RTP = 92,40%, E[X] = -0,0760
    - C4: Ponto de Equilíbrio / Jogo Justo (fator 125/105 ≈ 1,1905) -> RTP = 100,00%, E[X] = 0,0000
    - C5: Jogo Favorável ao Jogador (+25%, fator 1,25) -> RTP = 105,00%, E[X] = +0,0500

    Cenários 6 e 7 (Variação de Probabilidades / Estrutura dos Rolos mantendo os pagamentos Base):
    - C6: Inclusão de 6º símbolo sem prêmio ['A','B','C','D','E','F'] (espaço amostral 6^3 = 216):
          Prob. de prêmio cai de 4,00% para 5/216 = 2,31%; RTP cai de 84,00% para 105/216 = 48,61%.
    - C7: Duplicação do símbolo de menor prêmio ['A','A','B','C','D','E'] (6 posições por rolo):
          Prob(A-A-A) sobe para 8/216 e demais 1/216 (Prob. total = 12/216 = 5,56%), mas o RTP cai para
          (8*5 + 10 + 15 + 25 + 50)/216 = 140/216 = 64,81% (paga com mais frequência, porém perde-se mais!).
    """
    # Sorteia a sequência canônica de 10.000 giros (semente 2026) para parear os Cenários 1 a 5
    gerador_base = random.Random(SEMENTE_EXP1)
    linhas_10k_base = [f_extrairLinhaCentral(f_sortearTabuleiro3x3(gerador_base)) for _ in range(RODADAS_EXP1)]

    fatores_pagamento = [
        ("C1: Prêmios -20%", "C1 (-20%)", "Pagamentos x 0,80", 0.80),
        ("C2: Modelo Base (0%)", "C2 (Base)", "Pagamentos x 1,00", 1.00),
        ("C3: Prêmios +10% (E5)", "C3 (+10%)", "Pagamentos x 1,10", 1.10),
        ("C4: Equilíbrio (+19,05%)", "C4 (Justo)", "Pagamentos x 125/105", 125.0 / 105.0),  # onde a casa finalmente não leva vantagem
        ("C5: Favorável (+25%)", "C5 (+25%)", "Pagamentos x 1,25", 1.25),                   # sonho do apostador (e falência do cassino)
    ]

    cenarios_resultados: List[Dict[str, Any]] = []

    for nome, rotulo_curto, param_desc, fator in fatores_pagamento:
        tabela_fator = {k: v * fator for k, v in TABELA_BASE.items()}  # escala todos os prêmios pelo multiplicador
        soma_p = sum(tabela_fator.values())                            # soma das 5 triplas escaladas
        esp_p = soma_p / 125.0                                         # E[P] pela linearidade da esperança
        esp_x = esp_p - CUSTO_APOSTA                                   # E[X] = E[P] - 1
        rtp_teo = (esp_p / CUSTO_APOSTA) * 100.0                       # RTP teórico em %
        prob_teo_pct = (5.0 / 125.0) * 100.0                           # probabilidade de prêmio continua fixa em 4,00%

        premios_obs = [f_calcularPremioBruto(lc, tabela_fator) for lc in linhas_10k_base]
        lucros_obs = [f_calcularLucroLiquido(p, CUSTO_APOSTA) for p in premios_obs]
        n_win = sum(1 for p in premios_obs if p > 0.0)                 # número de giros premiados (412 na semente 2026)

        media_p_obs = f_calcularMediaAmostral(premios_obs)
        media_x_obs = f_calcularMediaAmostral(lucros_obs)
        rtp_obs = (media_p_obs / CUSTO_APOSTA) * 100.0

        cenarios_resultados.append({
            "cenario": nome,
            "rotulo_curto": rotulo_curto,
            "tipo_variacao": param_desc,
            "prob_premio_teo_pct": prob_teo_pct,
            "freq_premio_obs_pct": (n_win / RODADAS_EXP1) * 100.0,
            "esp_premio_teo": esp_p,
            "premio_medio_obs": media_p_obs,
            "esp_lucro_teo": esp_x,
            "lucro_medio_obs": media_x_obs,
            "rtp_teorico_pct": rtp_teo,
            "rtp_observado_pct": rtp_obs,
        })

    # Cenário 6: Rolo expandido com 6 símbolos distintos ['A', 'B', 'C', 'D', 'E', 'F']
    # Adicionar um único símbolo inútil ('F') dilui o espaço amostral de 125 para 216 combinações!
    obs_c6 = f_simularRoloCustomizado(["A", "B", "C", "D", "E", "F"], TABELA_BASE, SEMENTE_EXP1, RODADAS_EXP1)
    esp_p_c6 = 105.0 / 216.0  # os mesmos 105 créditos divididos por 216 triplas equiprováveis
    cenarios_resultados.append({
        "cenario": "C6: 6 Símbolos (A..F)",
        "rotulo_curto": "C6 (6 Símb.)",
        "tipo_variacao": "Prob. 5/216 (Rolo 6 pos.)",
        "prob_premio_teo_pct": (5.0 / 216.0) * 100.0,
        "freq_premio_obs_pct": obs_c6["freq_premio_pct"],
        "esp_premio_teo": esp_p_c6,
        "premio_medio_obs": obs_c6["premio_medio_obs"],
        "esp_lucro_teo": esp_p_c6 - CUSTO_APOSTA,
        "lucro_medio_obs": obs_c6["lucro_medio_obs"],
        "rtp_teorico_pct": esp_p_c6 * 100.0,
        "rtp_observado_pct": obs_c6["rtp_observado_pct"],
    })

    # Cenário 7: Rolo com símbolo 'A' duplicado ['A', 'A', 'B', 'C', 'D', 'E'] (6 posições)
    # P(A-A-A) sobe para (2/6)^3 = 8/216; demais triplas caem para 1/216 -> P(prêmio) sobe para 12/216 = 5,56%!
    # Porém, como os prêmios altos ficaram mais raros, E[P] cai para (8*5 + 10 + 15 + 25 + 50)/216 = 140/216 = 64,81%.
    obs_c7 = f_simularRoloCustomizado(["A", "A", "B", "C", "D", "E"], TABELA_BASE, SEMENTE_EXP1, RODADAS_EXP1)
    esp_p_c7 = 140.0 / 216.0
    cenarios_resultados.append({
        "cenario": "C7: Rolo [A,A,B,C,D,E]",
        "rotulo_curto": "C7 (Duplo A)",
        "tipo_variacao": "Prob. 12/216 (+Freq, -RTP)",
        "prob_premio_teo_pct": (12.0 / 216.0) * 100.0,
        "freq_premio_obs_pct": obs_c7["freq_premio_pct"],
        "esp_premio_teo": esp_p_c7,
        "premio_medio_obs": obs_c7["premio_medio_obs"],
        "esp_lucro_teo": esp_p_c7 - CUSTO_APOSTA,
        "lucro_medio_obs": obs_c7["lucro_medio_obs"],
        "rtp_teorico_pct": esp_p_c7 * 100.0,
        "rtp_observado_pct": obs_c7["rtp_observado_pct"],
    })

    cabecalhos = [
        "Cenário",
        "Alteração Aplicada",
        "Prob. Teo.",
        "Freq. Obs.",
        "E[P] Teo.",
        "E[X] Teo.",
        "X̄ Obs.",
        "RTP Teo.",
        "RTP Obs.",
    ]
    linhas_tabela: List[List[Any]] = []
    for c in cenarios_resultados:
        linhas_tabela.append([
            c["cenario"],
            c["tipo_variacao"],
            f"{c['prob_premio_teo_pct']:.2f}%",
            f"{c['freq_premio_obs_pct']:.2f}%",
            f"{c['esp_premio_teo']:.4f}",
            f"{c['esp_lucro_teo']:+.4f}",
            f"{c['lucro_medio_obs']:+.4f}",
            f"{c['rtp_teorico_pct']:.2f}%",
            f"{c['rtp_observado_pct']:.2f}%",
        ])

    caminho_csv = DIRETORIO_TABELAS_EXTRAS / "extra4_analise_sensibilidade.csv"
    f_exportarParaCsv(caminho_csv, cabecalhos, linhas_tabela)  # salva o CSV dos 7 cenários

    caminho_figura = DIRETORIO_FIGURAS_EXTRAS / "extra4_analise_sensibilidade.png"
    f_plotarAnaliseSensibilidadeExtra4(cenarios_resultados, caminho_figura)  # gera o gráfico de barras comparativo

    return {
        "cenarios": cenarios_resultados,
        "cabecalhos": cabecalhos,
        "linhas_tabela": linhas_tabela,
        "caminho_csv": caminho_csv,
        "caminho_figura": caminho_figura,
    }
