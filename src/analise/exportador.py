"""Módulo de persistência e exportação de dados em formatos tabulares (CSV, Markdown)."""

from pathlib import Path
from typing import Sequence, List, Any, Dict


def f_exportarParaCsv(caminhoArquivo: Path, cabecalhos: List[str], linhas: List[List[Any]]) -> None:
    """Exporta uma tabela para o formato CSV com codificação UTF-8.

    Argumentos:
        caminhoArquivo (Path): Caminho de destino para salvar o arquivo .csv.
        cabecalhos (List[str]): Nomes das colunas da tabela.
        linhas (List[List[Any]]): Matriz de dados com as linhas a serem salvas.
    """
    pass


def f_gerarTabelaFormatada(cabecalhos: List[str], linhas: List[List[Any]]) -> str:
    """Formata os dados tabulares em formato de texto legível para exibição no terminal ou console.

    Argumentos:
        cabecalhos (List[str]): Nomes das colunas.
        linhas (List[List[Any]]): Dados das linhas.

    Retorna:
        str: String contendo a tabela visualmente alinhada.
    """
    pass
