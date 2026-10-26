"""Pacote com a implementação dos experimentos opcionais de Pontos Extras (Seção 10 do Edital).

Inclui:
- Extra 1: Intervalos de confiança (até 4 pontos).
- Extra 2: Mesma média, riscos diferentes (até 4 pontos).
- Extra 3: Limites de exposição e regras de parada (até 3 pontos).
- Extra 4: Análise de sensibilidade em múltiplos cenários (até 3 pontos).
- Extra 5: Interface acessível com auditoria WCAG 2.1 e controle por teclado (até 3 pontos).
"""

from src.extras.extra1_intervalos_confianca import f_executarExtra1IntervalosConfianca
from src.extras.extra2_riscos_diferentes import f_executarExtra2RiscosDiferentes
from src.extras.extra3_limites_exposicao import f_executarExtra3LimitesExposicao
from src.extras.extra4_analise_sensibilidade import f_executarExtra4AnaliseSensibilidade
from src.extras.extra5_interface_acessivel import (
    f_executarExtra5InterfaceAcessivel,
    f_iniciarJanelaAcessivelTkinter,
)

__all__ = [
    "f_executarExtra1IntervalosConfianca",
    "f_executarExtra2RiscosDiferentes",
    "f_executarExtra3LimitesExposicao",
    "f_executarExtra4AnaliseSensibilidade",
    "f_executarExtra5InterfaceAcessivel",
    "f_iniciarJanelaAcessivelTkinter",
]
