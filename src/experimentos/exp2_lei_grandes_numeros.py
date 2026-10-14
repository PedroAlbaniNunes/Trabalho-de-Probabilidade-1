"""Experimento 2: O que muda quando aumentamos a amostra?

Conceitos em ação (Seção 7):
- Simulação de Monte Carlo e convergência assintótica.
- Média acumulada ao longo das rodadas.
- Lei dos Grandes Números (LLN).
- Reprodutibilidade e verificação estrita de sementes.

Procedimento:
- Simular três sequências de 10.000 rodadas com sementes 10, 2026 e 123456.
- Reutilizar a sequência de 2026 gerada no Experimento 1.
- Para cada execução, registrar a média acumulada de lucros após 100, 1.000 e 10.000 rodadas.
- Gerar tabela 3x3 de médias acumuladas e exportar para CSV.
- Gerar gráfico com as três trajetórias de convergência e a linha horizontal de referência E[X] = -0.16.
- Repetir a semente 2026 no mesmo ambiente e checar se os 10 primeiros resultados são idênticos.
"""

from typing import Dict, Any, List, Optional


def f_verificarReprodutibilidadePrimeirosResultados(semente: int = 2026, nResultados: int = 10) -> bool:
    """Verifica se os n primeiros resultados sorteados com a semente especificada são idênticos entre execuções.

    Argumentos:
        semente (int): Semente utilizada (padrão: 2026).
        nResultados (int): Quantidade de resultados a checar (padrão: 10).

    Retorna:
        bool: True se os resultados foram rigorosamente reproduzidos, False caso contrário.
    """
    pass


def f_executarExperimento2(dadosExp1: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Executa a simulação do Experimento 2.

    Passos sugeridos:
    1. Utilizar os resultados da semente 2026 obtidos em E1 (ou gerá-los se não fornecidos).
    2. Simular 10.000 rodadas para a semente 10 e 10.000 rodadas para a semente 123456.
    3. Para cada semente, computar o vetor de médias acumuladas de lucro:
        mediaAcumulada[k] = sum(lucros[:k]) / k
    4. Montar a tabela 3x3 com as médias acumuladas nos marcos N = 100, N = 1.000 e N = 10.000.
    5. Exportar a tabela para 'resultados/tabelas/exp2_medias_acumuladas.csv'.
    6. Plotar o gráfico com as 3 trajetórias e a linha horizontal em E[X] = -0.16
       salvando em 'resultados/figuras/exp2_convergencia.png'.
    7. Validar e registrar no resultado se os 10 primeiros resultados foram reproduzidos.

    Argumentos:
        dadosExp1 (Optional[Dict[str, Any]]): Dados prévios da execução do Experimento 1.

    Retorna:
        Dict[str, Any]: Dicionário contendo a tabela 3x3, trajetórias e status de reprodução.
    """
    pass
