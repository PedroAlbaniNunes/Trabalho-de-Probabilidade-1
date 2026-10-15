r"""Experimento 4: Depois de perder, aumenta a chance de ganhar?

Conceitos em ação (Seção 7 e 8 do edital):
- Probabilidade condicional: Pr(G_{i+1} | G_i) vs Pr(G_{i+1} | G_i^c).
- Independência estocástica entre rodadas consecutivas.
- Falácia do apostador e desmistificação da "máquina que deve prêmio".
"""

from typing import Dict, Any, List, Optional
from pathlib import Path

from src.configuracao import (
    DIRETORIO_TABELAS,
)
from src.analise.exportador import (
    f_exportarParaCsv,
)


def f_analisarParesConsecutivos(historicoPremios: List[float]) -> Dict[str, Any]:
    r"""Processa a lista sequencial de prêmios e agrupa os 9.999 pares consecutivos.

    Separa os pares (R_i, R_{i+1}) em dois conjuntos:
    - Grupo 1 (Após Prêmio): P_i > 0
    - Grupo 2 (Após Perda):  P_i == 0

    Args:
        historicoPremios (List[float]): Lista com os prêmios brutos P das 10.000 rodadas.

    Returns:
        Dict[str, Any]: Dicionário contendo contagens e proporções calculadas para cada grupo.
    """
    n_total_rodadas = len(historicoPremios)  # 10.000 rodadas
    n_pares = n_total_rodadas - 1  # 9.999 pares coladinhos (rodada i e rodada i+1)

    total_apos_premio = 0      # Quantas vezes a rodada anterior deu bom
    vitorias_apos_premio = 0   # E quantas dessas a rodada seguinte também deu bom

    total_apos_perda = 0       # Quantas vezes a rodada anterior foi um belo loss
    vitorias_apos_perda = 0    # E quantas dessas a rodada seguinte pagou prêmio

    # Varre a sequência pegando aos pares (ontem e hoje)
    for i in range(n_pares):
        premio_atual = historicoPremios[i]       # O que aconteceu no giro atual
        premio_proximo = historicoPremios[i + 1]  # O que aconteceu no giro seguinte
        vitoria_proxima = (premio_proximo > 0.0)  # Deu vitória no próximo giro?

        if premio_atual > 0.0:  # Se a rodada atual deu prêmio (vitória!)
            total_apos_premio += 1  # Joga pro grupo 'após vitória'
            if vitoria_proxima:
                vitorias_apos_premio += 1  # Repetiu a sorte!
        else:  # Se a rodada atual deu perda (96% dos casos)
            total_apos_perda += 1  # Joga pro grupo 'após derrota'
            if vitoria_proxima:
                vitorias_apos_perda += 1  # Pagou logo depois da derrota

    # Checagem de segurança pra ver se não perdemos nenhum par pelo caminho
    assert (total_apos_premio + total_apos_perda) == n_pares, f"Erro: soma de pares difere de {n_pares}"

    # Cálculo das proporções condicionais observadas (na moral, sem divisão por zero)
    if total_apos_premio > 0:
        prop_apos_premio_pct = (vitorias_apos_premio / total_apos_premio) * 100.0  # Taxa de ganho após ganhar
    else:
        prop_apos_premio_pct = None  # Se não teve vitória anterior, não dá pra estimar

    if total_apos_perda > 0:
        prop_apos_perda_pct = (vitorias_apos_perda / total_apos_perda) * 100.0  # Taxa de ganho após perder
    else:
        prop_apos_perda_pct = None  # Se não teve derrota anterior, não dá pra estimar

    total_vitorias_proximas = vitorias_apos_premio + vitorias_apos_perda  # Total geral de vitórias na segunda posição
    prop_total_pct = (total_vitorias_proximas / n_pares) * 100.0  # Média geral incondicional

    return {
        "n_pares": n_pares,
        "total_apos_premio": total_apos_premio,
        "vitorias_apos_premio": vitorias_apos_premio,
        "prop_apos_premio_pct": prop_apos_premio_pct,
        "total_apos_perda": total_apos_perda,
        "vitorias_apos_perda": vitorias_apos_perda,
        "prop_apos_perda_pct": prop_apos_perda_pct,
        "total_vitorias_proximas": total_vitorias_proximas,
        "prop_total_pct": prop_total_pct,
    }


def f_executarExperimento4(dadosExp1: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    r"""Executa o Experimento 4 reutilizando a sequência de 10.000 rodadas de E1.

    Testa se a chance de ganhar muda dependendo do que aconteceu na rodada anterior,
    desmistificando a Falácia do Apostador.

    Args:
        dadosExp1 (Optional[Dict[str, Any]]): Dados prévios da execução do Experimento 1 (semente 2026).

    Returns:
        Dict[str, Any]: Dicionário contendo a tabela de probabilidades condicionais e comparações.
    """
    # 1. Obter a sequência de rodadas do Experimento 1 (semente 2026)
    if dadosExp1 is None or "historico_premios_P" not in dadosExp1:
        from src.experimentos.exp1_frequencias import f_executarExperimento1
        dadosExp1 = f_executarExperimento1(semente=2026, totalRodadas=10_000)  # Roda E1 se necessário

    historico_premios = dadosExp1["historico_premios_P"]  # Puxa o extrato de prêmios das 10 mil rodadas

    # 2. Processar os 9.999 pares consecutivos
    res_pares = f_analisarParesConsecutivos(historico_premios)  # Passa o pente fino nos pares

    ref_teorica_pct = 4.00  # A probabilidade teórica incondicional (4%)

    # 3. Montar a tabela estruturada exigida pelo edital
    cabecalhos = [
        "Resultado Anterior",
        "Total de Pares",
        "Prêmios na Rodada Seguinte",
        "Proporção Observada (%)",
        "Referência Teórica (%)",
        "Diferença Amostral",
    ]

    linhas_tabela: List[List[Any]] = []

    # Linha: Após Prêmio (G_i)
    if res_pares["prop_apos_premio_pct"] is not None:
        prop_premio_str = f"{res_pares['prop_apos_premio_pct']:.2f}%"  # Deu ~4.13%
        dif_premio_str = f"{(res_pares['prop_apos_premio_pct'] - ref_teorica_pct):+.2f}%"
    else:
        prop_premio_str = "Não estimável"
        dif_premio_str = "-"

    linhas_tabela.append([
        "Após Prêmio (G_i)",
        res_pares["total_apos_premio"],
        res_pares["vitorias_apos_premio"],
        prop_premio_str,
        f"{ref_teorica_pct:.2f}%",
        dif_premio_str,
    ])

    # Linha: Após Perda (G_i^c)
    if res_pares["prop_apos_perda_pct"] is not None:
        prop_perda_str = f"{res_pares['prop_apos_perda_pct']:.2f}%"  # Deu ~4.12%
        dif_perda_str = f"{(res_pares['prop_apos_perda_pct'] - ref_teorica_pct):+.2f}%"
    else:
        prop_perda_str = "Não estimável"
        dif_perda_str = "-"

    linhas_tabela.append([
        "Após Perda (G_i^c)",
        res_pares["total_apos_perda"],
        res_pares["vitorias_apos_perda"],
        prop_perda_str,
        f"{ref_teorica_pct:.2f}%",
        dif_perda_str,
    ])

    # Linha: TOTAL (9.999 pares)
    linhas_tabela.append([
        "TOTAL (Todos os Pares)",
        res_pares["n_pares"],
        res_pares["total_vitorias_proximas"],
        f"{res_pares['prop_total_pct']:.2f}%",
        f"{ref_teorica_pct:.2f}%",
        f"{(res_pares['prop_total_pct'] - ref_teorica_pct):+.2f}%",
    ])

    # 4. Exportação para arquivo CSV
    caminho_csv = DIRETORIO_TABELAS / "exp4_prob_condicional.csv"
    f_exportarParaCsv(caminho_csv, cabecalhos, linhas_tabela)  # Cospe o CSV na pasta de resultados

    return {
        "n_pares": res_pares["n_pares"],
        "total_apos_premio": res_pares["total_apos_premio"],
        "vitorias_apos_premio": res_pares["vitorias_apos_premio"],
        "prop_apos_premio_pct": res_pares["prop_apos_premio_pct"],
        "total_apos_perda": res_pares["total_apos_perda"],
        "vitorias_apos_perda": res_pares["vitorias_apos_perda"],
        "prop_apos_perda_pct": res_pares["prop_apos_perda_pct"],
        "total_vitorias_proximas": res_pares["total_vitorias_proximas"],
        "prop_total_pct": res_pares["prop_total_pct"],
        "cabecalhos": cabecalhos,
        "linhas_tabela": linhas_tabela,
        "caminho_csv": caminho_csv,
    }
