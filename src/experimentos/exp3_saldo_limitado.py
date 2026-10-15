r"""Experimento 3: O que acontece com um saldo limitado?

Conceitos em ação (Seção 7 e 8 do edital):
- Distribuição empírica de resultados com parada prematura (tempo de parada e ruína do jogador).
- Comparação entre média e mediana em distribuições de lucros com assimetria positiva.
- Horizonte de observação e variabilidade entre sessões de apostadores.
- Desmistificação de relatos isolados de sucesso (viés do sobrevivente nas redes sociais).
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
)
from src.analise.graficos import (
    f_plotarTrajetoriasSaldosExp3,
)


def f_simularSessaoJogador(gerador: Any, saldoInicial: float = SALDO_INICIAL_EXP3, maxRodadas: int = MAX_RODADAS_EXP3) -> Dict[str, Any]:
    r"""Simula a sessão individual de um apostador até o tempo de parada (500 rodadas ou ruína B < 1).

    Args:
        gerador (Any): Instância do gerador pseudoaleatório compartilhada entre participantes.
        saldoInicial (float): Saldo de partida em créditos (padrão do edital: 100.0).
        maxRodadas (int): Limite máximo de rodadas na sessão (padrão do edital: 500).

    Returns:
        Dict[str, Any]: Dicionário contendo histórico de saldos, saldo final, rodadas jogadas e indicador de ruína.
    """
    saldo = float(saldoInicial)  # O camarada entra no cassino com 100 contos no bolso
    trajetoria: List[float] = [saldo]  # Histórico da montanha-russa do bolso do cidadão
    rodadas_jogadas = 0  # Contador de giros

    # O cara só joga se ainda tiver dinheiro (>= 1) e não tiver estourado o tempo limite (500 giros)
    while rodadas_jogadas < maxRodadas and saldo >= 1.0:
        tabuleiro = f_sortearTabuleiro3x3(gerador)  # Bota a máquina pra rodar
        linha_central = f_extrairLinhaCentral(tabuleiro)  # Olha o que caiu na linha do meio

        premio_P = f_calcularPremioBruto(linha_central, TABELA_BASE)  # Vê se bateu alguma trinca
        lucro_X = f_calcularLucroLiquido(premio_P, CUSTO_APOSTA)  # Desconta 1 crédito de entrada

        saldo += lucro_X  # Atualiza o caixa: ou subiu com um prêmio ou tomou -1 no lombo
        rodadas_jogadas += 1  # Mais uma rodada pra conta do caboclo
        trajetoria.append(saldo)  # Registra o novo saldo na fita

    esgotou = (saldo < 1.0)  # Quebrou a banca? Se sobrou menos de 1 crédito, já era: tá liso!

    return {
        "saldo_final": saldo,              # Com quanto saiu (muitas vezes zerado)
        "rodadas_jogadas": rodadas_jogadas,  # Quanto tempo conseguiu sobreviver na máquina
        "esgotou": esgotou,                # Flag de ruína: bateu na lona?
        "trajetoria_saldos": trajetoria,   # O filme completo da sessão
    }


def f_executarExperimento3(semente: int = SEMENTE_EXP3, numJogadores: int = NUMERO_JOGADORES_EXP3) -> Dict[str, Any]:
    r"""Executa a simulação completa do Experimento 3 para os 100 participantes virtuais.

    Coloca 100 jogadores em fila na mesma máquina com a semente 42 contínua,
    medindo quem sai no lucro, quem empata e quem quebra a cara.

    Args:
        semente (int): Semente do gerador pseudoaleatório (padrão do edital: 42).
        numJogadores (int): Total de participantes virtuais (padrão: 100).

    Returns:
        Dict[str, Any]: Dicionário contendo todas as métricas calculadas e trajetórias.
    """
    # 1. Inicializar o gerador pseudoaleatório uma única vez e continuar entre participantes
    gerador = random.Random(semente)  # Semente 42 ligada: a mesma máquina atendendo os 100 jogadores em fila!

    participantes: List[Dict[str, Any]] = []

    # 2. Simular as sessões sequenciais dos 100 jogadores virtuais
    for id_jogador in range(1, numJogadores + 1):  # Próximo da fila, por favor!
        sessao = f_simularSessaoJogador(gerador, SALDO_INICIAL_EXP3, MAX_RODADAS_EXP3)  # O jogador joga até 500 giros ou quebrar
        saldo_f = sessao["saldo_final"]  # Saldo que restou no bolso

        if saldo_f > SALDO_INICIAL_EXP3:  # Se terminou com mais de 100
            categoria = "Ganho"  # Esse é o sortudo que vai postar print no Instagram
        elif saldo_f == SALDO_INICIAL_EXP3:  # Terminou exatamente com 100
            categoria = "Empate"  # Não ganhou nem perdeu, ficou no zero a zero
        else:  # Terminou com menos de 100
            categoria = "Perda"  # A dura realidade da maioria dos mortais

        participantes.append({
            "id_jogador": id_jogador,
            "saldo_final": saldo_f,
            "rodadas_jogadas": sessao["rodadas_jogadas"],
            "esgotou": sessao["esgotou"],
            "categoria": categoria,
            "trajetoria_saldos": sessao["trajetoria_saldos"],
        })

    # 3. Contagem e cálculo das proporções (somando exatamente 100%)
    n_ganho = sum(1 for p in participantes if p["categoria"] == "Ganho")    # Quantos ganharam
    n_empate = sum(1 for p in participantes if p["categoria"] == "Empate")  # Quantos empataram
    n_perda = sum(1 for p in participantes if p["categoria"] == "Perda")    # Quantos perderam
    assert (n_ganho + n_empate + n_perda) == numJogadores, "Erro: categorias de saldo não somam 100!"  # Confere a soma

    prop_ganho_pct = (n_ganho / numJogadores) * 100.0   # Porcentagem de reis do cassino
    prop_empate_pct = (n_empate / numJogadores) * 100.0  # Porcentagem de neutros
    prop_perda_pct = (n_perda / numJogadores) * 100.0   # Porcentagem de derrotados (~75%)

    # Taxa de esgotamento (ruína do jogador, subconjunto das perdas)
    n_esgotados = sum(1 for p in participantes if p["esgotou"])  # Quantos perderam até o último tostão
    taxa_esgotamento_pct = (n_esgotados / numJogadores) * 100.0  # Taxa de ruína total (~67%) SIXSEVEN???? perdão.

    # 4. Cálculo de medidas de centro (média vs mediana)
    saldos_finais = [p["saldo_final"] for p in participantes]
    media_saldo_final = f_calcularMediaAmostral(saldos_finais)  # Média (~52.1): ilusão puxada pelos jackpots dos ganhadores
    mediana_saldo_final = f_calcularMediana(saldos_finais)      # Mediana (0.0): a realidade nua e crua, mais da metade sai liso!

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
    f_exportarParaCsv(caminho_csv, cabecalhos, linhas_tabela)  # Grava o extrato de todos os 100 apostadores

    # 6. Geração do gráfico de trajetórias dos 5 primeiros participantes
    trajetorias_cinco = [p["trajetoria_saldos"] for p in participantes[:5]]  # Pega os 5 primeiros da fila sem escolher
    caminho_figura = DIRETORIO_FIGURAS / "exp3_trajetorias.png"
    f_plotarTrajetoriasSaldosExp3(trajetorias_cinco, SALDO_INICIAL_EXP3, caminho_figura)  # Desenha as curvas com patamar plano se quebrar

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
