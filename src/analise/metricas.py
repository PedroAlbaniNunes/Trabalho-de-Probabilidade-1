r"""Módulo de cálculos estatísticos e funções matemáticas auxiliares.

Contém as fórmulas formais requeridas no edital:
- Média amostral: \bar{X} = \frac{1}{N} \sum_{i=1}^{N} X_i
- Desvio-padrão amostral (com divisor N - 1): s = \sqrt{\frac{1}{N - 1} \sum_{i=1}^{N} (X_i - \bar{X})^2}
- RTP observado: \widehat{RTP} = \left( \frac{\sum P_i}{\sum Aposta} \right) \times 100\%
- Mediana e médias cumulativas de Monte Carlo.
"""

from typing import List, Sequence, Dict
import math
import numpy as np


def f_calcularMediaAmostral(valores: Sequence[float]) -> float:
    r"""Calcula a média aritmética simples (\bar{X}) de uma sequência de valores observados.

    Fórmula:
        \bar{X} = \frac{1}{N} \sum_{i=1}^{N} X_i

    Args:
        valores (Sequence[float]): Coleção de valores numéricos (ex: lucros X_i).

    Returns:
        float: Média amostral calculada.
    """
    n = len(valores)  # Quantos dados temos na sacola
    if n == 0:  # Lista vazia? Sem dados, sem média
        return 0.0  # Evita o famigerado ZeroDivisionError na elegância
    return float(np.mean(valores))  # Deixa o NumPy mastigar a média na velocidade da luz


def f_calcularDesvioPadraoAmostral(valores: Sequence[float]) -> float:
    r"""Calcula o desvio-padrão amostral (s) utilizando estritamente o divisor N - 1.

    Conforme destacado na Seção 7 do edital:
    "Uma biblioteca pode calcular s, usando divisor N - 1. Explicar o significado da média e da
    dispersão, em créditos."

    Fórmula:
        s = \sqrt{ \frac{1}{N - 1} \sum_{i=1}^{N} (X_i - \bar{X})^2 }

    Args:
        valores (Sequence[float]): Coleção de valores observados com N >= 2.

    Returns:
        float: Desvio-padrão amostral s em créditos fictícios.
    """
    n = len(valores)  # Tamanho da amostra
    if n <= 1:  # Se só tem um gato pingado, não tem dispersão pra medir
        return 0.0  # Retorna zero sem pestanejar
    return float(np.std(valores, ddof=1))  # ddof=1 aplica o divisor N-1 na veia (correção de Bessel obrigatória!)


def f_calcularMediana(valores: Sequence[float]) -> float:
    """Calcula a mediana amostral de uma coleção de dados.

    Indispensável no Experimento 3 para revelar a realidade do apostador típico,
    sem ser iludido pela média inflacionada pelos sortudos com jackpot.

    Args:
        valores (Sequence[float]): Coleção de valores observados.

    Returns:
        float: Mediana calculada.
    """
    if len(valores) == 0:  # Se não tem ninguém na amostra
        return 0.0  # Retorna zero
    return float(np.median(valores))  # Ordena mentalmente e pega o cara bem do meio: o retrato fiel da galera


def f_calcularRtpObservado(totalPremios: float, totalApostado: float) -> float:
    r"""Calcula o retorno ao jogador observado (\widehat{RTP}) em termos percentuais.

    Fórmula:
        \widehat{RTP} = \left( \frac{\sum P_i}{\sum Aposta_i} \right) \times 100\%

    Args:
        totalPremios (float): Soma total de todos os prêmios brutos P pagos nas rodadas.
        totalApostado (float): Montante total de créditos apostados (ex: N * custo_aposta).

    Returns:
        float: Percentual de retorno observado (ex: 86.85 para 86,85%).
    """
    if totalApostado <= 0:  # Ninguém apostou nada?
        return 0.0  # Então não tem retorno nenhum pra calcular
    return float((totalPremios / totalApostado) * 100.0)  # Quanto do dinheiro que entrou voltou pro bolso dos jogadores


def f_calcularMediasAcumuladas(valores: Sequence[float]) -> List[float]:
    r"""Gera o vetor de médias cumulativas ao longo do avanço das rodadas.

    Para cada rodada k (de 1 até N):
        \bar{X}_k = \frac{1}{k} \sum_{i=1}^k X_i

    Args:
        valores (Sequence[float]): Lista sequencial dos lucros observados rodada a rodada.

    Returns:
        List[float]: Vetor de médias acumuladas de tamanho idêntico a `valores`.
    """
    if len(valores) == 0:  # Se não tem rodadas
        return []  # Devolve lista vazia
    arr = np.array(valores, dtype=float)  # Transforma num array NumPy pra acelerar o cálculo
    somas_acumuladas = np.cumsum(arr)  # Soma cumulativa rápida: cada posição soma tudo até ali
    contagens = np.arange(1, len(arr) + 1, dtype=float)  # Array [1, 2, 3, ..., N] com o número da rodada
    medias_acumuladas = somas_acumuladas / contagens  # Divide cada soma pelo número de giros até aquele momento
    return medias_acumuladas.tolist()  # Converte de volta pra lista Python clássica
