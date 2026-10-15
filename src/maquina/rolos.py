"""Módulo responsável pela composição dos rolos e sorteio do tabuleiro 3x3.

Regras do edital (Seção 5):
- Sequência circular de símbolos: R = ('A', 'B', 'C', 'D', 'E'), posições 0 a 4.
- Sorteio uniforme de uma parada K em {0, 1, 2, 3, 4} (probabilidade 1/5 = 20% para cada posição).
- A coluna de uma rodada exibe 3 símbolos adjacentes do rolo:
    - Topo:   R[K]
    - Centro: R[(K + 1) mod 5]
    - Base:   R[(K + 2) mod 5]
- O sorteio é independente entre os três rolos e para cada rodada.
- As três células centrais são independentes entre si (probabilidade de tripla = (1/5)^3 = 1/125).
- As três células da mesma coluna NÃO são independentes (pois são posições vizinhas do mesmo rolo).
"""

from typing import Any, Tuple, List
import random


def f_definirSequenciaCircular() -> List[str]:
    """Retorna a sequência circular base de símbolos dos rolos da máquina.

    A sequência circular canônica é definida no edital como R = ('A', 'B', 'C', 'D', 'E'),
    com índices de 0 a 4.

    Retorna:
        List[str]: Lista ordenada com os 5 símbolos canônicos dos rolos.
    """
    return ["A", "B", "C", "D", "E"]


def f_sortearPosicaoK(gerador: Any) -> int:
    """Sorteia uniformemente a posição de parada K entre 0 e 4 utilizando o gerador pseudoaleatório.

    Cada posição k no conjunto {0, 1, 2, 3, 4} possui probabilidade equiprovável de 1/5 (20%).

    Argumentos:
        gerador: Instância inicializada do gerador pseudoaleatório (ex: random.Random ou numpy.random.Generator).

    Retorna:
        int: Índice sorteado K no intervalo [0, 4].
    """
    if hasattr(gerador, "randint"):
        return gerador.randint(0, 4)
    elif hasattr(gerador, "integers"):
        return int(gerador.integers(0, 5))
    elif hasattr(gerador, "choice"):
        return int(gerador.choice([0, 1, 2, 3, 4]))
    else:
        return random.randint(0, 4)


def f_obterJanelaColuna(posicaoK: int, sequenciaRolo: List[str] = None) -> Tuple[str, str, str]:
    """Extrai a janela visível de 3 posições de uma coluna a partir da parada K sorteada.

    Aplica a aritmética modular com operador mod 5 (Seção 5 do edital):
        - Topo:   R[K]
        - Centro: R[(K + 1) mod 5]
        - Base:   R[(K + 2) mod 5]

    Argumentos:
        posicaoK (int): Índice de parada sorteado K (0 a 4).
        sequenciaRolo (List[str], opcional): Lista de símbolos circulares. Se None, usa o padrão.

    Retorna:
        Tuple[str, str, str]: Uma tripla contendo (topo, centro, base) da coluna.
    """
    if sequenciaRolo is None:
        sequenciaRolo = f_definirSequenciaCircular()

    tamanho = len(sequenciaRolo)
    topo = sequenciaRolo[posicaoK % tamanho]
    centro = sequenciaRolo[(posicaoK + 1) % tamanho]
    base = sequenciaRolo[(posicaoK + 2) % tamanho]

    return (topo, centro, base)


def f_sortearTabuleiro3x3(gerador: Any) -> List[List[str]]:
    """Realiza três sorteios independentes para compor o tabuleiro completo 3x3 da rodada.

    A máquina possui 3 rolos verticais. Para cada rolo (coluna), uma posição K é sorteada
    de maneira independente. O tabuleiro final é representado como uma matriz 3x3:
    - Linha 0: Símbolos do topo (Rolo 1, Rolo 2, Rolo 3)
    - Linha 1: Símbolos do centro [LINHA AVALIADA] (Rolo 1, Rolo 2, Rolo 3)
    - Linha 2: Símbolos da base (Rolo 1, Rolo 2, Rolo 3)

    Argumentos:
        gerador: Instância do gerador de números aleatórios.

    Retorna:
        List[List[str]]: Matriz 3x3 onde linhas são [topo, centro, base]
                         e colunas representam os rolos 1, 2 e 3.
    """
    seq = f_definirSequenciaCircular()

    k1 = f_sortearPosicaoK(gerador)
    k2 = f_sortearPosicaoK(gerador)
    k3 = f_sortearPosicaoK(gerador)

    col1 = f_obterJanelaColuna(k1, seq)
    col2 = f_obterJanelaColuna(k2, seq)
    col3 = f_obterJanelaColuna(k3, seq)

    linha_topo = [col1[0], col2[0], col3[0]]
    linha_centro = [col1[1], col2[1], col3[1]]
    linha_base = [col1[2], col2[2], col3[2]]

    return [linha_topo, linha_centro, linha_base]


def f_extrairLinhaCentral(tabuleiro3x3: List[List[str]]) -> Tuple[str, str, str]:
    """Extrai os três símbolos da linha central da matriz 3x3.

    Conforme o edital, a linha central é a ÚNICA linha avaliada para premiação.

    Argumentos:
        tabuleiro3x3 (List[List[str]]): Matriz 3x3 retornada por `f_sortearTabuleiro3x3`.

    Retorna:
        Tuple[str, str, str]: Tripla de símbolos (Rolo1_centro, Rolo2_centro, Rolo3_centro).
    """
    return (tabuleiro3x3[1][0], tabuleiro3x3[1][1], tabuleiro3x3[1][2])


def f_formatarTabuleiroParaExibicao(tabuleiro3x3: List[List[str]]) -> str:
    """Gera uma representação textual clara da matriz 3x3 para exibição em console.

    Destaca visualmente a linha central com setas (ex: '==> [ B | B | B ] <== (Linha Central)').

    Argumentos:
        tabuleiro3x3 (List[List[str]]): Matriz 3x3 dos rolos.

    Retorna:
        str: String formatada pronta para impressão no terminal.
    """
    topo = f"    [ {tabuleiro3x3[0][0]} | {tabuleiro3x3[0][1]} | {tabuleiro3x3[0][2]} ] (Topo)"
    centro = f"==> [ {tabuleiro3x3[1][0]} | {tabuleiro3x3[1][1]} | {tabuleiro3x3[1][2]} ] <== (Linha Central Premiada)"
    base = f"    [ {tabuleiro3x3[2][0]} | {tabuleiro3x3[2][1]} | {tabuleiro3x3[2][2]} ] (Base)"

    separador = "    +---+---+---+"
    return f"{separador}\n{topo}\n{centro}\n{base}\n{separador}"
