"""Módulo de persistência e exportação de dados em formatos tabulares (CSV, texto alinhado).

Garante a reprodutibilidade dos resultados exigida na Seção 4 e 5 do edital,
salvando os arquivos numéricos em 'resultados/tabelas/'.
"""

from pathlib import Path
from typing import Sequence, List, Any
import csv


def f_exportarParaCsv(caminhoArquivo: Path, cabecalhos: List[str], linhas: List[List[Any]]) -> None:
    """Exporta uma tabela para o formato CSV com codificação UTF-8 e delimitador padrão vírgula.

    Garante a criação automática das pastas parentes caso o diretório de destino não exista.

    Argumentos:
        caminhoArquivo (Path): Caminho completo do arquivo .csv de destino.
        cabecalhos (List[str]): Nomes das colunas da tabela.
        linhas (List[List[Any]]): Matriz de dados contendo os registros a serem salvos.
    """
    caminho = Path(caminhoArquivo)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    with open(caminho, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(cabecalhos)
        escritor.writerows(linhas)


def f_gerarTabelaFormatada(cabecalhos: List[str], linhas: List[List[Any]]) -> str:
    """Formata os dados tabulares em formato de texto visualmente alinhado para exibição no console.

    Argumentos:
        cabecalhos (List[str]): Nomes das colunas.
        linhas (List[List[Any]]): Matriz de dados.

    Retorna:
        str: String contendo a tabela visualmente formatada.
    """
    try:
        from tabulate import tabulate
        return tabulate(linhas, headers=cabecalhos, tablefmt="fancy_grid")
    except ImportError:
        # Fallback caso a biblioteca tabulate não esteja instalada
        linhas_str = [[str(item) for item in row] for row in linhas]
        larguras = [len(str(h)) for h in cabecalhos]
        for row in linhas_str:
            for i, val in enumerate(row):
                if len(val) > larguras[i]:
                    larguras[i] = len(val)

        separador = "+-" + "-+-".join(["-" * w for w in larguras]) + "-+"
        cabecalho_fmt = "| " + " | ".join([str(h).ljust(larguras[i]) for i, h in enumerate(cabecalhos)]) + " |"

        resultado = [separador, cabecalho_fmt, separador]
        for row in linhas_str:
            linha_fmt = "| " + " | ".join([val.ljust(larguras[i]) for i, val in enumerate(row)]) + " |"
            resultado.append(linha_fmt)
        resultado.append(separador)

        return "\n".join(resultado)
