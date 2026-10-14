"""Ponto de entrada principal da aplicação (Interface de Linha de Comando - CLI).

Permite interagir com a máquina caça-níqueis didática, visualizar uma rodada única
e disparar os cinco experimentos acadêmicos descritos no edital.
"""

import sys


def f_exibirCabecalho() -> None:
    """Exibe no terminal o cabeçalho do projeto e o aviso acadêmico obrigatório:

    'Simulador acadêmico - somente créditos fictícios'
    """
    pass


def f_executarRodadaDemonstrativa() -> None:
    """Realiza uma rodada única, sorteando a grade 3x3, destacando a linha central

    e informando o prêmio P e o lucro X obtidos.
    """
    pass


def f_menuPrincipal() -> None:
    """Apresenta o menu textual interativo com as opções disponíveis:

    1. Exibir uma rodada demonstrativa (tabuleiro 3x3 e premiação)
    2. Executar Experimento 1 (Frequências vs Probabilidades)
    3. Executar Experimento 2 (Lei dos Grandes Números e Monte Carlo)
    4. Executar Experimento 3 (Simulação com Saldo Limitado e Ruína)
    5. Executar Experimento 4 (Probabilidade Condicional e Falácia do Apostador)
    6. Executar Experimento 5 (Comparação com Tabela de Prêmios +10%)
    7. Executar todos os experimentos e gerar relatórios completos (CSVs e gráficos)
    0. Sair
    """
    pass


if __name__ == "__main__":
    f_menuPrincipal()
