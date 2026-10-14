"""Módulo de geração de gráficos com Matplotlib.

Diretrizes visuais do edital (Seção 9 e 11):
- Manter apenas rótulos de eixos, unidades, categorias e identificações estritamente necessárias dentro do gráfico.
- Deixar títulos longos, números de figura e legendas formais para serem inseridos no corpo do relatório/LaTeX.
- Gráficos devem ser exportados em alta resolução (.png) na pasta 'resultados/figuras/'.
"""

from pathlib import Path
from typing import List, Dict, Any


def f_plotarComparacaoFrequenciasExp1(
    categorias: List[str],
    frequenciasTeoricas: List[float],
    frequenciasObservadas: List[float],
    caminhoSaida: Path
) -> None:
    """Gera um gráfico de barras comparando as probabilidades teóricas com as frequências observadas no E1.

    Argumentos:
        categorias (List[str]): Nomes dos desfechos (ex: A-A-A, ..., Qualquer outra).
        frequenciasTeoricas (List[float]): Valores teóricos em porcentagem ou probabilidade.
        frequenciasObservadas (List[float]): Frequências relativas obtidas na simulação.
        caminhoSaida (Path): Caminho onde o arquivo .png será salvo.
    """
    pass


def f_plotarConvergenciaMediasExp2(
    trajetoriasPorSemente: Dict[int, List[float]],
    esperancaTeorica: float,
    caminhoSaida: Path
) -> None:
    """Plota as trajetórias de médias acumuladas de lucro para as 3 sementes (10, 2026, 123456) no E2.

    Deve conter:
    - Eixo X: Número de rodadas (escala linear ou logarítmica).
    - Eixo Y: Lucro médio acumulado (créditos).
    - Linha horizontal tracejada de referência em E[X] = -0.16.

    Argumentos:
        trajetoriasPorSemente (Dict[int, List[float]]): Mapeia semente -> lista de médias acumuladas.
        esperancaTeorica (float): Valor de referência teórico (-0.16).
        caminhoSaida (Path): Destino do arquivo .png.
    """
    pass


def f_plotarTrajetoriasSaldosExp3(
    trajetoriasCincoJogadores: List[List[float]],
    saldoInicial: float,
    caminhoSaida: Path
) -> None:
    """Plota as curvas de evolução de saldo dos 5 primeiros participantes virtuais no E3.

    Regra do edital:
    - Após a parada (por 500 rodadas ou por esgotamento B < 1), o saldo deve ser mantido constante na curva.

    Argumentos:
        trajetoriasCincoJogadores (List[List[float]]): Lista com as 5 séries de saldo.
        saldoInicial (float): Saldo de partida (ex: 100.0 créditos).
        caminhoSaida (Path): Destino da imagem .png.
    """
    pass
