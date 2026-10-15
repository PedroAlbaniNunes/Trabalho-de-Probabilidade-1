r"""Experimento 2: O que muda quando aumentamos a amostra?

Conceitos em ação (Seção 7 e 8 do edital):
- Simulação de Monte Carlo e convergência assintótica.
- Média acumulada ao longo das rodadas: \bar{X}_k = \frac{1}{k} \sum_{i=1}^k X_i.
- Lei dos Grandes Números (LLN): convergência em probabilidade para E[X] = -0,16 créditos.
- A LLN não garante convergência monótona nem teto de erro estrito em 10.000 rodadas.
- Reprodutibilidade estrita e verificação de sementes pseudoaleatórias.

Procedimento estipulado pelo edital:
- Executar três sequências de 10.000 rodadas com as sementes: 10, 2026 e 123456.
- Reutilizar a sequência da semente 2026 obtida no Experimento 1 (sem novo sorteio).
- Para cada execução, registrar a média acumulada após 100, 1.000 e 10.000 rodadas.
- Entregar uma tabela 3x3 com essas médias acumuladas e exportar para CSV.
- Entregar um gráfico com as três trajetórias completas e a linha de referência horizontal em E[X] = -0,16.
- Repetir a semente 2026 no mesmo ambiente e conferir se os 10 primeiros resultados coincidem elemento a elemento.
"""

from typing import Dict, Any, List, Optional, Tuple
import random
from pathlib import Path

from src.configuracao import (
    SEMENTES_EXP2,
    RODADAS_EXP2,
    CUSTO_APOSTA,
    DIRETORIO_TABELAS,
    DIRETORIO_FIGURAS,
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
    f_calcularMediasAcumuladas,
)
from src.analise.exportador import (
    f_exportarParaCsv,
    f_gerarTabelaFormatada,
)
from src.analise.graficos import (
    f_plotarConvergenciaMediasExp2,
)


def f_verificarReprodutibilidadePrimeirosResultados(semente: int = 2026, nResultados: int = 10) -> bool:
    """Verifica se os n primeiros resultados sorteados com a semente especificada são rigorosamente idênticos.

    Conforme a Seção 7 do edital:
    "Repetir a semente 2026, no mesmo ambiente, e conferir os dez primeiros resultados. Informar se foram reproduzidos."

    Argumentos:
        semente (int): Semente pseudoaleatória utilizada (padrão do edital: 2026).
        nResultados (int): Quantidade de resultados iniciais a auditar (padrão: 10).

    Retorna:
        bool: True se a sequência de resultados foi rigorosamente reproduzida, False caso haja divergência.
    """
    g1 = random.Random(semente)
    g2 = random.Random(semente)

    seq1 = [f_extrairLinhaCentral(f_sortearTabuleiro3x3(g1)) for _ in range(nResultados)]
    seq2 = [f_extrairLinhaCentral(f_sortearTabuleiro3x3(g2)) for _ in range(nResultados)]

    return seq1 == seq2


def f_executarExperimento2(dadosExp1: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    r"""Executa a simulação completa do Experimento 2 para análise da Lei dos Grandes Números.

    Argumentos:
        dadosExp1 (Optional[Dict[str, Any]]): Dados prévios da execução do Experimento 1 (para reaproveitamento).

    Retorna:
        Dict[str, Any]: Dicionário contendo tabela 3x3, trajetórias completas e status de reprodução.
    """
    # 1. Obtenção dos dados da semente 2026 (reutilização obrigatória do Experimento 1)
    if dadosExp1 is None or "historico_lucros_X" not in dadosExp1:
        from src.experimentos.exp1_frequencias import f_executarExperimento1
        dadosExp1 = f_executarExperimento1(semente=2026, totalRodadas=RODADAS_EXP2)

    lucros_por_semente: Dict[int, List[float]] = {}
    lucros_por_semente[2026] = list(dadosExp1["historico_lucros_X"])

    # 2. Simulação das outras duas sementes fixadas no edital (10 e 123456)
    outras_sementes = [s for s in SEMENTES_EXP2 if s != 2026]

    for semente in outras_sementes:
        gerador = random.Random(semente)
        lucros_s: List[float] = []

        for _ in range(RODADAS_EXP2):
            tabuleiro = f_sortearTabuleiro3x3(gerador)
            linha_central = f_extrairLinhaCentral(tabuleiro)
            premio_P = f_calcularPremioBruto(linha_central, TABELA_BASE)
            lucro_X = f_calcularLucroLiquido(premio_P, CUSTO_APOSTA)
            lucros_s.append(lucro_X)

        lucros_por_semente[semente] = lucros_s

    # 3. Cálculo das trajetórias completas de médias acumuladas
    # Garantir a ordem canônica: 10, 2026, 123456
    ordem_sementes = [10, 2026, 123456]
    trajetorias_medias: Dict[int, List[float]] = {}
    medias_marcos: Dict[int, Dict[int, float]] = {}

    for semente in ordem_sementes:
        medias_acum = f_calcularMediasAcumuladas(lucros_por_semente[semente])
        trajetorias_medias[semente] = medias_acum

        # Extração das médias nos pontos de controle: N = 100, 1.000 e 10.000 rodadas
        medias_marcos[semente] = {
            100: medias_acum[99],
            1000: medias_acum[999],
            10000: medias_acum[9999],
        }

    # 4. Construção da Tabela 3x3 de Médias Acumuladas
    cabecalhos = ["Semente", "N = 100 rodadas", "N = 1.000 rodadas", "N = 10.000 rodadas"]
    linhas_tabela: List[List[Any]] = []

    for semente in ordem_sementes:
        rotulo = f"Semente {semente} (E1)" if semente == 2026 else f"Semente {semente}"
        m100 = medias_marcos[semente][100]
        m1000 = medias_marcos[semente][1000]
        m10000 = medias_marcos[semente][10000]

        linhas_tabela.append([
            rotulo,
            f"{m100:+.4f}",
            f"{m1000:+.4f}",
            f"{m10000:+.4f}",
        ])

    # Linha de referência teórica
    linhas_tabela.append([
        "Referência Teórica (E[X])",
        "-0.1600",
        "-0.1600",
        "-0.1600",
    ])

    # 5. Exportação da Tabela CSV
    caminho_csv = DIRETORIO_TABELAS / "exp2_medias_acumuladas.csv"
    f_exportarParaCsv(caminho_csv, cabecalhos, linhas_tabela)

    # 6. Geração do Gráfico de Convergência de Trajetórias
    caminho_figura = DIRETORIO_FIGURAS / "exp2_convergencia.png"
    esperanca_teorica = -0.16
    f_plotarConvergenciaMediasExp2(
        trajetorias_medias,
        esperanca_teorica,
        caminho_figura,
    )

    # 7. Auditoria dos 10 primeiros resultados da semente 2026
    g_audit = random.Random(2026)
    dez_primeiros_audit = [f_extrairLinhaCentral(f_sortearTabuleiro3x3(g_audit)) for _ in range(10)]
    dez_primeiros_e1 = dadosExp1["historico_linhas_centrais"][:10]
    reproduzido_exato = (dez_primeiros_audit == dez_primeiros_e1) and f_verificarReprodutibilidadePrimeirosResultados(2026, 10)

    # 8. Retorno estruturado
    return {
        "ordem_sementes": ordem_sementes,
        "tabela_3x3_linhas": linhas_tabela,
        "cabecalhos_3x3": cabecalhos,
        "medias_marcos": medias_marcos,
        "trajetorias": trajetorias_medias,
        "reproduzido_com_sucesso": reproduzido_exato,
        "dez_primeiros_resultados_2026": dez_primeiros_audit,
        "caminho_csv": caminho_csv,
        "caminho_figura": caminho_figura,
    }
