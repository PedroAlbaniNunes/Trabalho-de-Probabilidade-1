"""Módulo de configurações e constantes globais do simulador da máquina caça-níqueis.

Centraliza as constantes de regras do jogo, sementes pré-definidas pelo edital,
caminhos de diretórios para salvar resultados e mensagens obrigatórias.
"""

from pathlib import Path

# Mensagem legal e acadêmica obrigatória (Seção 5 do edital)
AVISO_LEGAL: str = "Simulador acadêmico - somente créditos fictícios"

# Símbolos disponíveis nos rolos
SIMBOLOS: list[str] = ["A", "B", "C", "D", "E"]
NUMERO_SIMBOLOS: int = len(SIMBOLOS)

# Custo padrão de cada rodada
CUSTO_APOSTA: float = 1.0

# Sementes canônicas fixadas no edital para reprodutibilidade
SEMENTE_EXP1: int = 2026
SEMENTES_EXP2: list[int] = [10, 2026, 123456]
SEMENTE_EXP3: int = 42

# Parâmetros de rodadas e jogadores
RODADAS_EXP1: int = 10_000
RODADAS_EXP2: int = 10_000
NUMERO_JOGADORES_EXP3: int = 100
SALDO_INICIAL_EXP3: float = 100.0
MAX_RODADAS_EXP3: int = 500

# Diretórios base do projeto
DIRETORIO_RAIZ: Path = Path(__file__).resolve().parent.parent
DIRETORIO_RESULTADOS: Path = DIRETORIO_RAIZ / "resultados"
DIRETORIO_TABELAS: Path = DIRETORIO_RESULTADOS / "tabelas"
DIRETORIO_FIGURAS: Path = DIRETORIO_RESULTADOS / "figuras"
DIRETORIO_TABELAS_EXTRAS: Path = DIRETORIO_TABELAS / "extras"
DIRETORIO_FIGURAS_EXTRAS: Path = DIRETORIO_FIGURAS / "extras"
