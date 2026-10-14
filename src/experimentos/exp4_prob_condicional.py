"""Experimento 4: Depois de perder, aumenta a chance de ganhar?

Conceitos em ação (Seção 7):
- Probabilidade condicional: Pr(G_{i+1} | G_i) vs Pr(G_{i+1} | G_i^c).
- Independência estocástica entre rodadas consecutivas.
- Falácia do apostador e desmistificação da "máquina que deve prêmio".

Procedimento:
- Reutilizar a sequência de 10.000 rodadas do Experimento 1.
- Analisar os 9.999 pares de rodadas consecutivas (rodada i e rodada i+1).
- Separar os pares em dois grupos conforme o resultado da rodada i:
    1. Grupo "Após Prêmio": P_i > 0
    2. Grupo "Após Perda":  P_i == 0
- Para cada grupo, contar quantas vezes a rodada i+1 foi premiada (P_{i+1} > 0).
- Calcular as probabilidades condicionais empíricas e comparar com a referência teórica (4%).
- Gerar tabela com: resultado anterior, total de pares, prêmios na rodada seguinte e proporção.
- Exportar para CSV.
"""

from typing import Dict, Any, List, Optional


def f_analisarParesConsecutivos(historicoPremios: List[float]) -> Dict[str, Any]:
    """Processa a lista sequencial de prêmios e agrupa os 9.999 pares consecutivos.

    Argumentos:
        historicoPremios (List[float]): Lista com os prêmios brutos das 10.000 rodadas.

    Retorna:
        Dict[str, Any]: Contagens e proporções calculadas para os grupos 'apos_premio' e 'apos_perda'.
    """
    pass


def f_executarExperimento4(dadosExp1: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Executa o Experimento 4 reutilizando a sequência de 10.000 rodadas de E1.

    Passos sugeridos:
    1. Obter a sequência de rodadas do Experimento 1.
    2. Formar os 9.999 pares consecutivos (i, i+1).
    3. Segmentar os pares entre os grupos 'Após Prêmio' e 'Após Perda'.
    4. Calcular as frequências relativas condicionais (tratando caso com zero pares se ocorrer).
    5. Exportar a tabela para 'resultados/tabelas/exp4_prob_condicional.csv'.

    Argumentos:
        dadosExp1 (Optional[Dict[str, Any]]): Dados da execução prévia do Experimento 1.

    Retorna:
        Dict[str, Any]: Tabela com as probabilidades condicionais e comparações com a teoria (4%).
    """
    pass
