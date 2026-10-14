"""Experimento 1: As frequências acompanham as probabilidades?

Conceitos em ação (Seção 7):
- Espaço amostral e eventos equiprováveis (125 triplas).
- Variável discreta (Lucro líquido X e Prêmio P).
- Frequência relativa vs Probabilidade teórica.
- Média amostral, desvio-padrão amostral com divisor N - 1 e RTP observado.

Procedimento:
- Executar 10.000 rodadas com a semente 2026.
- Contar os seis resultados da Tabela 1.
- Gerar tabela em CSV e gráfico de barras comparativo (teoria vs observação).
- Salvar os dados para reutilização nos experimentos posteriores (E2, E4, E5).
"""

from typing import Dict, Any, List


def f_executarExperimento1(semente: int = 2026, totalRodadas: int = 10_000) -> Dict[str, Any]:
    """Executa a simulação do Experimento 1.

    Passos sugeridos:
    1. Inicializar o gerador pseudoaleatório com a semente fornecida (uma única vez).
    2. Simular as 10.000 rodadas registrando linha central, prêmio P e lucro X de cada rodada.
    3. Contar as ocorrências dos 6 desfechos (A-A-A, B-B-B, C-C-C, D-D-D, E-E-E, Sem prêmio).
    4. Calcular:
        - Média amostral do lucro (X_barra = sum(X_i) / N)
        - RTP observado (RTP_chapeu = sum(P_i) / N)
        - Proporção de rodadas premiadas
        - Desvio-padrão amostral (s) com divisor N - 1
    5. Exportar a tabela para CSV em 'resultados/tabelas/exp1_frequencias.csv'.
    6. Gerar o gráfico de barras comparativo em 'resultados/figuras/exp1_frequencias.png'.

    Argumentos:
        semente (int): Semente para o gerador (padrão: 2026).
        totalRodadas (int): Número de rodadas (padrão: 10.000).

    Retorna:
        Dict[str, Any]: Dicionário contendo os resultados resumidos e o histórico
                        das 10.000 rodadas (necessário para reaproveitamento em E2, E4 e E5).
    """
    pass
