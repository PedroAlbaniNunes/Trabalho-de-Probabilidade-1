r"""Módulo responsável pela composição dos rolos e sorteio do tabuleiro 3x3.

Regras do edital (Seção 5):
- Sequência circular de símbolos: R = ('A', 'B', 'C', 'D', 'E'), posições de 0 a 4.
- Sorteio uniforme de uma parada K em {0, 1, 2, 3, 4} (chance de 1/5 = 20% cada).
- A coluna de uma rodada exibe 3 símbolos adjacentes do rolo:
    - Topo:   R[K]
    - Centro: R[(K + 1) mod 5] (Linha que paga!)
    - Base:   R[(K + 2) mod 5]
- O sorteio é independente entre os três rolos e para cada rodada.
"""

from typing import Any, Tuple, List
import random


def f_definirSequenciaCircular() -> List[str]:
    """Retorna a sequência circular base de símbolos dos rolos da máquina.

    A sequência canônica oficial do edital é R = ('A', 'B', 'C', 'D', 'E'),
    com índices de 0 a 4 simulando uma fita física de caça-níqueis.

    Returns:
        List[str]: Lista ordenada com os 5 símbolos canônicos dos rolos.
    """
    return ["A", "B", "C", "D", "E"]  # A nossa 'fita' circular que fica girando na máquina


def f_sortearPosicaoK(gerador: Any) -> int:
    """Sorteia uniformemente a posição de parada K entre 0 e 4 utilizando o gerador pseudoaleatório.

    Cada posição k no conjunto {0, 1, 2, 3, 4} possui probabilidade equiprovável de 1/5 (20%).

    Args:
        gerador (Any): Instância inicializada do gerador pseudoaleatório (random.Random ou np.random).

    Returns:
        int: Índice sorteado K no intervalo fechado [0, 4].
    """
    if hasattr(gerador, "randint"):  # Se for o gerador nativo do Python, manda no randint
        return gerador.randint(0, 4)  # Trava o rolo num ponto entre 0 e 4 (sem vício, na honestidade)
    elif hasattr(gerador, "integers"):  # Se for o gerador moderno do NumPy
        return int(gerador.integers(0, 5))  # No numpy o limite superior é aberto, então vai até 5
    elif hasattr(gerador, "choice"):  # Se for um gerador que tem choice
        return int(gerador.choice([0, 1, 2, 3, 4]))  # Puxa uma das 5 posições no uni-duni-tê
    else:
        return random.randint(0, 4)  # Plano de emergência: usa o random global se nada mais der certo


def f_obterJanelaColuna(posicaoK: int, sequenciaRolo: List[str] = None) -> Tuple[str, str, str]:
    r"""Extrai a janela visível de 3 posições de uma coluna a partir da parada K sorteada.

    Aplica a aritmética modular com operador mod 5 (Seção 5 do edital):
        - Topo:   R[K]
        - Centro: R[(K + 1) mod 5]
        - Base:   R[(K + 2) mod 5]

    Args:
        posicaoK (int): Índice de parada sorteado K (0 a 4).
        sequenciaRolo (List[str], optional): Lista de símbolos circulares. Se None, usa o padrão.

    Returns:
        Tuple[str, str, str]: Uma tripla contendo (topo, centro, base) da coluna.
    """
    if sequenciaRolo is None:
        sequenciaRolo = f_definirSequenciaCircular()  # Se não passou nada, puxa a fita padrão A-B-C-D-E

    tamanho = len(sequenciaRolo)  # Tamanho da fita (5 símbolos)
    topo = sequenciaRolo[posicaoK % tamanho]  # Símbolo do topo (só pra fazer número no visual)
    centro = sequenciaRolo[(posicaoK + 1) % tamanho]  # Esse é o astro da festa! O miolo que decide se tem dindin
    base = sequenciaRolo[(posicaoK + 2) % tamanho]  # Símbolo da base (também só figuração no visor)

    return (topo, centro, base)  # Devolve a coluna prontinha como aparece no vidro do cassino


def f_sortearTabuleiro3x3(gerador: Any) -> List[List[str]]:
    """Realiza três sorteios independentes para compor o tabuleiro completo 3x3 da rodada.

    A máquina possui 3 rolos verticais girando de forma totalmente independente.

    Args:
        gerador (Any): Instância do gerador de números aleatórios.

    Returns:
        List[List[str]]: Matriz 3x3 onde linhas são [topo, centro, base]
                         e colunas representam os rolos 1, 2 e 3.
    """
    seq = f_definirSequenciaCircular()  # Carrega a sequência base de símbolos

    k1 = f_sortearPosicaoK(gerador)  # Rolo 1 rodando... e travou na posição k1!
    k2 = f_sortearPosicaoK(gerador)  # Rolo 2 rodando... e travou na posição k2!
    k3 = f_sortearPosicaoK(gerador)  # Rolo 3 rodando... e travou na posição k3!

    col1 = f_obterJanelaColuna(k1, seq)  # Monta a visualização da primeira coluna
    col2 = f_obterJanelaColuna(k2, seq)  # Monta a visualização da segunda coluna
    col3 = f_obterJanelaColuna(k3, seq)  # Monta a visualização da terceira coluna

    linha_topo = [col1[0], col2[0], col3[0]]  # Junta a linha de cima dos 3 rolos
    linha_centro = [col1[1], col2[1], col3[1]]  # Junta a linha do meio (a única que vale Pix!)
    linha_base = [col1[2], col2[2], col3[2]]  # Junta a linha de baixo dos 3 rolos

    return [linha_topo, linha_centro, linha_base]  # Entrega a grade 3x3 completa montada


def f_extrairLinhaCentral(tabuleiro3x3: List[List[str]]) -> Tuple[str, str, str]:
    """Extrai os três símbolos da linha central da matriz 3x3.

    Conforme o edital, a linha central é a ÚNICA linha avaliada para premiação.

    Args:
        tabuleiro3x3 (List[List[str]]): Matriz 3x3 retornada por `f_sortearTabuleiro3x3`.

    Returns:
        Tuple[str, str, str]: Tripla de símbolos (Rolo1_centro, Rolo2_centro, Rolo3_centro).
    """
    return (tabuleiro3x3[1][0], tabuleiro3x3[1][1], tabuleiro3x3[1][2])  # Pesca cirurgicamente só a linha premiada


def f_formatarTabuleiroParaExibicao(tabuleiro3x3: List[List[str]]) -> str:
    """Gera uma representação textual clara da matriz 3x3 para exibição em console.

    Destaca visualmente a linha central com setas para facilitar o acompanhamento do jogador.

    Args:
        tabuleiro3x3 (List[List[str]]): Matriz 3x3 dos rolos.

    Returns:
        str: String formatada pronta para impressão no terminal.
    """
    topo = f"    [ {tabuleiro3x3[0][0]} | {tabuleiro3x3[0][1]} | {tabuleiro3x3[0][2]} ] (Topo)"  # Linha decorativa
    centro = f"==> [ {tabuleiro3x3[1][0]} | {tabuleiro3x3[1][1]} | {tabuleiro3x3[1][2]} ] <== (Linha Central Premiada)"  # Destaque com holofote
    base = f"    [ {tabuleiro3x3[2][0]} | {tabuleiro3x3[2][1]} | {tabuleiro3x3[2][2]} ] (Base)"  # Linha decorativa

    separador = "    +---+---+---+"  # Gradezinha simpática de terminal
    return f"{separador}\n{topo}\n{centro}\n{base}\n{separador}"  # Junta tudo no layout bonitão
