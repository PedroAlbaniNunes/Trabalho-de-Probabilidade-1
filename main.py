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


def f_exibirCabecalho() -> None:
    """Exibe no terminal o cabeçalho do projeto e o aviso acadêmico obrigatório.

    Apresenta a identificação institucional da disciplina e o aviso legal
    determinado pelo edital: 'Simulador acadêmico - somente créditos fictícios'.
    """
    largura = 70
    print("=" * largura)
    print("  IFES - CAMPUS SERRA | PROBABILIDADE E ESTATÍSTICA I  ".center(largura))
    print("  MÁQUINA ESTATÍSTICA: Probabilidade, Apostas e Pensamento Crítico  ".center(largura))
    print("-" * largura)
    print(f"  [AVISO]: {AVISO_LEGAL}  ".center(largura))
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


def f_menuPrincipal() -> None:
    """Apresenta o menu textual interativo com as opções disponíveis no terminal.

    Gerencia o loop de execução da CLI, permitindo ao usuário acionar individualmente
    cada experimento, rodar demonstrações avulsas ou disparar a bateria completa.
    """
    dados_exp1 = None  # guarda os dados do E1 pra reaproveitar nos experimentos pareados (E2, E4, E5)

    while True:
        f_exibirCabecalho()
        print("\nEscolha uma opção:")
        print("  1. Exibir uma rodada demonstrativa (tabuleiro 3x3 e premiação)")
        print("  2. Executar Experimento 1 (Frequências vs Probabilidades em 10.000 rodadas)")
        print("  3. Executar Experimento 2 (Lei dos Grandes Números e Monte Carlo com 3 Sementes)")
        print("  4. Executar Experimento 3 (Simulação com Saldo Limitado e Ruína - 100 Jogadores)")
        print("  5. Executar Experimento 4 (Probabilidade Condicional e Falácia do Apostador)")
        print("  6. Executar Experimento 5 (Prêmios Maiores +10% Tornam o Jogo Favorável?)")
        print("  7. Executar todos os experimentos em lote (Gera todas as tabelas e gráficos)")
        print("  0. Sair")

        escolha = input("\nDigite o número da opção desejada: ").strip()  # lê o comando do usuário limpinho sem espaços soltos

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

        elif escolha == "0":
            print("\nEncerrando o simulador acadêmico. Bons estudos!")
            sys.exit(0)  # tchau e benção: encerra o programa tranquilamente
        else:
            print("\nOpção inválida! Tente novamente.")


if __name__ == "__main__":
    f_menuPrincipal()
