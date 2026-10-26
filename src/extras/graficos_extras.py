"""Módulo de geração de gráficos exclusivos para os experimentos de Pontos Extras (Seção 10).

Segue rigorosamente as diretrizes visuais do edital (Seção 9 e 11):
- Manter apenas rótulos de eixos, unidades, categorias e identificações estritamente necessárias dentro do gráfico.
- Exportar figuras em alta resolução (300 DPI) na pasta 'resultados/figuras/extras/'.
"""

from pathlib import Path
from typing import List, Dict, Any
import numpy as np
import matplotlib.pyplot as plt


def f_plotarIntervalosConfiancaExtra1(
    registrosExecucoes: List[Dict[str, Any]],
    esperancaTeorica: float,
    caminhoSaida: Path
) -> None:
    """Gera um gráfico de intervalos de confiança (Forest Plot) para as M execuções independentes."""
    caminho = Path(caminhoSaida)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(11, 6.2))

    indices = np.arange(1, len(registrosExecucoes) + 1)
    medias = [r["media_lucro"] for r in registrosExecucoes]
    erros = [r["margem_erro_lucro"] for r in registrosExecucoes]
    cobriu_lista = [r["cobriu_teorico"] for r in registrosExecucoes]

    # Plota separadamente os intervalos que cobriram e os que não cobriram o parâmetro real
    idx_cobriu = [i for i, c in zip(indices, cobriu_lista) if c]
    med_cobriu = [m for m, c in zip(medias, cobriu_lista) if c]
    err_cobriu = [e for e, c in zip(erros, cobriu_lista) if c]

    idx_nao = [i for i, c in zip(indices, cobriu_lista) if not c]
    med_nao = [m for m, c in zip(medias, cobriu_lista) if not c]
    err_nao = [e for e, c in zip(erros, cobriu_lista) if not c]

    if idx_cobriu:
        ax.errorbar(
            idx_cobriu, med_cobriu, yerr=err_cobriu, fmt="o",
            color="#1f77b4", ecolor="#1f77b4", elinewidth=1.5, capsize=3.5,
            label="IC 95% (Contém E[X] = -0,16)"
        )
    if idx_nao:
        ax.errorbar(
            idx_nao, med_nao, yerr=err_nao, fmt="s",
            color="#d62728", ecolor="#d62728", elinewidth=1.8, capsize=4.0,
            label="IC 95% (Fora de E[X] = -0,16)"
        )

    ax.axhline(
        y=esperancaTeorica, color="#2ca02c", linestyle="--", linewidth=2.0,
        label=f"Parâmetro Real (E[X] = {esperancaTeorica:+.2f})"
    )

    ax.set_xlabel("Execução Independente (k = 1, ..., 30 | N = 10.000 rodadas cada)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Lucro Médio por Rodada e IC 95% (créditos)", fontsize=11, fontweight="bold")
    ax.set_xticks(indices)
    ax.set_xticklabels([str(r["semente"]) for r in registrosExecucoes], rotation=45, fontsize=8.5)
    ax.legend(frameon=True, fontsize=10, loc="upper right")
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(caminho, dpi=300)
    plt.close()


def f_plotarRiscosDiferentesExtra2(
    saldosPorPerfil: Dict[str, List[float]],
    resumoPerfis: List[Dict[str, Any]],
    caminhoSaida: Path
) -> None:
    """Plota a comparação de distribuição de saldos finais e taxas de ruína sob mesmo RTP (84%)."""
    caminho = Path(caminhoSaida)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

    nomes = list(saldosPorPerfil.keys())
    dados_saldos = [saldosPorPerfil[n] for n in nomes]
    cores = ["#2ca02c", "#1f77b4", "#d62728"]

    # Painel 1: Boxplot + Média dos saldos finais (100 jogadores)
    bp = ax1.boxplot(
        dados_saldos, patch_artist=True,
        showmeans=True,
        meanprops={"marker": "D", "markerfacecolor": "gold", "markeredgecolor": "black", "markersize": 7}
    )
    ax1.set_xticklabels(nomes, fontsize=9.5)
    for patch, cor in zip(bp["boxes"], cores):
        patch.set_facecolor(cor)
        patch.set_alpha(0.65)

    ax1.axhline(y=100.0, color="#333333", linestyle="--", linewidth=1.2, label="Saldo Inicial (100)")
    ax1.set_xlabel("Perfil de Volatilidade (Mesmo RTP = 84%)", fontsize=10.5, fontweight="bold")
    ax1.set_ylabel("Saldo Final após até 500 Rodadas (créditos)", fontsize=10.5, fontweight="bold")
    ax1.legend(frameon=True, fontsize=9, loc="upper left")
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    # Painel 2: Taxa de Ruína (%) vs Proporção de Ganho (%)
    x = np.arange(len(resumoPerfis))
    largura = 0.36
    taxas_ruina = [p["taxa_ruina_pct"] for p in resumoPerfis]
    taxas_ganho = [p["prop_ganho_pct"] for p in resumoPerfis]

    b1 = ax2.bar(x - largura / 2, taxas_ruina, largura, label="Taxa de Ruína (%)", color="#d62728", alpha=0.85)
    b2 = ax2.bar(x + largura / 2, taxas_ganho, largura, label="Sessões com Ganho (%)", color="#2ca02c", alpha=0.85)

    ax2.set_xlabel("Perfil de Volatilidade (Mesmo E[X] = -0,16)", fontsize=10.5, fontweight="bold")
    ax2.set_ylabel("Proporção de Participantes (%)", fontsize=10.5, fontweight="bold")
    ax2.set_xticks(x)
    ax2.set_xticklabels(nomes, fontsize=9.5)
    ax2.set_ylim(0, 105)
    ax2.legend(frameon=True, fontsize=9, loc="upper right")
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    for b in list(b1) + list(b2):
        h = b.get_height()
        ax2.annotate(
            f"{h:.1f}%",
            xy=(b.get_x() + b.get_width() / 2, h),
            xytext=(0, 3), textcoords="offset points",
            ha="center", va="bottom", fontsize=8.5
        )

    plt.tight_layout()
    plt.savefig(caminho, dpi=300)
    plt.close()


def f_plotarLimitesExposicaoExtra3(
    resultadosRegras: List[Dict[str, Any]],
    caminhoSaida: Path
) -> None:
    """Plota a comparação de desfechos e exposição média (rodadas jogadas) entre regras de parada."""
    caminho = Path(caminhoSaida)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

    nomes = [r["nome_curto"] for r in resultadosRegras]
    x = np.arange(len(nomes))
    largura = 0.25

    ganhos = [r["prop_ganho_pct"] for r in resultadosRegras]
    perdas = [r["prop_perda_pct"] for r in resultadosRegras]
    ruinas = [r["taxa_ruina_pct"] for r in resultadosRegras]

    b_g = ax1.bar(x - largura, ganhos, largura, label="Ganho (Bf > 100)", color="#2ca02c", alpha=0.85)
    b_p = ax1.bar(x, perdas, largura, label="Perda (Bf < 100)", color="#ff7f0e", alpha=0.85)
    b_r = ax1.bar(x + largura, ruinas, largura, label="Ruína Total (Bf < 1)", color="#d62728", alpha=0.85)

    ax1.set_xlabel("Regra de Parada Definida a Priori", fontsize=10.5, fontweight="bold")
    ax1.set_ylabel("Proporção de Participantes (%)", fontsize=10.5, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(nomes, fontsize=9)
    ax1.set_ylim(0, 105)
    ax1.legend(frameon=True, fontsize=9)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    for b in list(b_g) + list(b_p) + list(b_r):
        h = b.get_height()
        ax1.annotate(
            f"{h:.0f}%",
            xy=(b.get_x() + b.get_width() / 2, h),
            xytext=(0, 2), textcoords="offset points",
            ha="center", va="bottom", fontsize=8
        )

    # Painel 2: Exposição Média (Rodadas Jogadas) vs Saldo Final Médio
    rodadas_med = [r["media_rodadas"] for r in resultadosRegras]
    saldos_med = [r["media_saldo_final"] for r in resultadosRegras]

    b_rod = ax2.bar(x - largura / 2, rodadas_med, largura * 1.2, label="Exposição Média (Rodadas)", color="#1f77b4", alpha=0.85)
    b_sal = ax2.bar(x + largura / 2, saldos_med, largura * 1.2, label="Saldo Final Médio (Créditos)", color="#9467bd", alpha=0.85)

    ax2.set_xlabel("Regra de Parada Definida a Priori", fontsize=10.5, fontweight="bold")
    ax2.set_ylabel("Valor Médio Observado (Rodadas / Créditos)", fontsize=10.5, fontweight="bold")
    ax2.set_xticks(x)
    ax2.set_xticklabels(nomes, fontsize=9)
    ax2.set_ylim(0, max(rodadas_med) * 1.18)
    ax2.legend(frameon=True, fontsize=9)
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    for b in list(b_rod) + list(b_sal):
        h = b.get_height()
        ax2.annotate(
            f"{h:.1f}",
            xy=(b.get_x() + b.get_width() / 2, h),
            xytext=(0, 3), textcoords="offset points",
            ha="center", va="bottom", fontsize=8.5
        )

    plt.tight_layout()
    plt.savefig(caminho, dpi=300)
    plt.close()


def f_plotarAnaliseSensibilidadeExtra4(
    cenarios: List[Dict[str, Any]],
    caminhoSaida: Path
) -> None:
    """Plota o RTP Teórico vs Observado para todos os cenários da Análise de Sensibilidade."""
    caminho = Path(caminhoSaida)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(11.5, 5.8))

    rotulos = [c["rotulo_curto"] for c in cenarios]
    rtp_teo = [c["rtp_teorico_pct"] for c in cenarios]
    rtp_obs = [c["rtp_observado_pct"] for c in cenarios]

    x = np.arange(len(rotulos))
    largura = 0.36

    b_teo = ax.bar(x - largura / 2, rtp_teo, largura, label="RTP Teórico (%)", color="#1f77b4", alpha=0.9)
    b_obs = ax.bar(x + largura / 2, rtp_obs, largura, label="RTP Observado (N = 10.000) (%)", color="#ff7f0e", alpha=0.9)

    ax.axhline(
        y=100.0, color="#d62728", linestyle="--", linewidth=1.8,
        label="Limiar de Jogo Justo (RTP = 100% | E[X] = 0)"
    )

    ax.set_xlabel("Cenários de Sensibilidade (Variação de Pagamentos e Probabilidades)", fontsize=10.5, fontweight="bold")
    ax.set_ylabel("Retorno ao Jogador - RTP (%)", fontsize=10.5, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(rotulos, rotation=15, ha="right", fontsize=9)
    ax.set_ylim(0, max(max(rtp_teo), max(rtp_obs)) * 1.16)
    ax.legend(frameon=True, fontsize=9.5, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for b in list(b_teo) + list(b_obs):
        h = b.get_height()
        ax.annotate(
            f"{h:.1f}%",
            xy=(b.get_x() + b.get_width() / 2, h),
            xytext=(0, 3), textcoords="offset points",
            ha="center", va="bottom", fontsize=8
        )

    plt.tight_layout()
    plt.savefig(caminho, dpi=300)
    plt.close()


def f_plotarPainelAcessibilidadeExtra5(
    rotulosSimbolos: List[str],
    contribuicoesEsperanca: List[float],
    paresContraste: List[Dict[str, Any]],
    caminhoSaida: Path
) -> None:
    """Plota o painel visual acessível com paleta Okabe-Ito, hachuras geométricas e auditoria WCAG 2.1."""
    caminho = Path(caminhoSaida)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.8))

    # Painel 1: Contribuição x * Pr(X=x) com Paleta Okabe-Ito (segura para daltonismo) + Hachuras distintas
    # Cada barra é diferenciada por: (1) Posição/Rótulo com Forma, (2) Hachura geométrica, (3) Valor numérico, (4) Cor Okabe-Ito
    cores_okabe_ito = ["#0072B2", "#E69F00", "#009E73", "#56B4E9", "#CC79A7", "#D55E00"]
    hachuras = ["///", "\\\\\\", "xxx", "...", "+++", "---"]

    x1 = np.arange(len(rotulosSimbolos))
    barras1 = []
    for i in range(len(rotulosSimbolos)):
        b = ax1.bar(
            x1[i],
            contribuicoesEsperanca[i],
            width=0.58,
            color=cores_okabe_ito[i % len(cores_okabe_ito)],
            edgecolor="black",
            linewidth=1.2,
            hatch=hachuras[i % len(hachuras)],
            label=f"{rotulosSimbolos[i]} (hachura '{hachuras[i % len(hachuras)]}')"
        )
        barras1.append(b[0])

    ax1.axhline(y=0.0, color="black", linewidth=1.4)
    ax1.set_xlabel("Símbolo (Forma + Letra) — Redundância Não-Cromática", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Contribuição para E[X] = x · Pr(X=x) (créditos)", fontsize=10, fontweight="bold")
    ax1.set_xticks(x1)
    ax1.set_xticklabels(rotulosSimbolos, fontsize=9)
    ax1.set_ylim(-1.18, 0.58)
    ax1.legend(frameon=True, fontsize=8, loc="lower right")
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    for b in barras1:
        h = b.get_height()
        desloc_y = 4 if h >= 0 else -13
        ax1.annotate(
            f"{h:+.3f}",
            xy=(b.get_x() + b.get_width() / 2, h),
            xytext=(0, desloc_y), textcoords="offset points",
            ha="center", va="bottom", fontsize=8.5, fontweight="bold"
        )

    # Painel 2: Razão de Contraste WCAG 2.1 auditada nos componentes da interface
    nomes_pares = [p["componente_curto"] for p in paresContraste]
    razoes = [p["razao_contraste"] for p in paresContraste]
    x2 = np.arange(len(nomes_pares))

    barras2 = ax2.barh(
        x2, razoes, height=0.55,
        color="#0072B2", edgecolor="black", linewidth=1.1, hatch="//"
    )

    ax2.axvline(x=4.5, color="#E69F00", linestyle="--", linewidth=1.8, label="Mínimo WCAG AA (4,5:1)")
    ax2.axvline(x=7.0, color="#009E73", linestyle="-.", linewidth=2.0, label="Excelência WCAG AAA (7,0:1)")

    ax2.set_xlabel("Razão de Contraste Luminoso Auditada (CR : 1)", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Elemento Auditado da Interface", fontsize=10, fontweight="bold")
    ax2.set_yticks(x2)
    ax2.set_yticklabels(nomes_pares, fontsize=8.5)
    ax2.set_xlim(0, max(razoes) * 1.18)
    ax2.legend(frameon=True, fontsize=8.5, loc="lower right")
    ax2.grid(axis="x", linestyle="--", alpha=0.5)

    for b in barras2:
        larg = b.get_width()
        ax2.annotate(
            f"{larg:.2f}:1 (AAA)",
            xy=(larg, b.get_y() + b.get_height() / 2),
            xytext=(4, 0), textcoords="offset points",
            ha="left", va="center", fontsize=8, fontweight="bold"
        )

    plt.tight_layout()
    plt.savefig(caminho, dpi=300)
    plt.close()
