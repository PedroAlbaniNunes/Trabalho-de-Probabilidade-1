"""Ponto de entrada principal da aplicação (Interface de Linha de Comando - CLI).

Permite interagir com a máquina caça-níqueis didática, visualizar uma rodada única
e disparar os cinco experimentos acadêmicos descritos no edital.
"""

import sys
import random
from src.configuracao import (
    AVISO_LEGAL,
    SEMENTE_EXP1,
    RODADAS_EXP1,
    SEMENTE_EXP3,
    NUMERO_JOGADORES_EXP3,
)
from src.maquina.rolos import (
    f_sortearTabuleiro3x3,
    f_extrairLinhaCentral,
    f_formatarTabuleiroParaExibicao,
)
from src.maquina.pagamentos import (
    f_ehTriplaPremiada,
    f_calcularPremioBruto,
    f_calcularLucroLiquido,
    TABELA_BASE,
)
from src.analise.exportador import f_gerarTabelaFormatada
from src.experimentos.exp1_frequencias import f_executarExperimento1
from src.experimentos.exp2_lei_grandes_numeros import f_executarExperimento2
from src.experimentos.exp3_saldo_limitado import f_executarExperimento3
from src.experimentos.exp4_prob_condicional import f_executarExperimento4
from src.experimentos.exp5_premios_maiores import f_executarExperimento5
from src.extras import (
    f_executarExtra1IntervalosConfianca,
    f_executarExtra2RiscosDiferentes,
    f_executarExtra3LimitesExposicao,
    f_executarExtra4AnaliseSensibilidade,
    f_executarExtra5InterfaceAcessivel,
)


def f_exibirCabecalho() -> None:
    """Exibe no terminal o cabeçalho do projeto e o aviso acadêmico obrigatório.

    Apresenta a identificação institucional da disciplina e o aviso legal
    determinado pelo edital: 'Simulador acadêmico - somente créditos fictícios'.
    """
    largura = 78
    print("\n" + "=" * largura)
    print("IFES - CAMPUS SERRA | PROBABILIDADE E ESTATÍSTICA I".center(largura))
    print("MÁQUINA ESTATÍSTICA: Probabilidade, Apostas e Pensamento Crítico".center(largura))
    print("-" * largura)
    print(f"[AVISO OBRIGATÓRIO]: {AVISO_LEGAL}".center(largura))
    print("=" * largura)


def f_executarRodadaDemonstrativa() -> None:
    """Realiza uma rodada única para demonstração das regras fundamentais.

    Sorteia a grade 3x3 com gerador aleatório padrão, extrai a linha central,
    avalia se houve tripla premiada e exibe o prêmio e o lucro líquido obtidos.
    """
    print("\n--- [ RODADA DEMONSTRATIVA ] ---")
    gerador = random.Random()  # inicializa o gerador aleatório pro giro avulso
    tabuleiro = f_sortearTabuleiro3x3(gerador)  # sorteia os 9 símbolos e monta a matriz 3x3
    linha_central = f_extrairLinhaCentral(tabuleiro)  # fisga a linha do meio (a única linha de pagamento que importa)

    print(f_formatarTabuleiroParaExibicao(tabuleiro))

    premiada = f_ehTriplaPremiada(linha_central)  # confere se os 3 símbolos são iguaizinhos (A-A-A, B-B-B...)
    premio = f_calcularPremioBruto(linha_central, TABELA_BASE)  # busca o prêmio na tabela se deu bom, ou zero se bateu na trave
    lucro = f_calcularLucroLiquido(premio, 1.0)  # desconta a aposta de 1 crédito: mostra se o saldo subiu ou tomou fumo

    print(f"\nLinha Central Avaliada: ({linha_central[0]} - {linha_central[1]} - {linha_central[2]})")
    if premiada:
        print(f">> Parabéns! Tripla premiada! Prêmio (P): {premio:.2f} créditos | Lucro (X): {lucro:+.2f} créditos")
    else:
        print(f">> Sem prêmio nesta rodada. Prêmio (P): {premio:.2f} créditos | Lucro (X): {lucro:+.2f} créditos")
    print("-" * 50)


def f_menuPontosExtras() -> None:
    """Submenu dedicado à execução dos experimentos de Pontos Extras (Seção 10 do Edital)."""
    largura = 78
    while True:
        print("\n" + "=" * largura)
        print("SUBMENU — EXPERIMENTOS DE PONTOS EXTRAS (SEÇÃO 10 DO EDITAL)".center(largura))
        print("=" * largura)

        print("\n  >> EXPERIMENTOS INDIVIDUAIS (SEÇÃO 10):")
        print("     [1] Extra 1 — Intervalos de Confiança (30 Execuções Independentes | até 4 pts)")
        print("     [2] Extra 2 — Mesma Média, Riscos Diferentes (3 Tabelas RTP 84%   | até 4 pts)")
        print("     [3] Extra 3 — Limites de Exposição e Parada (Stop-Win / Stop-Loss | até 3 pts)")
        print("     [4] Extra 4 — Análise de Sensibilidade (7 Cenários Paramétricos   | até 3 pts)")
        print("     [5] Extra 5 — Interface Web Acessível (Abre Automaticamente no Navegador | até 3 pts)")

        print("\n  >> EXECUÇÃO EM LOTE:")
        print("     [6] Executar TODOS os 5 Experimentos Extras em lote (Gera CSVs, PNGs e HTML)")

        print("\n  >> NAVEGAÇÃO:")
        print("     [0] Voltar ao Menu Principal")
        print("-" * largura)

        op = input("  Selecione uma opção [0-6]: ").strip()

        if op == "1":
            print("\nExecutando Extra 1: Intervalos de Confiança (30 execuções de 10.000 giros)... Aguarde...")
            res1 = f_executarExtra1IntervalosConfianca()
            print("\n" + f_gerarTabelaFormatada(res1["cabecalhos_resumo"], res1["tabela_resumo"]))
            print("\n--- INTERPRETAÇÃO (EXTRA 1 - INTERVALOS DE CONFIANÇA) ---")
            print("Método: IC 95% via distribuição t-Student (gl=9.999 por amostra; gl=29 entre as 30 médias).")
            print(f"Taxa de cobertura observada: {res1['qtd_cobriu']}/{res1['num_execucoes']} ({res1['taxa_cobertura_pct']:.1f}%) dos ICs contiveram E[X] = -0,16.")
            print(f"CSV salvo em:    {res1['caminho_csv']}")
            print(f"Figura salva em: {res1['caminho_figura']}")
            input("\nPressione ENTER para continuar...")

        elif op == "2":
            print("\nExecutando Extra 2: Mesma Média, Riscos Diferentes (RTP = 84%, E[X] = -0,16)... Aguarde...")
            res2 = f_executarExtra2RiscosDiferentes()
            print("\n" + f_gerarTabelaFormatada(res2["cabecalhos"], res2["linhas_tabela"]))
            print("\n--- INTERPRETAÇÃO (EXTRA 2 - MESMA MÉDIA, RISCOS DIFERENTES) ---")
            print(f"Igualdade analítica das esperanças conferida (E[X] = -0,16 e RTP = 84%): {res2['esperancas_iguais']}")
            print("A tabela de Baixa Volatilidade reduz os extremos, mas acelera a drenagem previsível;")
            print("a tabela de Alta Volatilidade gera raros jackpots altos (maior saldo máximo), mas eleva a dispersão.")
            print(f"CSV salvo em:    {res2['caminho_csv']}")
            print(f"Figura salva em: {res2['caminho_figura']}")
            input("\nPressione ENTER para continuar...")

        elif op == "3":
            print("\nExecutando Extra 3: Limites de Exposição e Regras de Parada... Aguarde...")
            res3 = f_executarExtra3LimitesExposicao()
            print("\n" + f_gerarTabelaFormatada(res3["cabecalhos"], res3["linhas_tabela"]))
            print("\n--- INTERPRETAÇÃO (EXTRA 3 - LIMITES DE EXPOSIÇÃO) ---")
            print("Pela Identidade de Wald (E[Bf - B0] = E[X] * E[T]), regras de Stop-Win/Stop-Loss não alteram")
            print("a esperança negativa por rodada (E[X] = -0,16), mas reduzem a exposição média (T̄),")
            print("preservando o saldo contra a ruína total.")
            print(f"CSV salvo em:    {res3['caminho_csv']}")
            print(f"Figura salva em: {res3['caminho_figura']}")
            input("\nPressione ENTER para continuar...")

        elif op == "4":
            print("\nExecutando Extra 4: Análise de Sensibilidade (7 Cenários)... Aguarde...")
            res4 = f_executarExtra4AnaliseSensibilidade()
            print("\n" + f_gerarTabelaFormatada(res4["cabecalhos"], res4["linhas_tabela"]))
            print("\n--- INTERPRETAÇÃO (EXTRA 4 - ANÁLISE DE SENSIBILIDADE) ---")
            print("O jogo só atinge equilíbrio (E[X] = 0, RTP = 100%) quando os prêmios sobem +19,05% (C4),")
            print("e torna-se favorável ao jogador em +25% (C5). Já alterar a estrutura dos rolos (C6 e C7)")
            print("demonstra que elevar a frequência de acertos baratos (C7: 5,56%) pode até reduzir o RTP (64,81%).")
            print(f"CSV salvo em:    {res4['caminho_csv']}")
            print(f"Figura salva em: {res4['caminho_figura']}")
            input("\nPressione ENTER para continuar...")

        elif op == "5":
            print("\nGerando e abrindo Extra 5: Interface Web Acessível no navegador padrão...")
            res5 = f_executarExtra5InterfaceAcessivel(abrirNavegador=True)
            print("\n" + f_gerarTabelaFormatada(res5["cabecalhos_resumo"], res5["tabela_resumo"]))
            print("\n--- RESUMO (EXTRA 5 - INTERFACE WEB ACESSÍVEL) ---")
            print(f"Aplicação Web HTML gerada em: {res5['caminho_html']}")
            print(f"Laudo CSV salvo em:           {res5['caminho_csv']}")
            print(">> A página foi aberta automaticamente no seu navegador padrão (navegação por Mouse e Teclado)!")
            input("\nPressione ENTER para continuar...")

        elif op == "6":
            print("\n======================================================================")
            print("  EXECUTANDO BATERIA COMPLETA DE PONTOS EXTRAS (EXTRAS 1 A 5)  ")
            print("======================================================================")
            print("1/5: Executando Extra 1 (Intervalos de Confiança)...")
            res1 = f_executarExtra1IntervalosConfianca()
            print("\n" + f_gerarTabelaFormatada(res1["cabecalhos_resumo"], res1["tabela_resumo"]))

            print("\n2/5: Executando Extra 2 (Mesma Média, Riscos Diferentes)...")
            res2 = f_executarExtra2RiscosDiferentes()
            print("\n" + f_gerarTabelaFormatada(res2["cabecalhos"], res2["linhas_tabela"]))

            print("\n3/5: Executando Extra 3 (Limites de Exposição e Regras de Parada)...")
            res3 = f_executarExtra3LimitesExposicao()
            print("\n" + f_gerarTabelaFormatada(res3["cabecalhos"], res3["linhas_tabela"]))

            print("\n4/5: Executando Extra 4 (Análise de Sensibilidade em 7 Cenários)...")
            res4 = f_executarExtra4AnaliseSensibilidade()
            print("\n" + f_gerarTabelaFormatada(res4["cabecalhos"], res4["linhas_tabela"]))

            print("\n5/5: Executando Extra 5 (Interface Web Acessível — Abrindo no Navegador)...")
            res5 = f_executarExtra5InterfaceAcessivel(abrirNavegador=True)
            print("\n" + f_gerarTabelaFormatada(res5["cabecalhos_resumo"], res5["tabela_resumo"]))

            print("\n>> Sucesso! Todos os 5 experimentos de pontos extras foram exportados para:")
            print("   - Aplicação Web: resultados/interface_acessivel.html")
            print("   - Tabelas CSV:   resultados/tabelas/extras/")
            print("   - Gráficos PNG:  resultados/figuras/extras/")
            print("======================================================================")
            input("\nPressione ENTER para voltar ao menu de pontos extras...")

        elif op == "0":
            break
        else:
            print("\nOpção inválida! Tente novamente.")


def f_menuPrincipal() -> None:
    """Apresenta o menu textual interativo com as opções disponíveis no terminal.

    Gerencia o loop de execução da CLI, permitindo ao usuário acionar individualmente
    cada experimento, rodar demonstrações avulsas ou disparar a bateria completa.
    """
    dados_exp1 = None  # guarda os dados do E1 pra reaproveitar nos experimentos pareados (E2, E4, E5)
    largura = 78

    while True:
        f_exibirCabecalho()

        print("\n  >> DEMONSTRAÇÃO DA MÁQUINA:")
        print("     [1] Rodada Demonstrativa Isolada       (Sorteio da grade 3x3 e linha central)")

        print("\n  >> EXPERIMENTOS OBRIGATÓRIOS (SEÇÃO 7 DO EDITAL):")
        print("     [2] Experimento 1 — Frequências vs. Probabilidades     (10.000 giros | Seed 2026)")
        print("     [3] Experimento 2 — Lei dos Grandes Números            (3 Sementes   | Monte Carlo)")
        print("     [4] Experimento 3 — Saldo Limitado e Risco de Ruína    (100 Jogadores| Seed 42)")
        print("     [5] Experimento 4 — Probabilidade Condicional          (9.999 Pares  | Falácia)")
        print("     [6] Experimento 5 — Prêmios Maiores (+10%)             (Comparação Pareada)")

        print("\n  >> EXECUÇÃO EM LOTE E PONTOS EXTRAS (SEÇÃO 10 DO EDITAL):")
        print("     [7] Executar Bateria Completa (Exp. 1 a 5)             (Exporta CSVs e Figuras PNG)")
        print("     [8] Submenu de Pontos Extras (Extras 1 a 5)            (IC, Riscos, Parada, WCAG...)")

        print("\n  >> SISTEMA:")
        print("     [0] Encerrar o Simulador")
        print("-" * largura)

        escolha = input("  Selecione uma opção [0-8]: ").strip()  # lê o comando do usuário limpinho sem espaços soltos

        if escolha == "1":
            f_executarRodadaDemonstrativa()  # roda aquele giro demonstrativo maroto na tela
            input("\nPressione ENTER para voltar ao menu...")

        elif escolha == "2":
            print("\nExecutando Experimento 1 (Semente 2026, 10.000 rodadas)... Aguarde...")
            dados_exp1 = f_executarExperimento1(semente=SEMENTE_EXP1, totalRodadas=RODADAS_EXP1)  # roda os 10k giros canônicos

            cabecalhos = ["Desfecho", "Lucro X", "Prob. Teórica", "Prob. (%)", "Contagem", "Freq. Relativa (%)"]
            print("\n" + f_gerarTabelaFormatada(cabecalhos, dados_exp1["tabela_linhas"]))

            print("\n--- RESUMO ESTATÍSTICO DO EXPERIMENTO 1 ---")
            print(f"Total de rodadas:          {dados_exp1['total_rodadas']:,}")
            print(f"Semente utilizada:         {dados_exp1['semente']}")
            print(f"Lucro médio amostral (X̄): {dados_exp1['lucro_medio_amostral']:+.4f} créditos (Referência teórica: -0.1600)")
            print(f"Desvio-padrão amostral (s): {dados_exp1['desvio_padrao_amostral']:.4f} créditos (Divisor N - 1)")
            print(f"RTP observado:             {dados_exp1['rtp_observado_pct']:.2f}% (Referência teórica: 84.00%)")
            print(f"Proporção premiadas:       {dados_exp1['proporcao_premiadas_pct']:.2f}% (Referência teórica: 4.00%)")
            print(f"Arquivo CSV gravado em:    {dados_exp1['caminho_csv']}")
            print(f"Gráfico gerado em:         {dados_exp1['caminho_figura']}")
            print("-" * 50)
            input("\nPressione ENTER para voltar ao menu...")

        elif escolha == "3":
            print("\nExecutando Experimento 2 (Sementes 10, 2026 e 123456)... Aguarde...")
            dados_exp2 = f_executarExperimento2(dadosExp1=dados_exp1)  # roda as 3 sementes pra provar a convergência da média

            print("\n" + f_gerarTabelaFormatada(dados_exp2["cabecalhos_3x3"], dados_exp2["tabela_3x3_linhas"]))

            status_rep = "REPRODUZIDOS COM SUCESSO" if dados_exp2["reproduzido_com_sucesso"] else "DIVERGÊNCIA IDENTIFICADA"
            print("\n--- RESUMO DO EXPERIMENTO 2 ---")
            print(f"Auditoria da Semente 2026 (10 primeiros sorteios): {status_rep}")
            print("10 primeiros resultados da semente 2026:")
            for i, res in enumerate(dados_exp2["dez_primeiros_resultados_2026"], start=1):
                print(f"  Rodada {i:02d}: ({res[0]} - {res[1]} - {res[2]})")
            print(f"Arquivo CSV gravado em:    {dados_exp2['caminho_csv']}")
            print(f"Gráfico gerado em:         {dados_exp2['caminho_figura']}")
            print("-" * 50)
            input("\nPressione ENTER para voltar ao menu...")

        elif escolha == "4":
            print("\nExecutando Experimento 3 (100 participantes, Saldo Inicial 100, Semente 42)... Aguarde...")
            dados_exp3 = f_executarExperimento3(semente=SEMENTE_EXP3, numJogadores=NUMERO_JOGADORES_EXP3)  # simula a ruína dos 100 jogadores

            print("\n" + f_gerarTabelaFormatada(dados_exp3["cabecalhos_resumo"], dados_exp3["tabela_resumo"]))

            print("\n--- DETALHES DE ARQUIVOS GERADOS (EXPERIMENTO 3) ---")
            print(f"Total de participantes simulados: {dados_exp3['num_jogadores']}")
            print(f"Média dos saldos finais:          {dados_exp3['media_saldo_final']:.2f} créditos")
            print(f"Mediana dos saldos finais:        {dados_exp3['mediana_saldo_final']:.2f} créditos")
            print(f"Taxa de esgotamento (ruína):      {dados_exp3['taxa_esgotamento_pct']:.1f}%")
            print(f"Arquivo CSV detalhado:            {dados_exp3['caminho_csv']}")
            print(f"Gráfico das 5 trajetórias:        {dados_exp3['caminho_figura']}")
            print("-" * 50)
            input("\nPressione ENTER para voltar ao menu...")

        elif escolha == "5":
            print("\nExecutando Experimento 4 (Probabilidade Condicional e Falácia do Apostador)... Aguarde...")
            dados_exp4 = f_executarExperimento4(dadosExp1=dados_exp1)  # calcula P(G_{i+1}|G_i) e P(G_{i+1}|G_i^c) pra provar independência

            print("\n" + f_gerarTabelaFormatada(dados_exp4["cabecalhos"], dados_exp4["linhas_tabela"]))

            print("\n--- INTERPRETAÇÃO ESTATÍSTICA (EXPERIMENTO 4) ---")
            print(f"Total de pares consecutivos analisados: {dados_exp4['n_pares']:,}")
            print(f"Chance após Prêmio:  P(Gi+1 | Gi)   = {dados_exp4['prop_apos_premio_pct']:.2f}% (Ref: 4.00%)")
            print(f"Chance após Perda:   P(Gi+1 | Gi^c) = {dados_exp4['prop_apos_perda_pct']:.2f}% (Ref: 4.00%)")
            print(">> Conclusão: Perder na rodada anterior NÃO aumenta a chance de ganhar na rodada seguinte.")
            print("   A máquina não guarda memória nem 'deve' prêmios (Falácia do Apostador).")
            print(f"Arquivo CSV gravado em: {dados_exp4['caminho_csv']}")
            print("-" * 50)
            input("\nPressione ENTER para voltar ao menu...")

        elif escolha == "6":
            print("\nExecutando Experimento 5 (Comparação com Tabela Prêmios +10%)... Aguarde...")
            dados_exp5 = f_executarExperimento5(dadosExp1=dados_exp1)  # compara lado a lado a tabela normal com a tabela +10%

            print("\n" + f_gerarTabelaFormatada(dados_exp5["cabecalhos"], dados_exp5["linhas_tabela"]))

            print("\n--- INTERPRETAÇÃO ESTATÍSTICA (EXPERIMENTO 5) ---")
            print(f"RTP Teórico:       Base = {dados_exp5['rtp_teo_base']:.2f}%  -->  Prêmios +10% = {dados_exp5['rtp_teo_bonus']:.2f}%")
            print(f"RTP Observado:     Base = {dados_exp5['rtp_obs_base']:.2f}%  -->  Prêmios +10% = {dados_exp5['rtp_obs_bonus']:.2f}%")
            print(f"Lucro Médio (E[X]): Base = {dados_exp5['lucro_medio_teo_base']:+.4f}  -->  Prêmios +10% = {dados_exp5['lucro_medio_teo_bonus']:+.4f}")
            print(">> Conclusão: Aumentar os prêmios em 10% melhora o retorno (RTP de 84% para 92.4%),")
            print("   mas o jogo CONTINUA DESFAVORÁVEL (E[X] = -0.076 < 0).")
            print("   Pagar mais NÃO significa pagar com mais frequência e NÃO garante lucro ao jogador.")
            print(f"Arquivo CSV gravado em: {dados_exp5['caminho_csv']}")
            print("-" * 50)
            input("\nPressione ENTER para voltar ao menu...")

        elif escolha == "7":
            print("\n=======================================================")
            print("  EXECUTANDO BATERIA COMPLETA DE EXPERIMENTOS (1 A 5)  ")
            print("=======================================================")
            print("1/5: Executando Experimento 1...")
            dados_exp1 = f_executarExperimento1(semente=SEMENTE_EXP1, totalRodadas=RODADAS_EXP1)  # roda o primeiro experimento
            print("2/5: Executando Experimento 2...")
            f_executarExperimento2(dadosExp1=dados_exp1)  # roda o segundo aproveitando o histórico
            print("3/5: Executando Experimento 3...")
            f_executarExperimento3(semente=SEMENTE_EXP3, numJogadores=NUMERO_JOGADORES_EXP3)  # roda a simulação dos 100 jogadores
            print("4/5: Executando Experimento 4...")
            f_executarExperimento4(dadosExp1=dados_exp1)  # roda a análise de pares consecutivos
            print("5/5: Executando Experimento 5...")
            f_executarExperimento5(dadosExp1=dados_exp1)  # roda o pareamento de premiações maiores
            print("\n>> Sucesso! Todos os 5 experimentos foram gerados e exportados para:")
            print("   - Tabelas CSV: resultados/tabelas/")
            print("   - Gráficos PNG: resultados/figuras/")
            print("=======================================================")
            input("\nPressione ENTER para voltar ao menu...")

        elif escolha == "8":
            f_menuPontosExtras()

        elif escolha == "0":
            print("\nEncerrando o simulador acadêmico.")
            sys.exit(0)  # tchau e benção: encerra o programa tranquilamente
        else:
            print("\nOpção inválida! Tente novamente.")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    f_menuPrincipal()
