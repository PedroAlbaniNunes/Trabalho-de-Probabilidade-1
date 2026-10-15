"""Módulo de geração de gráficos com Matplotlib.

Diretrizes visuais do edital (Seção 9 e 11):
- Manter apenas rótulos de eixos, unidades, categorias e identificações estritamente necessárias dentro do gráfico.
- Deixar títulos longos, números de figura e legendas formais para serem inseridos no corpo do relatório/LaTeX.
- Gráficos devem ser exportados em alta resolução (.png) na pasta 'resultados/figuras/'.
"""

from pathlib import Path
from typing import List, Dict, Any
import numpy as np
import matplotlib.pyplot as plt


def f_plotarComparacaoFrequenciasExp1(
    categorias: List[str],
    frequenciasTeoricas: List[float],
    frequenciasObservadas: List[float],
    caminhoSaida: Path
) -> None:
    """Gera um gráfico de barras comparando as probabilidades teóricas com as frequências observadas no E1."""
    caminho = Path(caminhoSaida)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    n_cat = len(categorias)
    x = np.arange(n_cat)
    largura = 0.38

    fig, ax = plt.subplots(figsize=(10, 5.5))

    barras_teoria = ax.bar(x - largura / 2, frequenciasTeoricas, largura, label="Teoria (%)", color="#1f77b4", alpha=0.9)
    barras_obs = ax.bar(x + largura / 2, frequenciasObservadas, largura, label="Observado (%)", color="#ff7f0e", alpha=0.9)

    ax.set_xlabel("Desfecho da Linha Central", fontsize=11, fontweight="bold")
    ax.set_ylabel("Frequência Relativa (%)", fontsize=11, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, fontsize=10)
    ax.legend(frameon=True, fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for b in barras_teoria:
        altura = b.get_height()
        ax.annotate(f"{altura:.2f}%",
                    xy=(b.get_x() + b.get_width() / 2, altura),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom", fontsize=8)

    for b in barras_obs:
        altura = b.get_height()
        ax.annotate(f"{altura:.2f}%",
                    xy=(b.get_x() + b.get_width() / 2, altura),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom", fontsize=8)

    y_max = max(max(frequenciasTeoricas), max(frequenciasObservadas))
    ax.set_ylim(0, y_max * 1.12)

    plt.tight_layout()
    plt.savefig(caminho, dpi=300)
    plt.close()


def f_plotarConvergenciaMediasExp2(
    trajetoriasPorSemente: Dict[int, List[float]],
    esperancaTeorica: float,
    caminhoSaida: Path
) -> None:
    """Plota as trajetórias de médias acumuladas de lucro para as 3 sementes (10, 2026, 123456) no E2."""
    caminho = Path(caminhoSaida)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(11, 5.8))

    cores = {
        10: "#2ca02c",      # verde
        2026: "#1f77b4",    # azul
        123456: "#9467bd",  # roxo
    }

    for semente, medias in trajetoriasPorSemente.items():
        n_pontos = len(medias)
        x = np.arange(1, n_pontos + 1)
        cor = cores.get(semente, "#333333")
        ax.plot(x, medias, label=f"Semente {semente}", color=cor, alpha=0.85, linewidth=1.2)

    ax.axhline(
        y=esperancaTeorica,
        color="#d62728",
        linestyle="--",
        linewidth=1.8,
        label=f"Teórico (E[X] = {esperancaTeorica:+.2f})"
    )

    ax.set_xlabel("Número de Rodadas (N)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Lucro Médio Acumulado (créditos)", fontsize=11, fontweight="bold")
    ax.legend(frameon=True, fontsize=10, loc="upper right")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.set_xlim(1, 10000)

    plt.tight_layout()
    plt.savefig(caminho, dpi=300)
    plt.close()


def f_plotarTrajetoriasSaldosExp3(
    trajetoriasCincoJogadores: List[List[float]],
    saldoInicial: float,
    caminhoSaida: Path
) -> None:
    """Plota as curvas de evolução de saldo dos 5 primeiros participantes virtuais no E3.

    Conforme o edital (Seção 7, Experimento 3):
    "um gráfico das trajetórias dos cinco primeiros participantes, sem selecionar os casos pela
    conclusão. Após a parada, manter o saldo constante no gráfico, se necessário."

    Argumentos:
        trajetoriasCincoJogadores (List[List[float]]): Lista contendo as 5 listas de evolução de saldo.
        saldoInicial (float): Saldo inicial de cada participante (padrão: 100.0 créditos).
        caminhoSaida (Path): Caminho completo onde a imagem .png será gravada.
    """
    caminho = Path(caminhoSaida)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(11, 6))

    cores = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    # Para cada jogador, se a sessão encerrou antes da rodada 500 (por ruína),
    # estender com o saldo constante de parada até o ponto 500.
    for i, serie in enumerate(trajetoriasCincoJogadores):
        serie_completa = list(serie)
        if len(serie_completa) < 501:
            ultimo_saldo = serie_completa[-1]
            serie_completa.extend([ultimo_saldo] * (501 - len(serie_completa)))

        x = np.arange(len(serie_completa))
        ax.plot(x, serie_completa, label=f"Jogador {i+1}", color=cores[i % len(cores)], linewidth=1.6, alpha=0.9)

    # Linha horizontal de referência do saldo inicial B_0 = 100
    ax.axhline(y=saldoInicial, color="#333333", linestyle="--", linewidth=1.2, label=f"Saldo Inicial (B0 = {saldoInicial:.0f})")

    # Linha horizontal de ruína / esgotamento B = 0
    ax.axhline(y=0, color="#d62728", linestyle=":", linewidth=1.4, label="Limiar de Ruína (Saldo < 1)")

    ax.set_xlabel("Rodada da Sessão (t)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Saldo do Jogador (créditos)", fontsize=11, fontweight="bold")
    ax.set_xlim(0, 500)
    ax.legend(frameon=True, fontsize=10, loc="upper right")
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(caminho, dpi=300)
    plt.close()
