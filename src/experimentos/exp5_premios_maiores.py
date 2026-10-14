"""Experimento 5: Prêmios maiores tornam o jogo favorável?

Conceitos em ação (Seção 7):
- Esperança de uma função da variável aleatória.
- RTP sob alteração linear de premiações (+10%).
- Comparação pareada sob a mesma realização amostral (mesmas 10.000 rodadas de E1).

Procedimento:
- Aplicar a Tabela Base e a Tabela Prêmios +10% exatamente aos MESMOS 10.000 resultados do Experimento 1.
- Manter símbolos, probabilidades e aposta de 1 crédito inalterados.
- Gerar tabela comparativa contendo:
    - Probabilidade teórica de prêmio vs Frequência observada
    - Prêmio médio (teórico e observado)
    - Lucro médio (teórico e observado)
    - RTP (teórico e observado)
- Valores de referência teóricos com bônus de 10%:
    RTP_{+10%} = 1.10 * 0.84 = 92.4%
    E[X_{+10%}] = 0.924 - 1 = -0.076
- Exportar a tabela comparativa para CSV.
"""

from typing import Dict, Any, List, Optional


def f_executarExperimento5(dadosExp1: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Executa o Experimento 5 recalculando as métricas com a tabela +10% sobre as rodadas de E1.

    Passos sugeridos:
    1. Obter as 10.000 rodadas geradas no Experimento 1 (com semente 2026).
    2. Recalcular o prêmio bruto P e o lucro X de cada rodada sob a Tabela Prêmios +10%.
    3. Computar para ambas as tabelas (Base e +10%):
       - Probabilidade teórica e observada de prêmio (4%).
       - Prêmio médio observado e teórico.
       - Lucro médio observado e teórico (-0.16 vs -0.076).
       - RTP observado e teórico (84% vs 92.4%).
    4. Exportar a tabela comparativa para 'resultados/tabelas/exp5_comparacao_tabelas.csv'.

    Argumentos:
        dadosExp1 (Optional[Dict[str, Any]]): Dados da execução do Experimento 1.

    Retorna:
        Dict[str, Any]: Tabela comparativa com os resultados da Base e do Bônus +10%.
    """
    pass
