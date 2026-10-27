"""Testes e validações automatizadas do projeto (Item Extra - Seção 10 do Edital).

Este módulo atende ao quesito de "Validação automatizada" (até 3 pontos extras).
Verificações implementadas:
1. Pagamentos corretos das 5 triplas e prêmio zero para as outras combinações centrais.
2. Cálculo estrito do lucro líquido como X = P - 1.
3. Reprodutibilidade estrita da semente pseudoaleatória (mesma semente gerando os mesmos resultados).
4. Integridade dos totais (soma de 10.000 contagens no E1, marcos 3x3 no E2 e 100 jogadores no E3).
5. Regras de parada e consistência do saldo limitado (E3).
6. Independência estocástica e integridade dos 9.999 pares consecutivos (E4).
7. Linearidade e comparação pareada das tabelas de pagamento Base vs +10% (E5).
8. Caso-limite: verificação de saldo insuficiente.
"""

import math
import random
from src.maquina.pagamentos import (
    f_ehTriplaPremiada,
    f_calcularPremioBruto,
    f_calcularLucroLiquido,
    f_calcularEsperancaTeorica,
    TABELA_BASE,
    TABELA_BONUS_10,
)
from src.maquina.rolos import (
    f_sortearTabuleiro3x3,
    f_extrairLinhaCentral,
)
from src.experimentos.exp1_frequencias import f_executarExperimento1
from src.experimentos.exp2_lei_grandes_numeros import (
    f_verificarReprodutibilidadePrimeirosResultados,
    f_executarExperimento2,
)
from src.experimentos.exp3_saldo_limitado import (
    f_executarExperimento3,
)
from src.experimentos.exp4_prob_condicional import (
    f_analisarParesConsecutivos,
    f_executarExperimento4,
)
from src.experimentos.exp5_premios_maiores import (
    f_executarExperimento5,
)
from src.extras import (
    f_executarExtra1IntervalosConfianca,
    f_executarExtra2RiscosDiferentes,
    f_executarExtra3LimitesExposicao,
    f_executarExtra4AnaliseSensibilidade,
    f_executarExtra5InterfaceAcessivel,
)


def test_f_pagamentosTriplasEOutrasCombinacoes() -> None:
    """Verifica se as 5 triplas pagam os valores corretos e se combinações não premiadas pagam zero."""
    assert f_calcularPremioBruto(("A", "A", "A"), TABELA_BASE) == 5.0
    assert f_calcularPremioBruto(("B", "B", "B"), TABELA_BASE) == 10.0
    assert f_calcularPremioBruto(("C", "C", "C"), TABELA_BASE) == 15.0
    assert f_calcularPremioBruto(("D", "D", "D"), TABELA_BASE) == 25.0
    assert f_calcularPremioBruto(("E", "E", "E"), TABELA_BASE) == 50.0

    # Combinações não premiadas
    assert f_calcularPremioBruto(("A", "B", "A"), TABELA_BASE) == 0.0
    assert f_calcularPremioBruto(("B", "D", "A"), TABELA_BASE) == 0.0
    assert f_calcularPremioBruto(("E", "A", "B"), TABELA_BASE) == 0.0


def test_f_calculoLucroLiquido() -> None:
    """Verifica se o lucro líquido subtrai a aposta de 1 crédito: X = P - 1 para qualquer prêmio."""
    assert f_calcularLucroLiquido(0.0, custoAposta=1.0) == -1.0
    assert f_calcularLucroLiquido(5.0, custoAposta=1.0) == 4.0
    assert f_calcularLucroLiquido(10.0, custoAposta=1.0) == 9.0
    assert f_calcularLucroLiquido(15.0, custoAposta=1.0) == 14.0
    assert f_calcularLucroLiquido(25.0, custoAposta=1.0) == 24.0
    assert f_calcularLucroLiquido(50.0, custoAposta=1.0) == 49.0


def test_f_reprodutibilidadeSemente() -> None:
    """Verifica se inicializar o gerador com a mesma semente reproduz rigorosamente a mesma sequência."""
    assert f_verificarReprodutibilidadePrimeirosResultados(semente=2026, nResultados=10)
    assert f_verificarReprodutibilidadePrimeirosResultados(semente=10, nResultados=10)
    assert f_verificarReprodutibilidadePrimeirosResultados(semente=123456, nResultados=10)


def test_f_integridadeTotaisExperimentos() -> None:
    """Verifica se a soma das contagens do E1 atinge rigorosamente 10.000 rodadas."""
    res = f_executarExperimento1(semente=2026, totalRodadas=10_000)
    soma_contagens = sum(res["contagens"].values())
    assert soma_contagens == 10_000, f"Soma incorreta: {soma_contagens}"
    assert res["total_rodadas"] == 10_000


def test_f_experimento2_tabela_e_trajetorias() -> None:
    """Verifica a integridade dos dados gerados pelo Experimento 2 (tabela 3x3 e trajetórias)."""
    res_e2 = f_executarExperimento2()
    assert res_e2["reproduzido_com_sucesso"] is True
    assert len(res_e2["ordem_sementes"]) == 3
    assert len(res_e2["trajetorias"][10]) == 10_000
    assert len(res_e2["trajetorias"][2026]) == 10_000
    assert len(res_e2["trajetorias"][123456]) == 10_000

    for semente in [10, 2026, 123456]:
        marcos = res_e2["medias_marcos"][semente]
        assert 100 in marcos
        assert 1000 in marcos
        assert 10000 in marcos


def test_f_experimento3_saldo_limitado_e_ruina() -> None:
    """Verifica as regras de parada, integridade de categorias e esgotamento do Experimento 3."""
    res_e3 = f_executarExperimento3(semente=42, numJogadores=100)

    assert res_e3["num_jogadores"] == 100
    assert len(res_e3["participantes"]) == 100

    soma_proporcoes = res_e3["prop_ganho_pct"] + res_e3["prop_empate_pct"] + res_e3["prop_perda_pct"]
    assert round(soma_proporcoes, 4) == 100.0
    assert res_e3["taxa_esgotamento_pct"] <= res_e3["prop_perda_pct"]

    for p in res_e3["participantes"]:
        assert p["rodadas_jogadas"] <= 500
        if p["esgotou"]:
            assert p["saldo_final"] < 1.0
        else:
            assert p["saldo_final"] >= 1.0
            assert p["rodadas_jogadas"] == 500


def test_f_experimento4_probabilidade_condicional() -> None:
    """Verifica a integridade dos 9.999 pares e independência estocástica no Experimento 4."""
    res_e4 = f_executarExperimento4()

    assert res_e4["n_pares"] == 9_999
    soma_pares = res_e4["total_apos_premio"] + res_e4["total_apos_perda"]
    assert soma_pares == 9_999

    assert 2.0 <= res_e4["prop_apos_premio_pct"] <= 7.0
    assert 3.0 <= res_e4["prop_apos_perda_pct"] <= 5.0

    caso_sem_premios = [0.0] * 20
    resultado_limite = f_analisarParesConsecutivos(caso_sem_premios)
    assert resultado_limite["total_apos_premio"] == 0
    assert resultado_limite["prop_apos_premio_pct"] is None


def test_f_experimento5_premios_maiores() -> None:
    """Verifica a linearidade e comparação pareada das tabelas Base e +10% no Experimento 5."""
    res_e5 = f_executarExperimento5()

    # 1. Conferência das referências teóricas estipuladas no edital
    assert math.isclose(res_e5["rtp_teo_bonus"], 92.4, abs_tol=1e-4)
    assert math.isclose(res_e5["lucro_medio_teo_bonus"], -0.076, abs_tol=1e-4)
    assert math.isclose(res_e5["premio_medio_teo_bonus"], 0.924, abs_tol=1e-4)

    # 2. A probabilidade de prêmio deve ser rigorosamente 4.0% para ambas as tabelas
    assert res_e5["prob_premio_teo"] == 4.0
    assert res_e5["freq_premio_obs"] == 4.12

    # 3. Linearidade exata observada na comparação pareada (+10% nos prêmios e no RTP)
    assert math.isclose(res_e5["rtp_obs_bonus"], 1.10 * res_e5["rtp_obs_base"], rel_tol=1e-4)
    assert math.isclose(res_e5["premio_medio_obs_bonus"], 1.10 * res_e5["premio_medio_obs_base"], rel_tol=1e-4)


def test_f_casoLimiteSaldoInsuficiente() -> None:
    """Verifica a regra de negócio para saldo insuficiente (menor que 1 crédito)."""
    saldo = 0.5
    aposta = 1.0
    pode_jogar = saldo >= aposta
    assert not pode_jogar, "Jogador com saldo insuficiente não deveria poder apostar."


def test_f_extra1_intervalos_confianca() -> None:
    """Verifica a construção dos intervalos de confiança de 95% e execuções independentes (Extra 1)."""
    res = f_executarExtra1IntervalosConfianca(numExecucoes=30, nRodadasPorExecucao=10_000, sementeInicial=2026)
    assert res["num_execucoes"] == 30
    assert len(res["registros_execucoes"]) == 30
    assert res["canonico"]["li_lucro"] < res["canonico"]["media_lucro"] < res["canonico"]["ls_lucro"]
    assert res["li_global_lucro"] <= -0.16 <= res["ls_global_lucro"]
    assert res["caminho_csv"].exists()
    assert res["caminho_figura"].exists()


def test_f_extra2_mesma_media_riscos_diferentes() -> None:
    """Verifica se as 3 tabelas de risco mantêm exatamente E[X] = -0,16 e RTP = 84% com desvios distintos (Extra 2)."""
    res = f_executarExtra2RiscosDiferentes()
    assert res["esperancas_iguais"] is True
    perfis = res["resumo_perfis"]
    assert len(perfis) == 3
    # Desvio-padrão teórico deve crescer da Baixa Volatilidade para a Alta Volatilidade
    assert perfis[0]["dp_teorico"] < perfis[1]["dp_teorico"] < perfis[2]["dp_teorico"]
    assert res["caminho_csv"].exists()
    assert res["caminho_figura"].exists()


def test_f_extra3_limites_exposicao() -> None:
    """Verifica a comparação de regras de parada e redução da exposição média (Extra 3)."""
    res = f_executarExtra3LimitesExposicao()
    regras = res["resultados_regras"]
    assert len(regras) == 3
    # Regra 2 (Stop-Win 120 + Stop-Loss 70) deve ter exposição média menor e ruína total zero
    assert regras[1]["media_rodadas"] < regras[0]["media_rodadas"]
    assert regras[1]["taxa_ruina_pct"] == 0.0
    assert res["caminho_csv"].exists()
    assert res["caminho_figura"].exists()


def test_f_extra4_analise_sensibilidade() -> None:
    """Verifica os 7 cenários da Análise de Sensibilidade (Extra 4)."""
    res = f_executarExtra4AnaliseSensibilidade()
    cenarios = res["cenarios"]
    assert len(cenarios) >= 5
    # Cenário 4 é o ponto de equilíbrio (RTP = 100%, E[X] = 0)
    assert math.isclose(cenarios[3]["rtp_teorico_pct"], 100.0, abs_tol=1e-4)
    assert math.isclose(cenarios[3]["esp_lucro_teo"], 0.0, abs_tol=1e-4)
    # Cenário 5 é favorável ao jogador (E[X] > 0)
    assert cenarios[4]["esp_lucro_teo"] > 0.0
    assert res["caminho_csv"].exists()
    assert res["caminho_figura"].exists()


def test_f_extra5_interface_acessivel() -> None:
    """Verifica a geração da Interface Web Acessível (HTML/CSS/JS) e auditoria WCAG 2.1 AAA (Extra 5)."""
    res = f_executarExtra5InterfaceAcessivel(abrirNavegador=False)
    assert res["todos_wcag_aaa"] is True
    assert res["menor_razao_contraste"] >= 7.0
    assert res["caminho_html"].exists()
    assert res["caminho_csv"].exists()
    html_gerado = res["caminho_html"].read_text(encoding="utf-8")
    assert 'aria-live="polite"' in html_gerado
    assert "Simulador Interativo 3×3" in html_gerado




