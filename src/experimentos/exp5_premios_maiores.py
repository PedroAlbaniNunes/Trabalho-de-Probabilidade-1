r"""Experimento 5: Prêmios maiores tornam o jogo favorável?

Conceitos em ação (Seção 7 e 8 do edital):
- Esperança de uma função da variável aleatória: E[1.10 * P] = 1.10 * E[P].
- RTP sob alteração linear de premiações (+10%): RTP sobe de 84% para 92,4%.
- Comparação pareada sob a mesma realização amostral (mesmas 10.000 rodadas de E1).
- Tríplice distinção: pagar mais, pagar com maior frequência e produzir lucro esperado positivo.

Procedimento estipulado pelo edital:
- Aplicar a Tabela Base e a Tabela Prêmios +10% exatamente aos MESMOS 10.000 resultados do Experimento 1.
- Manter símbolos, probabilidades e aposta de 1 crédito inalterados.
- Gerar tabela comparativa contendo:
    - Probabilidade teórica de prêmio vs Frequência observada
    - Prêmio médio (teórico e observado)
    - Lucro médio (teórico e observado)
    - RTP (teórico e observado)
- Valores de referência teóricos com bônus de 10%:
    RTP_{+10%} = 1.10 * 0.84 = 92.4%
    E[X_{+10%}] = 0.924 - 1 = -0.076
- Exportar a tabela comparativa para CSV em 'resultados/tabelas/exp5_comparacao_tabelas.csv'.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path

from src.configuracao import (
    CUSTO_APOSTA,
    DIRETORIO_TABELAS,
)
from src.maquina.pagamentos import (
    f_calcularPremioBruto,
    f_calcularLucroLiquido,
    f_calcularEsperancaTeorica,
    TABELA_BASE,
    TABELA_BONUS_10,
)
from src.analise.metricas import (
    f_calcularMediaAmostral,
    f_calcularRtpObservado,
)
from src.analise.exportador import (
    f_exportarParaCsv,
    f_gerarTabelaFormatada,
)


def f_executarExperimento5(dadosExp1: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    r"""Executa o Experimento 5 recalculando as métricas com a tabela +10% sobre as rodadas de E1.

    Aplica a propriedade de linearidade da esperança matemática sob transformação linear:
    \[
    E[1.10 \cdot P] = 1.10 \cdot E[P]
    \]
    mantendo rigorosamente os mesmos sorteios e a aposta de 1 crédito para isolar
    o efeito exclusivo do aumento nos valores das premiações.

    Args:
        dadosExp1 (Optional[Dict[str, Any]]): Dicionário retornado pela execução do
            Experimento 1. Se omitido, o E1 é rodado automaticamente com a semente 2026.

    Returns:
        Dict[str, Any]: Estrutura com métricas teóricas e empíricas pareadas
            (probabilidade de prêmio, prêmio médio, lucro médio, RTP e caminho do CSV).
    """
    # 1. Obter a realização amostral das 10.000 rodadas de E1 (semente 2026)
    if dadosExp1 is None or "historico_linhas_centrais" not in dadosExp1:
        from src.experimentos.exp1_frequencias import f_executarExperimento1
        dadosExp1 = f_executarExperimento1(semente=2026, totalRodadas=10_000)  # se não passaram o histórico, roda o E1 na tora pra parear

    historico_linhas = dadosExp1["historico_linhas_centrais"]  # pega a fita gravada dos 10k giros pra fazer o tira-teima lado a lado
    n_total = len(historico_linhas)  # total de giros analisados (10.000 redondinho)

    # 2. Recálculo das premiações e lucros para ambas as tabelas sobre a MESMA sequência
    premios_base: List[float] = []
    lucros_base: List[float] = []

    premios_bonus: List[float] = []
    lucros_bonus: List[float] = []

    for linha in historico_linhas:
        # Tabela Base (o padrão do cassino)
        p_base = f_calcularPremioBruto(linha, TABELA_BASE)  # calcula o prêmio bruto na tabela clássica
        x_base = f_calcularLucroLiquido(p_base, CUSTO_APOSTA)  # desconta o 1 real da aposta pra ver se sobrou troco ou preju
        premios_base.append(p_base)  # guarda na sacola de prêmios base
        lucros_base.append(x_base)  # guarda na sacola de lucros base

        # Tabela Prêmios +10% (aquela ilusão de ótica que parece que vai dar bom)
        p_bonus = f_calcularPremioBruto(linha, TABELA_BONUS_10)  # calcula o prêmio com o bônus generoso de +10%
        x_bonus = f_calcularLucroLiquido(p_bonus, CUSTO_APOSTA)  # desconta o mesmo 1 real da entrada pra ver o saldo real
        premios_bonus.append(p_bonus)  # guarda na sacola de prêmios com bônus
        lucros_bonus.append(x_bonus)  # guarda na sacola de lucros com bônus

    # 3. Estatísticas Teóricas de Referência (a matemática pura que a banca usa pra não quebrar)
    teo_base = f_calcularEsperancaTeorica(TABELA_BASE, CUSTO_APOSTA)  # calcula as expectativas teóricas da tabela base
    teo_bonus = f_calcularEsperancaTeorica(TABELA_BONUS_10, CUSTO_APOSTA)  # calcula as expectativas teóricas com +10% de prêmio

    prob_premio_teo = teo_base["prob_vitoria_pct"]  # cravado em 4%: 5 triplas num mar de 125 combinações possíveis
    premio_medio_teo_base = teo_base["esperanca_premio"]  # retorno bruto esperado por giro: 84 centavos na base
    premio_medio_teo_bonus = teo_bonus["esperanca_premio"]  # retorno bruto esperado com bônus: sobe exatos 10% (92,4 centavos)
    lucro_medio_teo_base = teo_base["esperanca_lucro"]  # sangria esperada por giro: jogador perde 16 centavos a cada rodada
    lucro_medio_teo_bonus = teo_bonus["esperanca_lucro"]  # sangria com bônus: cai pra 7,6 centavos, mas CONTINUA NO VERMELHO!
    rtp_teo_base = teo_base["rtp_teorico_pct"]  # a máquina devolve em média 84% de tudo que entra
    rtp_teo_bonus = teo_bonus["rtp_teorico_pct"]  # com bônus devolve 92,4%, mas os outros 7,6% ainda ficam com a casa

    # 4. Estatísticas Amostrais Observadas (o que rolou de fato na prática)
    total_premiadas = sum(1 for p in premios_base if p > 0.0)  # conta quantas vezes caiu tripla e o sino tocou
    freq_premio_obs = (total_premiadas / n_total) * 100.0  # frequência percentual real de vitórias observada

    premio_medio_obs_base = f_calcularMediaAmostral(premios_base)  # média real do prêmio que pingou na conta com a tabela base
    premio_medio_obs_bonus = f_calcularMediaAmostral(premios_bonus)  # média real do prêmio turbinado: reflete os 10% a mais na prática

    lucro_medio_obs_base = f_calcularMediaAmostral(lucros_base)  # prejuízo médio observado por giro na tabela base
    lucro_medio_obs_bonus = f_calcularMediaAmostral(lucros_bonus)  # prejuízo médio observado na turbinada: dói menos, mas ainda dói

    rtp_obs_base = f_calcularRtpObservado(sum(premios_base), n_total * CUSTO_APOSTA)  # RTP real observado na tabela base
    rtp_obs_bonus = f_calcularRtpObservado(sum(premios_bonus), n_total * CUSTO_APOSTA)  # RTP real observado na tabela com bônus

    vantagem_casa_teo_base = 100.0 - rtp_teo_base  # a gordurinha matemática da casa na regra clássica (16%)
    vantagem_casa_teo_bonus = 100.0 - rtp_teo_bonus  # o pedágio do cassino com bônus: cai pra 7,6%, mas a casa NUNCA perde

    vantagem_casa_obs_base = 100.0 - rtp_obs_base  # quanto a banca faturou na prática no cenário base
    vantagem_casa_obs_bonus = 100.0 - rtp_obs_bonus  # quanto a banca faturou na prática mesmo dando 10% a mais de colher de chá

    # 5. Construção da Tabela Comparativa Estruturada
    cabecalhos = [
        "Métrica Analisada",
        "Tabela Base (Teórico)",
        "Tabela Base (Observado)",
        "Tabela +10% (Teórico)",
        "Tabela +10% (Observado)",
        "Variação Teórica",
        "Variação Observada",
    ]

    linhas_tabela: List[List[Any]] = [
        [
            "Probabilidade de Prêmio",
            f"{prob_premio_teo:.2f}%",
            f"{freq_premio_obs:.2f}%",
            f"{prob_premio_teo:.2f}%",
            f"{freq_premio_obs:.2f}%",
            "0.00% (Inalterada)",
            "0.00% (Inalterada)",
        ],
        [
            "Prêmio Médio (P)",
            f"{premio_medio_teo_base:.4f}",
            f"{premio_medio_obs_base:.4f}",
            f"{premio_medio_teo_bonus:.4f}",
            f"{premio_medio_obs_bonus:.4f}",
            f"{((premio_medio_teo_bonus - premio_medio_teo_base) / premio_medio_teo_base * 100):+.2f}%",
            f"{((premio_medio_obs_bonus - premio_medio_obs_base) / premio_medio_obs_base * 100):+.2f}%",
        ],
        [
            "Lucro Médio (X)",
            f"{lucro_medio_teo_base:+.4f}",
            f"{lucro_medio_obs_base:+.4f}",
            f"{lucro_medio_teo_bonus:+.4f}",
            f"{lucro_medio_obs_bonus:+.4f}",
            f"{((lucro_medio_teo_bonus - lucro_medio_teo_base) / abs(lucro_medio_teo_base) * 100):+.2f}%",
            f"{((lucro_medio_obs_bonus - lucro_medio_obs_base) / abs(lucro_medio_obs_base) * 100):+.2f}%",
        ],
        [
            "RTP (%)",
            f"{rtp_teo_base:.2f}%",
            f"{rtp_obs_base:.2f}%",
            f"{rtp_teo_bonus:.2f}%",
            f"{rtp_obs_bonus:.2f}%",
            f"{((rtp_teo_bonus - rtp_teo_base) / rtp_teo_base * 100):+.2f}%",
            f"{((rtp_obs_bonus - rtp_obs_base) / rtp_obs_base * 100):+.2f}%",
        ],
        [
            "Vantagem da Casa (%)",
            f"{vantagem_casa_teo_base:.2f}%",
            f"{vantagem_casa_obs_base:.2f}%",
            f"{vantagem_casa_teo_bonus:.2f}%",
            f"{vantagem_casa_obs_bonus:.2f}%",
            f"{((vantagem_casa_teo_bonus - vantagem_casa_teo_base) / vantagem_casa_teo_base * 100):+.2f}%",
            f"{((vantagem_casa_obs_bonus - vantagem_casa_obs_base) / vantagem_casa_obs_base * 100):+.2f}%",
        ],
    ]

    # 6. Exportação para arquivo CSV
    caminho_csv = DIRETORIO_TABELAS / "exp5_comparacao_tabelas.csv"
    f_exportarParaCsv(caminho_csv, cabecalhos, linhas_tabela)

    return {
        "n_rodadas": n_total,
        "prob_premio_teo": prob_premio_teo,
        "freq_premio_obs": freq_premio_obs,
        "premio_medio_teo_base": premio_medio_teo_base,
        "premio_medio_obs_base": premio_medio_obs_base,
        "premio_medio_teo_bonus": premio_medio_teo_bonus,
        "premio_medio_obs_bonus": premio_medio_obs_bonus,
        "lucro_medio_teo_base": lucro_medio_teo_base,
        "lucro_medio_obs_base": lucro_medio_obs_base,
        "lucro_medio_teo_bonus": lucro_medio_teo_bonus,
        "lucro_medio_obs_bonus": lucro_medio_obs_bonus,
        "rtp_teo_base": rtp_teo_base,
        "rtp_obs_base": rtp_obs_base,
        "rtp_teo_bonus": rtp_teo_bonus,
        "rtp_obs_bonus": rtp_obs_bonus,
        "vantagem_casa_teo_base": vantagem_casa_teo_base,
        "vantagem_casa_obs_base": vantagem_casa_obs_base,
        "vantagem_casa_teo_bonus": vantagem_casa_teo_bonus,
        "vantagem_casa_obs_bonus": vantagem_casa_obs_bonus,
        "cabecalhos": cabecalhos,
        "linhas_tabela": linhas_tabela,
        "caminho_csv": caminho_csv,
    }
