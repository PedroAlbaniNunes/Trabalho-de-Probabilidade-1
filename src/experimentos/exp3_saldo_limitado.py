"""Experimento 3: O que acontece com um saldo limitado?

Conceitos em ação (Seção 7):
- Distribuição empírica de resultados com parada prematura (ruína do jogador).
- Comparação entre média e mediana em distribuições assimétricas.
- Horizonte de observação e variabilidade entre sessões.

Procedimento:
- Simular 100 participantes virtuais, cada um com saldo inicial de 100 créditos e aposta de 1 crédito.
- Regra de parada: sessão termina ao atingir 500 rodadas OU quando o saldo for inferior a 1 (esgotamento).
- Atualização do saldo: B_{t+1} = B_t + X_{t+1} (sem empréstimo ou reposição).
- A semente 42 deve ser inicializada UMA ÚNICA VEZ no início e mantida continuamente entre os participantes.
- Registrar saldo final, número de rodadas e se houve esgotamento.
- Apresentar proporções: ganho (B_f > 100), empate (B_f = 100), perda (B_f < 100).
- Apresentar taxa de esgotamento (subconjunto das perdas), média e mediana dos saldos finais.
- Gerar gráfico das trajetórias dos cinco primeiros participantes (mantendo o saldo constante após a parada).
"""

from typing import Dict, Any, List


def f_simularSessaoJogador(gerador: Any, saldoInicial: float = 100.0, maxRodadas: int = 500) -> Dict[str, Any]:
    """Simula a sessão individual de um jogador até atingir 500 rodadas ou esgotar o saldo (< 1).

    Argumentos:
        gerador: Instância contínua do gerador pseudoaleatório (não reinicializar a cada jogador).
        saldoInicial (float): Saldo inicial em créditos (padrão: 100.0).
        maxRodadas (int): Limite máximo de rodadas na sessão (padrão: 500).

    Retorna:
        Dict[str, Any]: Histórico contendo saldo final, total de rodadas jogadas,
                        booleano de esgotamento (ruína) e a lista da trajetória dos saldos.
    """
    pass


def f_executarExperimento3(semente: int = 42, numJogadores: int = 100) -> Dict[str, Any]:
    """Executa a simulação do Experimento 3 para os 100 participantes virtuais.

    Passos sugeridos:
    1. Inicializar o gerador com a semente 42 uma única vez.
    2. Simular sequencialmente os 100 participantes usando o mesmo fluxo de números pseudoaleatórios.
    3. Registrar os dados de cada participante em uma estrutura tabular:
       [idJogador, saldoFinal, rodadasJogadas, esgotou, categoria (ganho/empate/perda)].
    4. Calcular:
       - Proporções: ganho (B_f > 100), empate (B_f == 100), perda (B_f < 100).
       - Taxa de esgotamento (B_f < 1).
       - Média e mediana dos saldos finais.
    5. Exportar a tabela resumo e dados para 'resultados/tabelas/exp3_participantes.csv'.
    6. Plotar as trajetórias dos 5 primeiros participantes salvando em 'resultados/figuras/exp3_trajetorias.png'.

    Argumentos:
        semente (int): Semente do gerador (padrão: 42).
        numJogadores (int): Total de participantes virtuais (padrão: 100).

    Retorna:
        Dict[str, Any]: Métricas calculadas e histórico de trajetórias.
    """
    pass
