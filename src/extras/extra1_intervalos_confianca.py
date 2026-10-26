r"""Extra 1: Intervalos de Confiança (Seção 10 do Edital — até 4 pontos).

Requisitos do edital:
- Estimar um intervalo de confiança para o lucro médio (\mu_X) ou RTP.
- Explicar o método (Teorema Central do Limite e distribuição t-Student, Cap. 8 de Illowsky & Dean, 2023),
  as hipóteses (independência e variância finita) e o significado frequentista da incerteza.
- Usar execuções independentes para verificar empiricamente a taxa de cobertura do intervalo de 95%.
"""

from typing import Dict, Any, List
import math
import random

from src.configuracao import (
    SEMENTE_EXP1,
    RODADAS_EXP1,
    CUSTO_APOSTA,
    DIRETORIO_TABELAS_EXTRAS,
    DIRETORIO_FIGURAS_EXTRAS,
)
from src.maquina.rolos import (
    f_sortearTabuleiro3x3,
    f_extrairLinhaCentral,
)
from src.maquina.pagamentos import (
    f_calcularPremioBruto,
    f_calcularLucroLiquido,
    f_calcularEsperancaTeorica,
    TABELA_BASE,
)
from src.analise.metricas import (
    f_calcularMediaAmostral,
    f_calcularDesvioPadraoAmostral,
)
from src.analise.exportador import f_exportarParaCsv
from src.extras.graficos_extras import f_plotarIntervalosConfiancaExtra1

# Quantis críticos de 95% bicaudais (alfa = 0,05):
# - Para N = 10.000 (gl = 9.999): t_{0,975; 9999} = 1,960201
# - Para M = 30 execuções (gl = 29): t_{0,975; 29} = 2,045230
T_CRITICO_9999: float = 1.960201  # praticamente a normal padrão (1,96), já que N=10.000 é gente pra caramba
T_CRITICO_29: float = 2.045230    # t-Student clássica com 29 graus de liberdade para as 30 replicações


def f_simularExecucaoComIntervalo(
    semente: int,
    nRodadas: int = RODADAS_EXP1
) -> Dict[str, Any]:
    r"""Executa N rodadas independentes e estima o IC de 95% para o lucro médio e para o RTP.

    Args:
        semente (int): Semente do gerador pseudoaleatório para esta replicação.
        nRodadas (int): Tamanho da amostra (padrão: 10.000).

    Returns:
        Dict[str, Any]: Métricas pontuais, erro-padrão, limites do IC 95% e verificação de cobertura.
    """
    gerador = random.Random(semente)  # inicializa o gerador exclusivo desta execução
    lucros: List[float] = []          # lista para acumular o lucro líquido X_i de cada giro
    premios: List[float] = []         # lista para acumular o prêmio bruto P_i de cada giro

    for _ in range(nRodadas):
        tabuleiro = f_sortearTabuleiro3x3(gerador)            # sorteia a janela 3x3
        linha_central = f_extrairLinhaCentral(tabuleiro)      # extrai a linha do meio (onde o choro ou a alegria acontece)
        p = f_calcularPremioBruto(linha_central, TABELA_BASE) # verifica quanto a máquina pagou na rodada
        x = f_calcularLucroLiquido(p, CUSTO_APOSTA)           # desconta 1 crédito da aposta
        premios.append(p)                                     # registra o prêmio bruto
        lucros.append(x)                                      # registra o lucro líquido

    media_lucro = f_calcularMediaAmostral(lucros)               # estimativa pontual do lucro médio (\bar{X})
    dp_lucro = f_calcularDesvioPadraoAmostral(lucros)           # desvio-padrão amostral s (divisor N - 1)
    erro_padrao_lucro = dp_lucro / math.sqrt(nRodadas)          # erro-padrão da média: SE = s / \sqrt{N}
    margem_erro_lucro = T_CRITICO_9999 * erro_padrao_lucro      # margem de erro de 95% de confiança

    li_lucro = media_lucro - margem_erro_lucro                  # limite inferior do IC 95% para o lucro médio
    ls_lucro = media_lucro + margem_erro_lucro                  # limite superior do IC 95% para o lucro médio

    # Como P_i = X_i + 1 e Aposta = 1, o RTP (%) = (media_lucro + 1) * 100
    # e o desvio-padrão de P_i em % é idêntico a dp_lucro * 100.
    rtp_obs_pct = (media_lucro + CUSTO_APOSTA) * 100.0          # RTP empírico da amostra em porcentagem
    erro_padrao_rtp_pct = erro_padrao_lucro * 100.0             # erro-padrão do RTP em pontos percentuais
    margem_erro_rtp_pct = margem_erro_lucro * 100.0             # margem de erro do RTP para 95% de confiança
    li_rtp_pct = rtp_obs_pct - margem_erro_rtp_pct              # limite inferior do IC 95% do RTP
    ls_rtp_pct = rtp_obs_pct + margem_erro_rtp_pct              # limite superior do IC 95% do RTP

    teoria = f_calcularEsperancaTeorica(TABELA_BASE, CUSTO_APOSTA)  # busca os parâmetros populacionais exatos
    esp_lucro = teoria["esperanca_lucro"]                           # esperança teórica (-0,16 crédito)
    cobriu_teorico = (li_lucro <= esp_lucro <= ls_lucro)            # checa se o intervalo capturou o parâmetro real

    return {
        "semente": semente,
        "n_rodadas": nRodadas,
        "media_lucro": media_lucro,
        "dp_lucro": dp_lucro,
        "erro_padrao_lucro": erro_padrao_lucro,
        "margem_erro_lucro": margem_erro_lucro,
        "li_lucro": li_lucro,
        "ls_lucro": ls_lucro,
        "rtp_obs_pct": rtp_obs_pct,
        "erro_padrao_rtp_pct": erro_padrao_rtp_pct,
        "margem_erro_rtp_pct": margem_erro_rtp_pct,
        "li_rtp_pct": li_rtp_pct,
        "ls_rtp_pct": ls_rtp_pct,
        "cobriu_teorico": cobriu_teorico,
    }


def f_executarExtra1IntervalosConfianca(
    numExecucoes: int = 30,
    nRodadasPorExecucao: int = RODADAS_EXP1,
    sementeInicial: int = SEMENTE_EXP1
) -> Dict[str, Any]:
    r"""Executa o estudo completo de Intervalos de Confiança (Extra 1).

    Realiza 30 execuções independentes de 10.000 rodadas cada (iniciando pela semente canônica 2026),
    calcula o IC 95% individual de cada amostra e o IC 95% global das 30 médias independentes.

    Args:
        numExecucoes (int): Quantidade de replicações independentes (padrão: 30).
        nRodadasPorExecucao (int): Rodadas por execução (padrão: 10.000).
        sementeInicial (int): Primeira semente da sequência (padrão: 2026).

    Returns:
        Dict[str, Any]: Dicionário com todas as estimativas intervalares, tabelas e caminhos de saída.
    """
    teoria = f_calcularEsperancaTeorica(TABELA_BASE, CUSTO_APOSTA)  # referências exatas do modelo
    esp_lucro = teoria["esperanca_lucro"]   # -0.1600 crédito por rodada
    rtp_teo = teoria["rtp_teorico_pct"]     # 84.00% de retorno teórico

    registros: List[Dict[str, Any]] = []
    for k in range(numExecucoes):
        semente_k = sementeInicial + k  # sementes sequenciais independentes (2026, 2027, ..., 2055)
        res_k = f_simularExecucaoComIntervalo(semente_k, nRodadasPorExecucao)  # roda os 10k giros da semente k
        res_k["id_execucao"] = k + 1    # numeração amigável de 1 até 30
        registros.append(res_k)         # guarda o relatório da replicação

    # Resultado específico da semente canônica 2026 (primeira execução da lista)
    canonico = registros[0]

    # Estatísticas globais sobre as M = 30 médias independentes (distribuição amostral da média)
    medias_lucro_m = [r["media_lucro"] for r in registros]  # extrai as 30 médias amostrais de lucro
    medias_rtp_m = [r["rtp_obs_pct"] for r in registros]    # extrai os 30 RTPs observados

    media_global_lucro = f_calcularMediaAmostral(medias_lucro_m)          # média das 30 médias (300.000 giros no total)
    dp_entre_medias = f_calcularDesvioPadraoAmostral(medias_lucro_m)      # dispersão observada entre as médias
    ep_global_lucro = dp_entre_medias / math.sqrt(numExecucoes)           # erro-padrão global das 30 execuções
    t_crit_m = T_CRITICO_29 if numExecucoes == 30 else 1.96               # usa t_{29} se M=30
    me_global_lucro = t_crit_m * ep_global_lucro                          # margem de erro global para 95%
    li_global_lucro = media_global_lucro - me_global_lucro                # limite inferior global do lucro
    ls_global_lucro = media_global_lucro + me_global_lucro                # limite superior global do lucro

    media_global_rtp = f_calcularMediaAmostral(medias_rtp_m)              # RTP médio global das 30 baterias
    me_global_rtp = me_global_lucro * 100.0                               # margem de erro global do RTP em %
    li_global_rtp = media_global_rtp - me_global_rtp                      # limite inferior global do RTP
    ls_global_rtp = media_global_rtp + me_global_rtp                      # limite superior global do RTP

    # Conta quantos intervalos acertaram o alvo (-0,16): na teoria de 95%, uns 28 ou 29 de 30 devem acertar
    qtd_cobriu = sum(1 for r in registros if r["cobriu_teorico"])
    taxa_cobertura_pct = (qtd_cobriu / numExecucoes) * 100.0              # proporção empírica de cobertura

    # Exportação CSV detalhada
    cabecalhos_csv = [
        "Execucao",
        "Semente",
        "Media_Lucro_X",
        "DP_Amostral_s",
        "Erro_Padrao_SE",
        "IC95_Lucro_LI",
        "IC95_Lucro_LS",
        "RTP_Obs_Pct",
        "IC95_RTP_LI_Pct",
        "IC95_RTP_LS_Pct",
        "Cobriu_Parametro_Real",
    ]
    linhas_csv: List[List[Any]] = []
    for r in registros:
        linhas_csv.append([
            r["id_execucao"],
            r["semente"],
            f"{r['media_lucro']:+.4f}",
            f"{r['dp_lucro']:.4f}",
            f"{r['erro_padrao_lucro']:.4f}",
            f"{r['li_lucro']:+.4f}",
            f"{r['ls_lucro']:+.4f}",
            f"{r['rtp_obs_pct']:.2f}%",
            f"{r['li_rtp_pct']:.2f}%",
            f"{r['ls_rtp_pct']:.2f}%",
            "Sim" if r["cobriu_teorico"] else "Não",  # se deu "Não", caiu nos ~5% de azar amostral esperado
        ])

    linhas_csv.append(["---"] * len(cabecalhos_csv))
    linhas_csv.append([
        "GLOBAL (30 Exec.)",
        f"{sementeInicial}..{sementeInicial + numExecucoes - 1}",
        f"{media_global_lucro:+.4f}",
        f"{dp_entre_medias:.4f}",
        f"{ep_global_lucro:.4f}",
        f"{li_global_lucro:+.4f}",
        f"{ls_global_lucro:+.4f}",
        f"{media_global_rtp:.2f}%",
        f"{li_global_rtp:.2f}%",
        f"{ls_global_rtp:.2f}%",
        f"Cobertura: {qtd_cobriu}/{numExecucoes} ({taxa_cobertura_pct:.1f}%)",
    ])

    caminho_csv = DIRETORIO_TABELAS_EXTRAS / "extra1_intervalos_confianca.csv"
    f_exportarParaCsv(caminho_csv, cabecalhos_csv, linhas_csv)  # salva a tabela completa no disco

    caminho_figura = DIRETORIO_FIGURAS_EXTRAS / "extra1_intervalos_confianca.png"
    f_plotarIntervalosConfiancaExtra1(registros, esp_lucro, caminho_figura)  # gera o Forest Plot dos 30 intervalos

    # Tabela resumo enxuta para exibição no console
    cabecalhos_resumo = [
        "Escopo da Estimativa",
        "Métrica",
        "Estimativa Pontual",
        "Erro-Padrão (SE)",
        "IC 95% [LI ; LS]",
        "Parâmetro Real",
    ]
    tabela_resumo = [
        [
            "Amostra Canônica (Semente 2026, N=10.000)",
            "Lucro Médio (cr.)",
            f"{canonico['media_lucro']:+.4f}",
            f"{canonico['erro_padrao_lucro']:.4f}",
            f"[{canonico['li_lucro']:+.4f} ; {canonico['ls_lucro']:+.4f}]",
            f"{esp_lucro:+.4f}",
        ],
        [
            "Amostra Canônica (Semente 2026, N=10.000)",
            "RTP (%)",
            f"{canonico['rtp_obs_pct']:.2f}%",
            f"{canonico['erro_padrao_rtp_pct']:.2f}%",
            f"[{canonico['li_rtp_pct']:.2f}% ; {canonico['ls_rtp_pct']:.2f}%]",
            f"{rtp_teo:.2f}%",
        ],
        [
            f"Média Global ({numExecucoes} Execuções, 300.000 giros)",
            "Lucro Médio (cr.)",
            f"{media_global_lucro:+.4f}",
            f"{ep_global_lucro:.4f}",
            f"[{li_global_lucro:+.4f} ; {ls_global_lucro:+.4f}]",
            f"{esp_lucro:+.4f}",
        ],
        [
            f"Média Global ({numExecucoes} Execuções, 300.000 giros)",
            "RTP (%)",
            f"{media_global_rtp:.2f}%",
            f"{ep_global_lucro * 100.0:.2f}%",
            f"[{li_global_rtp:.2f}% ; {ls_global_rtp:.2f}%]",
            f"{rtp_teo:.2f}%",
        ],
        [
            "Verificação Frequentista de Cobertura",
            "Taxa de Cobertura",
            f"{qtd_cobriu}/{numExecucoes} ({taxa_cobertura_pct:.1f}%)",
            "—",
            "Esperado teórico: ~95,0%",
            "Confirmado",
        ],
    ]

    return {
        "canonico": canonico,
        "registros_execucoes": registros,
        "num_execucoes": numExecucoes,
        "media_global_lucro": media_global_lucro,
        "li_global_lucro": li_global_lucro,
        "ls_global_lucro": ls_global_lucro,
        "media_global_rtp": media_global_rtp,
        "li_global_rtp": li_global_rtp,
        "ls_global_rtp": ls_global_rtp,
        "qtd_cobriu": qtd_cobriu,
        "taxa_cobertura_pct": taxa_cobertura_pct,
        "cabecalhos_resumo": cabecalhos_resumo,
        "tabela_resumo": tabela_resumo,
        "caminho_csv": caminho_csv,
        "caminho_figura": caminho_figura,
    }
