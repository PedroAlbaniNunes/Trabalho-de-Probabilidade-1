"""Módulo responsável pela composição dos rolos e sorteio do tabuleiro 3x3.

Regras do edital (Seção 5):
- Sequência circular de símbolos: R = ('A', 'B', 'C', 'D', 'E'), posições 0 a 4.
- Sorteio uniforme de uma parada K em {0, 1, 2, 3, 4} (probabilidade 1/5 para cada posição).
- A coluna exibe:
    - Topo:   R[K]
    - Centro: R[(K + 1) mod 5]
    - Base:   R[(K + 2) mod 5]
- O sorteio é independente entre os três rolos e para cada rodada.
"""

from typing import Any, Tuple, List


def f_definirSequenciaCircular() -> List[str]:
    """Retorna a sequência circular base de símbolos dos rolos: R = (A, B, C, D, E).

    Retorna:
        List[str]: Lista ordenada com os 5 símbolos.
    """
    pass


def f_sortearPosicaoK(gerador: Any) -> int:
    """Sorteia uniformemente a posição de parada K entre 0 e 4 utilizando o gerador pseudoaleatório.

    Argumentos:
        gerador: Instância do gerador de números aleatórios (ex: random.Random ou numpy.random.Generator).

    Retorna:
        int: Índice sorteado K no intervalo [0, 4].
    """
    pass


def f_obterJanelaColuna(posicaoK: int, sequenciaRolo: List[str] = None) -> Tuple[str, str, str]:
    """Aplica o operador circular mod 5 para extrair a janela visível de 3 posições da coluna.

    Topo:   R[K]
    Centro: R[(K + 1) mod 5]
    Base:   R[(K + 2) mod 5]

    Argumentos:
        posicaoK (int): Posição de parada sorteada K.
        sequenciaRolo (List[str], opcional): Sequência dos símbolos.

    Retorna:
        Tuple[str, str, str]: Uma tripla contendo (topo, centro, base).
    """
    pass


def f_sortearTabuleiro3x3(gerador: Any) -> List[List[str]]:
    """Realiza três sorteios independentes para compor o tabuleiro completo 3x3.

    Cada coluna é gerada a partir de sua própria parada independente K sorteada.

    Argumentos:
        gerador: Instância do gerador de números aleatórios.

    Retorna:
        List[List[str]]: Matriz 3x3 onde linhas representam (topo, centro, base)
                         e colunas representam os rolos 1, 2 e 3.
    """
    pass


def f_extrairLinhaCentral(tabuleiro3x3: List[List[str]]) -> Tuple[str, str, str]:
    """Extrai a combinação de símbolos presentes na linha central avaliada da grade.

    Argumentos:
        tabuleiro3x3 (List[List[str]]): Matriz 3x3 dos rolos.

    Retorna:
        Tuple[str, str, str]: Tripla de símbolos (Rolo1_centro, Rolo2_centro, Rolo3_centro).
    """
    pass


def f_formatarTabuleiroParaExibicao(tabuleiro3x3: List[List[str]]) -> str:
    """Gera uma representação textual visualmente amigável do tabuleiro 3x3 para exibição em terminal.

    Deve destacar visualmente a linha central, que é a única linha de pagamento.

    Argumentos:
        tabuleiro3x3 (List[List[str]]): Matriz 3x3.

    Retorna:
        str: String formatada pronta para print().
    """
    pass
