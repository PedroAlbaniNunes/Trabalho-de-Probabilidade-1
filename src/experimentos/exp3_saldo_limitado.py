r"""Experimento 3: O que acontece com um saldo limitado?

Conceitos em ação (Seção 7 e 8 do edital):
- Distribuição empírica de resultados com parada prematura (tempo de parada e ruína do jogador).
- Comparação entre média e mediana em distribuições de lucros com assimetria positiva.
- Horizonte de observação e variabilidade entre sessões de apostadores.
- Desmistificação de relatos isolados de sucesso (viés do sobrevivente).

Procedimento estipulado pelo edital:
- Simular 100 participantes virtuais, cada um com saldo inicial de 100 créditos e aposta de 1 crédito.
- Regra de parada: sessão termina ao atingir 500 rodadas OU quando o saldo for inferior a 1 (esgotamento).
- Atualização do saldo: B_{t+1} = B_t + X_{t+1} (sem empréstimo ou reposição).
- A semente 42 deve ser inicializada UMA ÚNICA VEZ no início e mantida continuamente entre os participantes.
- Registrar saldo final, número de rodadas e se houve esgotamento.
- Apresentar proporções: ganho (B_f > 100), empate (B_f = 100), perda (B_f < 100), somando rigorosamente 100%.
- Apresentar taxa de esgotamento (subconjunto das perdas), média e mediana dos saldos finais.
- Gerar gráfico das trajetórias dos cinco primeiros participantes (mantendo o saldo constante após a parada até a rodada 500).
"""

from typing import Dict, Any, List
import random
from pathlib import Path

from src.configuracao import (
    SEMENTE_EXP3,
    NUMERO_JOGADORES_EXP3,
    SALDO_INICIAL_EXP3,
    MAX_RODADAS_EXP3,
    CUSTO_APOSTA,
    DIRETORIO_TABELAS,
    DIRETORIO_FIGURAS,
)
from src.maquina.rolos import (
    f_sortearTabuleiro3x3,
    f_extrairLinhaCentral,
)
from src.maquina.pagamentos import (
    f_calcularPremioBruto,
    f_calcularLucroLiquido,
    TABELA_BASE,
)
from src.analise.metricas import (
    f_calcularMediaAmostral,
    f_calcularMediana,
)
from src.analise.exportador import (
    f_exportarParaCsv,
    f_gerarTabelaFormatada,
)
from src.analise.graficos import (
    f_plotarTrajetoriasSaldosExp3,
)


def f_simularSessaoJogador(gerador: Any, saldoInicial: float = SALDO_INICIAL_EXP3, maxRodadas: int = MAX_RODADAS_EXP3) -> Dict[str, Any]:
    r"""Simula a sessão individual de um apostador até o tempo de parada (500 rodadas ou ruína B < 1).

    Argumentos:
        gerador: Instância do gerador pseudoaleatório compartilhada entre participantes.
        saldoInicial (float): Saldo de partida em créditos (padrão do edital: 100.0).
        maxRodadas (int): Limite máximo de rodadas na sessão (padrão do edital: 500).

    Retorna:
        Dict[str, Any]: Dicionário contendo histórico de saldos, saldo final, rodadas jogadas e esgotamento.
    """
    saldo = float(saldoInicial)
    trajetoria: List[float] = [saldo]
    rodadas_jogadas = 0

    while rodadas_jogadas < maxRodadas and saldo >= 1.0:
        tabuleiro = f_sortearTabuleiro3x3(gerador)
        linha_central = f_extrairLinhaCentral(tabuleiro)

        premio_P = f_calcularPremioBruto(linha_central, TABELA_BASE)
        lucro_X = f_calcularLucroLiquido(premio_P, CUSTO_APOSTA)

        saldo += lucro_X
        rodadas_jogadas += 1
        trajetoria.append(saldo)

    esgotou = (saldo < 1.0)

    return {
        "saldo_final": saldo,
        "rodadas_jogadas": rodadas_jogadas,
        "esgotou": esgotou,
        "trajetoria_saldos": trajetoria,
    }


def f_executarExperimento3(semente: int = SEMENTE_EXP3, numJogadores: int = NUMERO_JOGADORES_EXP3) -> Dict[str, Any]:
    r"""Executa a simulação completa do Experimento 3 para os 100 participantes virtuais.

    Argumentos:
        semente (int): Semente do gerador pseudoaleatório (padrão: 42).
        numJogadores (int): Total de participantes virtuais (padrão: 100).

    Retorna:
        Dict[str, Any]: Dicionário contendo todas as métricas calculadas e trajetórias.
    """
    # 1. Inicializar o gerador pseudoaleatório uma única vez e continuar entre participantes
    gerador = random.Random(semente)

    participantes: List[Dict[str, Any]] = []

    # 2. Simular as sessões sequenciais dos 100 jogadores virtuais
    for id_jogador in range(1, numJogadores + 1):
        sessao = f_simularSessaoJogador(gerador, SALDO_INICIAL_EXP3, MAX_RODADAS_EXP3)
        saldo_f = sessao["saldo_final"]

        if saldo_f > SALDO_INICIAL_EXP3:
            categoria = "Ganho"
        elif saldo_f == SALDO_INICIAL_EXP3:
            categoria = "Empate"
        else:
            categoria = "Perda"

        participantes.append({
            "id_jogador": id_jogador,
            "saldo_final": saldo_f,
            "rodadas_jogadas": sessao["rodadas_jogadas"],
            "esgotou": sessao["esgotou"],
            "categoria": categoria,
            "trajetoria_saldos": sessao["trajetoria_saldos"],
        })

    # 3. Contagem e cálculo das proporções (somando exatamente 100%)
    n_ganho = sum(1 for p in participantes if p["categoria"] == "Ganho")
    n_empate = sum(1 for p in participantes if p["categoria"] == "Empate")
    n_perda = sum(1 for p in participantes if p["categoria"] == "Perda")
    assert (n_ganho + n_empate + n_perda) == numJogadores, "Erro: categorias de saldo não somam 100!"

    prop_ganho_pct = (n_ganho / numJogadores) * 100.0
    prop_empate_pct = (n_empate / numJogadores) * 100.0
    prop_perda_pct = (n_perda / numJogadores) * 100.0

    # Taxa de esgotamento (ruína do jogador, subconjunto das perdas)
    n_esgotados = sum(1 for p in participantes if p["esgotou"])
    taxa_esgotamento_pct = (n_esgotados / numJogadores) * 100.0

    # 4. Cálculo de medidas de centro (média vs mediana)
    saldos_finais = [p["saldo_final"] for p in participantes]
    media_saldo_final = f_calcularMediaAmostral(saldos_finais)
    mediana_saldo_final = f_calcularMediana(saldos_finais)

    # 5. Estruturação dos dados e exportação para CSV
    cabecalhos = ["ID_Jogador", "Saldo_Final", "Rodadas_Jogadas", "Esgotou", "Categoria"]
    linhas_tabela: List[List[Any]] = []

    for p in participantes:
        linhas_tabela.append([
            p["id_jogador"],
            f"{p['saldo_final']:.2f}",
            p["rodadas_jogadas"],
            "Sim" if p["esgotou"] else "Não",
            p["categoria"],
        ])

    # Linhas de resumo estatístico ao final do arquivo CSV
    linhas_tabela.append(["---", "---", "---", "---", "---"])
    linhas_tabela.append(["RESUMO", f"Proporção Ganho (>100): {prop_ganho_pct:.1f}% ({n_ganho}/{numJogadores})", "-", "-", "-"])
    linhas_tabela.append(["RESUMO", f"Proporção Empate (=100): {prop_empate_pct:.1f}% ({n_empate}/{numJogadores})", "-", "-", "-"])
    linhas_tabela.append(["RESUMO", f"Proporção Perda (<100): {prop_perda_pct:.1f}% ({n_perda}/{numJogadores})", "-", "-", "-"])
    linhas_tabela.append(["RESUMO", f"Taxa de Esgotamento: {taxa_esgotamento_pct:.1f}% ({n_esgotados}/{numJogadores})", "-", "-", "-"])
    linhas_tabela.append(["RESUMO", f"Média dos Saldos Finais: {media_saldo_final:.2f} créditos", "-", "-", "-"])
    linhas_tabela.append(["RESUMO", f"Mediana dos Saldos Finais: {mediana_saldo_final:.2f} créditos", "-", "-", "-"])

    caminho_csv = DIRETORIO_TABELAS / "exp3_participantes.csv"
    f_exportarParaCsv(caminho_csv, cabecalhos, linhas_tabela)

    # 6. Geração do gráfico de trajetórias dos 5 primeiros participantes
    trajetorias_cinco = [p["trajetoria_saldos"] for p in participantes[:5]]
    caminho_figura = DIRETORIO_FIGURAS / "exp3_trajetorias.png"
    f_plotarTrajetoriasSaldosExp3(trajetorias_cinco, SALDO_INICIAL_EXP3, caminho_figura)

    # 7. Tabela resumo compacta para exibição
    cabecalhos_resumo = ["Métrica", "Valor Observado", "Observação Conceitual"]
    tabela_resumo_compacta = [
        ["Ganho (Bf > 100)", f"{prop_ganho_pct:.1f}% ({n_ganho} jogadores)", "Vitória aparente por horizonte curto"],
        ["Empate (Bf = 100)", f"{prop_empate_pct:.1f}% ({n_empate} jogadores)", "Retorno ao saldo de partida"],
        ["Perda (Bf < 100)", f"{prop_perda_pct:.1f}% ({n_perda} jogadores)", "Maioria consistente com E[X] < 0"],
        ["Soma das Proporções", f"{prop_ganho_pct + prop_empate_pct + prop_perda_pct:.1f}%", "Conferência estrita (100%)"],
        ["Taxa de Esgotamento (Ruína)", f"{taxa_esgotamento_pct:.1f}% ({n_esgotados} jogadores)", "Subconjunto das perdas com saldo < 1"],
        ["Média dos Saldos Finais", f"{media_saldo_final:.2f} créditos", "Inflacionada por jackpots pontuais"],
        ["Mediana dos Saldos Finais", f"{mediana_saldo_final:.2f} créditos", "Demonstra assimetria real à direita"],
    ]

    return {
        "num_jogadores": numJogadores,
        "n_ganho": n_ganho,
        "n_empate": n_empate,
        "n_perda": n_perda,
        "prop_ganho_pct": prop_ganho_pct,
        "prop_empate_pct": prop_empate_pct,
        "prop_perda_pct": prop_perda_pct,
        "n_esgotados": n_esgotados,
        "taxa_esgotamento_pct": taxa_esgotamento_pct,
        "media_saldo_final": media_saldo_final,
        "mediana_saldo_final": mediana_saldo_final,
        "participantes": participantes,
        "tabela_resumo": tabela_resumo_compacta,
        "cabecalhos_resumo": cabecalhos_resumo,
        "caminho_csv": caminho_csv,
        "caminho_figura": caminho_figura,
    }
