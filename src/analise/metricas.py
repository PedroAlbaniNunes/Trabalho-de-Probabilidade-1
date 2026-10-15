r"""Módulo de cálculos estatísticos e funções matemáticas auxiliares.

Contém as fórmulas formais requeridas no edital:
- Média amostral: \bar{X} = \frac{1}{N} \sum_{i=1}^{N} X_i
- Desvio-padrão amostral (com divisor N - 1): s = \sqrt{\frac{1}{N - 1} \sum_{i=1}^{N} (X_i - \bar{X})^2}
- RTP observado: \widehat{RTP} = \left( \frac{\sum P_i}{\sum Aposta} \right) \times 100\%
- Mediana e proporções percentuais.
"""

from typing import List, Sequence, Dict
import math
import numpy as np


def f_calcularMediaAmostral(valores: Sequence[float]) -> float:
    r"""Calcula a média aritmética simples (\bar{X}) de uma sequência de valores observados.

    Fórmula:
        \bar{X} = (1 / N) * sum(X_i)

    Argumentos:
        valores (Sequence[float]): Coleção de valores numéricos (ex: lucros X_i).

    Retorna:
        float: Média amostral calculada.
    """
    n = len(valores)
    if n == 0:
        return 0.0
    return float(np.mean(valores))


def f_calcularDesvioPadraoAmostral(valores: Sequence[float]) -> float:
    r"""Calcula o desvio-padrão amostral (s) utilizando estritamente o divisor N - 1 (graus de liberdade).

    Conforme destacado na Seção 7 do edital:
    "Uma biblioteca pode calcular s, usando divisor N - 1. Explicar o significado da média e da
    dispersão, em créditos."

    Fórmula:
        s = sqrt( (1 / (N - 1)) * sum( (X_i - \bar{X})^2 ) )

    Argumentos:
        valores (Sequence[float]): Coleção de valores observados com N >= 2.

    Retorna:
        float: Desvio-padrão amostral s em créditos fictícios.
    """
    n = len(valores)
    if n <= 1:
        return 0.0
    return float(np.std(valores, ddof=1))


def f_calcularMediana(valores: Sequence[float]) -> float:
    """Calcula a mediana amostral de uma coleção de dados.

    Argumentos:
        valores (Sequence[float]): Coleção de valores observados.

    Retorna:
        float: Mediana calculada.
    """
    if len(valores) == 0:
        return 0.0
    return float(np.median(valores))


def f_calcularRtpObservado(totalPremios: float, totalApostado: float) -> float:
    r"""Calcula o retorno ao jogador observado (\widehat{RTP}) em termos percentuais.

    Fórmula da Seção 7 do edital:
        \widehat{RTP} = ( sum(P_i) / sum(Aposta_i) ) * 100

    Argumentos:
        totalPremios (float): Soma total de todos os prêmios brutos P pagos nas rodadas.
        totalApostado (float): Montante total de créditos apostados (ex: N * custo_aposta).

    Retorna:
        float: Percentual de retorno observado (ex: 84.15 para 84,15%).
    """
    if totalApostado <= 0:
        return 0.0
    return float((totalPremios / totalApostado) * 100.0)


def f_calcularMediasAcumuladas(valores: Sequence[float]) -> List[float]:
    """Gera o vetor de médias cumulativas ao longo do avanço das rodadas.

    Para cada rodada k (de 1 até N):
        media_acumulada[k] = (1 / k) * sum(valores[0:k])

    Argumentos:
        valores (Sequence[float]): Lista sequencial dos lucros observados rodada a rodada.

    Retorna:
        List[float]: Vetor de médias acumuladas com tamanho idêntico a `valores`.
    """
    if len(valores) == 0:
        return []
    arr = np.array(valores, dtype=float)
    somas_acumuladas = np.cumsum(arr)
    contagens = np.arange(1, len(arr) + 1, dtype=float)
    medias_acumuladas = somas_acumuladas / contagens
    return medias_acumuladas.tolist()
