r"""Experimento 1: As frequências acompanham as probabilidades?

Conceitos em ação (Seção 7 do edital):
- Espaço amostral: 125 resultados centrais equiprováveis.
- Variável aleatória discreta: Lucro líquido X e Prêmio bruto P.
- Frequência relativa vs Probabilidade teórica correspondente.
- Média amostral (\bar{X}), desvio-padrão amostral (s com divisor N - 1) e RTP observado.
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
    TABELA_BASE,
)
from src.analise.metricas import (
    f_calcularMediaAmostral,
    f_calcularDesvioPadraoAmostral,
    f_calcularRtpObservado,
)
from src.analise.exportador import (
    f_exportarParaCsv,
)
from src.analise.graficos import (
    f_plotarComparacaoFrequenciasExp1,
)


def f_executarExperimento1(semente: int = SEMENTE_EXP1, totalRodadas: int = RODADAS_EXP1) -> Dict[str, Any]:
    r"""Executa a simulação completa do Experimento 1 conforme as especificações da Seção 7.

    Manda a máquina girar 10.000 vezes com semente 2026 cravada, computa cada giro,
    compara a teoria com a prática e gera a tabela CSV e o gráfico de barras.

    Args:
        semente (int): Semente para o gerador pseudoaleatório (padrão do edital: 2026).
        totalRodadas (int): Quantidade total de rodadas na simulação (padrão: 10.000).

    Returns:
        Dict[str, Any]: Dicionário contendo os resumos estatísticos e os históricos de rodadas.
    """
    # 1. Inicialização do gerador pseudoaleatório uma única vez (sem resetar durante os giros!)
    gerador = random.Random(semente)  # Trava a semente no início pra ninguém chiar de manipulação

    # Definição das categorias canônicas da Tabela 1 do edital
    categorias = ["A-A-A", "B-B-B", "C-C-C", "D-D-D", "E-E-E", "Qualquer outra tripla"]
    contagens = {cat: 0 for cat in categorias}  # Placar zerado no início do jogo

    lista_lucros_X: List[float] = []  # O extrato financeiro da brincadeira
    lista_premios_P: List[float] = []  # Quanto a máquina cuspiu de prêmio bruto
    lista_linhas_centrais: List[tuple] = []  # O que caiu no meio em cada rodada

    # 2. Execução das 10.000 rodadas na marra
    for _ in range(totalRodadas):  # Bota o motor pra roncar 10 mil vezes
        tabuleiro = f_sortearTabuleiro3x3(gerador)  # Gira os rolos e para na sorte
        linha_central = f_extrairLinhaCentral(tabuleiro)  # Pega o que interessa: a linha do meio

        premio_P = f_calcularPremioBruto(linha_central, TABELA_BASE)  # Passa na régua: tem prêmio ou zero?
        lucro_X = f_calcularLucroLiquido(premio_P, CUSTO_APOSTA)  # Desconta 1 crédito da aposta: lucro real

        if f_ehTriplaPremiada(linha_central):  # Opa! Bateu trinca idêntica, alegria de apostador!
            chave = f"{linha_central[0]}-{linha_central[1]}-{linha_central[2]}"  # Monta a chave (tipo 'B-B-B')
            if chave in contagens:
                contagens[chave] += 1  # Pontua no placar da trinca correspondente
            else:
                contagens["Qualquer outra tripla"] += 1  # Salvaguarda se vier algo estranho
        else:
            contagens["Qualquer outra tripla"] += 1  # Deu zebra, vai pra vala dos 96% que só perde dindin

        lista_premios_P.append(premio_P)  # Anota o prêmio da rodada
        lista_lucros_X.append(lucro_X)  # Anota o lucro da rodada (quase sempre -1.0)
        lista_linhas_centrais.append(linha_central)  # Guarda a combinação pra reutilizar nos outros experimentos

    # 3. Conferência estrita: a soma das contagens deve somar exatamente 10.000
    soma_contagens = sum(contagens.values())  # Conta se todas as fichas estão no balde
    assert soma_contagens == totalRodadas, f"Erro: contagens somam {soma_contagens}, esperado {totalRodadas}"  # Check de ferro!

    # 4. Cálculo das estatísticas descritivas amostrais
    media_lucro_X = f_calcularMediaAmostral(lista_lucros_X)  # Média de lucro (-0.1315): a casa sempre vence!
    desvio_padrao_s = f_calcularDesvioPadraoAmostral(lista_lucros_X)  # Dispersão alta (~5.27): prêmios raros esticam a variância
    rtp_observado = f_calcularRtpObservado(sum(lista_premios_P), totalRodadas * CUSTO_APOSTA)  # O retorno observado (~86.85%)

    total_premiadas = totalRodadas - contagens["Qualquer outra tripla"]  # Quantas rodadas não foram derrota
    proporcao_premiadas_pct = (total_premiadas / totalRodadas) * 100.0  # Frequência real de vitória (~4.12%)

    # Probabilidades teóricas canônicas do edital
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
        cont = contagens[cat]  # Quantas vezes essa categoria caiu
        freq_rel_pct = (cont / totalRodadas) * 100.0  # Transforma contagem em porcentagem do total
        prob_frac, prob_pct = prob_teorica_dict[cat]  # Pega a probabilidade que a matemática prometeu
        lucro_val = lucro_esperado_por_cat[cat]  # Lucro líquido daquela categoria

        linhas_tabela.append([
            cat,
            f"{lucro_val:+.0f}",
            f"{prob_frac:.4f}",
            f"{prob_pct:.2f}%",
            cont,
            f"{freq_rel_pct:.2f}%",
        ])

        freq_obs_pct_lista.append(freq_rel_pct)  # Guarda pro gráfico
        freq_teo_pct_lista.append(prob_pct)  # Guarda pro gráfico

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
    caminho_csv = DIRETORIO_TABELAS / "exp1_frequencias.csv"  # Destino oficial da tabela
    f_exportarParaCsv(caminho_csv, cabecalhos, linhas_tabela)  # Grava no disco com UTF-8

    # 7. Geração do gráfico de barras
    caminho_figura = DIRETORIO_FIGURAS / "exp1_frequencias.png"  # Destino da figura
    nomes_curtos_categorias = ["A-A-A", "B-B-B", "C-C-C", "D-D-D", "E-E-E", "Outras"]
    f_plotarComparacaoFrequenciasExp1(
        nomes_curtos_categorias,
        freq_teo_pct_lista,
        freq_obs_pct_lista,
        caminho_figura,
    )  # Desenha as barras emparelhadas e salva em DPI 300

    # Retorno estruturado pra alimentar o main e os experimentos irmãos (E2, E4, E5)
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
        "historico_lucros_X": lista_lucros_X,  # Guardado a sete chaves pro Exp 2
        "historico_premios_P": lista_premios_P,  # Guardado pro Exp 4
        "historico_linhas_centrais": lista_linhas_centrais,  # Guardado pro Exp 5
    }
