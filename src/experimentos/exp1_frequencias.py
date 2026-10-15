r"""Experimento 1: As frequências acompanham as probabilidades?

Conceitos em ação (Seção 7 do edital):
- Espaço amostral: 125 resultados centrais equiprováveis.
- Variável aleatória discreta: Lucro líquido X e Prêmio bruto P.
- Frequência relativa vs Probabilidade teórica correspondente.
- Média amostral (\bar{X}), desvio-padrão amostral (s com divisor N - 1) e RTP observado.

Procedimento estipulado:
- Executar 10.000 rodadas, semente 2026, sem saldo ou regra de parada.
- Contar os seis resultados da Tabela 1:
    - A-A-A: P = 5,  X = +4, Prob = 1/125 = 0,8%
    - B-B-B: P = 10, X = +9, Prob = 1/125 = 0,8%
    - C-C-C: P = 15, X = +14, Prob = 1/125 = 0,8%
    - D-D-D: P = 25, X = +24, Prob = 1/125 = 0,8%
    - E-E-E: P = 50, X = +49, Prob = 1/125 = 0,8%
    - Qualquer outra tripla: P = 0, X = -1, Prob = 120/125 = 96,0%
- Entregar uma tabela em CSV com valor do lucro, probabilidade teórica, contagem e frequência relativa.
- Gerar um gráfico de barras que compare teoria e observação.
- Calcular o lucro médio (\bar{X}), o RTP observado, a proporção de rodadas premiadas e o desvio-padrão amostral (s).
- Conferir se as contagens somam rigorosamente 10.000.
- Preservar o histórico completo das 10.000 rodadas (necessário para reutilização em E2, E4 e E5).
"""

from typing import Dict, Any, List
import random
from pathlib import Path

from src.configuracao import (
    SEMENTE_EXP1,
    RODADAS_EXP1,
    CUSTO_APOSTA,
    DIRETORIO_TABELAS,
    DIRETORIO_FIGURAS,
)
from src.maquina.rolos import (
    f_sortearTabuleiro3x3,
    f_extrairLinhaCentral,
)
from src.maquina.pagamentos import (
    f_ehTriplaPremiada,
    f_calcularPremioBruto,
    f_calcularLucroLiquido,
    f_calcularEsperancaTeorica,
    TABELA_BASE,
)
from src.analise.metricas import (
    f_calcularMediaAmostral,
    f_calcularDesvioPadraoAmostral,
    f_calcularRtpObservado,
)
from src.analise.exportador import (
    f_exportarParaCsv,
    f_gerarTabelaFormatada,
)
from src.analise.graficos import (
    f_plotarComparacaoFrequenciasExp1,
)


def f_executarExperimento1(semente: int = SEMENTE_EXP1, totalRodadas: int = RODADAS_EXP1) -> Dict[str, Any]:
    r"""Executa a simulação completa do Experimento 1 conforme as especificações da Seção 7.

    Argumentos:
        semente (int): Semente para o gerador pseudoaleatório (padrão: 2026).
        totalRodadas (int): Quantidade total de rodadas na simulação (padrão: 10.000).

    Retorna:
        Dict[str, Any]: Dicionário contendo os resultados resumidos e o histórico de rodadas.
    """
    # 1. Inicialização do gerador pseudoaleatório uma única vez
    gerador = random.Random(semente)

    # Definição das categorias canônicas da Tabela 1
    categorias = ["A-A-A", "B-B-B", "C-C-C", "D-D-D", "E-E-E", "Qualquer outra tripla"]
    contagens = {cat: 0 for cat in categorias}

    lista_lucros_X: List[float] = []
    lista_premios_P: List[float] = []
    lista_linhas_centrais: List[tuple] = []

    # 2. Execução das 10.000 rodadas
    for _ in range(totalRodadas):
        tabuleiro = f_sortearTabuleiro3x3(gerador)
        linha_central = f_extrairLinhaCentral(tabuleiro)

        premio_P = f_calcularPremioBruto(linha_central, TABELA_BASE)
        lucro_X = f_calcularLucroLiquido(premio_P, CUSTO_APOSTA)

        if f_ehTriplaPremiada(linha_central):
            chave = f"{linha_central[0]}-{linha_central[1]}-{linha_central[2]}"
            if chave in contagens:
                contagens[chave] += 1
            else:
                contagens["Qualquer outra tripla"] += 1
        else:
            contagens["Qualquer outra tripla"] += 1

        lista_premios_P.append(premio_P)
        lista_lucros_X.append(lucro_X)
        lista_linhas_centrais.append(linha_central)

    # 3. Conferência estrita: a soma das contagens deve somar exatamente 10.000
    soma_contagens = sum(contagens.values())
    assert soma_contagens == totalRodadas, f"Erro: contagens somam {soma_contagens}, esperado {totalRodadas}"

    # 4. Cálculo das estatísticas descritivas amostrais
    media_lucro_X = f_calcularMediaAmostral(lista_lucros_X)
    desvio_padrao_s = f_calcularDesvioPadraoAmostral(lista_lucros_X)
    rtp_observado = f_calcularRtpObservado(sum(lista_premios_P), totalRodadas * CUSTO_APOSTA)

    total_premiadas = totalRodadas - contagens["Qualquer outra tripla"]
    proporcao_premiadas_pct = (total_premiadas / totalRodadas) * 100.0

    # Probabilidades teóricas canônicas
    prob_teorica_dict = {
        "A-A-A": (1.0 / 125.0, 0.8),
        "B-B-B": (1.0 / 125.0, 0.8),
        "C-C-C": (1.0 / 125.0, 0.8),
        "D-D-D": (1.0 / 125.0, 0.8),
        "E-E-E": (1.0 / 125.0, 0.8),
        "Qualquer outra tripla": (120.0 / 125.0, 96.0),
    }

    lucro_esperado_por_cat = {
        "A-A-A": 4.0,
        "B-B-B": 9.0,
        "C-C-C": 14.0,
        "D-D-D": 24.0,
        "E-E-E": 49.0,
        "Qualquer outra tripla": -1.0,
    }

    # 5. Estruturação dos dados tabulares
    cabecalhos = ["Desfecho", "Lucro_X", "Prob_Teorica", "Prob_Teorica_Pct", "Contagem", "Freq_Relativa_Pct"]
    linhas_tabela: List[List[Any]] = []
    freq_obs_pct_lista: List[float] = []
    freq_teo_pct_lista: List[float] = []

    for cat in categorias:
        cont = contagens[cat]
        freq_rel_pct = (cont / totalRodadas) * 100.0
        prob_frac, prob_pct = prob_teorica_dict[cat]
        lucro_val = lucro_esperado_por_cat[cat]

        linhas_tabela.append([
            cat,
            f"{lucro_val:+.0f}",
            f"{prob_frac:.4f}",
            f"{prob_pct:.2f}%",
            cont,
            f"{freq_rel_pct:.2f}%",
        ])

        freq_obs_pct_lista.append(freq_rel_pct)
        freq_teo_pct_lista.append(prob_pct)

    # Linha totalizadora de conferência
    linhas_tabela.append([
        "TOTAL",
        "-",
        "1.0000",
        "100.00%",
        soma_contagens,
        "100.00%",
    ])

    # 6. Exportação do CSV
    caminho_csv = DIRETORIO_TABELAS / "exp1_frequencias.csv"
    f_exportarParaCsv(caminho_csv, cabecalhos, linhas_tabela)

    # 7. Geração do gráfico de barras
    caminho_figura = DIRETORIO_FIGURAS / "exp1_frequencias.png"
    nomes_curtos_categorias = ["A-A-A", "B-B-B", "C-C-C", "D-D-D", "E-E-E", "Outras"]
    f_plotarComparacaoFrequenciasExp1(
        nomes_curtos_categorias,
        freq_teo_pct_lista,
        freq_obs_pct_lista,
        caminho_figura,
    )

    # Retorno estruturado para consumo no main e nos demais experimentos
    return {
        "semente": semente,
        "total_rodadas": totalRodadas,
        "contagens": contagens,
        "lucro_medio_amostral": media_lucro_X,
        "desvio_padrao_amostral": desvio_padrao_s,
        "rtp_observado_pct": rtp_observado,
        "proporcao_premiadas_pct": proporcao_premiadas_pct,
        "tabela_linhas": linhas_tabela,
        "caminho_csv": caminho_csv,
        "caminho_figura": caminho_figura,
        "historico_lucros_X": lista_lucros_X,
        "historico_premios_P": lista_premios_P,
        "historico_linhas_centrais": lista_linhas_centrais,
    }
