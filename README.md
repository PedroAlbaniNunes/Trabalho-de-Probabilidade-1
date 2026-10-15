# Máquina Estatística: Probabilidade, Apostas e Pensamento Crítico

Projeto acadêmico desenvolvido para a disciplina de **Probabilidade e Estatística I** do curso de **Bacharelado em Sistemas de Informação** do **Instituto Federal do Espírito Santo (IFES) – Campus Serra**.

- **Docente Responsável:** Prof. Fidelis Zanetti de Castro
- **Natureza do Projeto:** Trabalho Prático de Simulação Estocástica e Pensamento Crítico
- **Aviso Obrigatório:** *Simulador acadêmico - somente créditos fictícios.*

---

## Integrantes da Equipe

- **Integrante 1:** Gustavo Saraiva Mariano
- **Integrante 2:** Lucas Mariani Gomes
- **Integrante 3:** Pedro Henrique Albani Nunes

---

## Visão Geral do Projeto

Este projeto consiste na modelagem e implementação de um simulador estocástico transparente baseado em uma máquina caça-níqueis de rolos digitais ($3 \times 3$). O objetivo principal é articular conceitos fundamentais de probabilidade e estatística com a desmistificação matemática de jogos de azar eletrônicos.

A aplicação permite confrontar as previsões teóricas (espaço amostral equiprovável, esperança matemática, retorno teórico ao jogador - RTP e probabilidade condicional) com resultados observados por meio de métodos de Monte Carlo e simulações com controle estrito de sementes pseudoaleatórias.

> **Nota:** Para a fundamentação matemática aprofundada, deduções analíticas completas, tabela de premiações e roteiro de discussão interdisciplinar, consulte o documento oficial de especificação em PDF disponibilizado pelo professor.

---

## Síntese dos Experimentos

O simulador implementa cinco experimentos acadêmicos que investigam o comportamento probabilístico do jogo sob diferentes perspectivas amostrais e financeiras:

### Experimento 1: Frequências Relativas vs. Probabilidades Teóricas
- **Objetivo:** Simular $10.000$ rodadas consecutivas (semente canônica `2026`) com aposta unitária e sem saldo limitante.
- **Aspectos Analisados:** Confronto entre as probabilidades teóricas das 5 triplas premiadas ($P = 4,00\%$) e suas frequências observadas, cálculo da média amostral de lucro ($\bar{X} \approx -0,16$), variância amostral ($s^2$ com divisor $N-1$) e verificação empírica do RTP base ($84,00\%$).

### Experimento 2: Lei dos Grandes Números e Estabilidade de Monte Carlo
- **Objetivo:** Avaliar a velocidade e estabilidade da convergência da média amostral de lucro em função do tamanho da amostra.
- **Aspectos Analisados:** Três trajetórias independentes de $10.000$ rodadas sob sementes distintas (`10`, `2026` e `123456`), com medição das médias acumuladas nos marcos amostrais $N = 100$, $N = 1.000$ e $N = 10.000$. Evidencia a convergência assintótica não monótona para a reta de esperança matemática ($E[X] = -0,16$).

### Experimento 3: Saldo Finito, Regras de Parada e Risco de Ruína
- **Objetivo:** Simular a experiência de $100$ participantes virtuais operando com restrição orçamentária individual ($B_0 = 100$ créditos) sob até $500$ rodadas.
- **Aspectos Analisados:** Classificação dos desfechos em Ganho, Empate e Perda, taxa de esgotamento total do saldo (ruína financeira) e a marcante assimetria entre a média e a mediana dos saldos finais, ilustrando como poucos ganhadores atípicos mascaram a ruína da grande maioria dos apostadores.

### Experimento 4: Probabilidade Condicional e Falácia do Apostador
- **Objetivo:** Investigar a hipótese empírica de memória estocástica ou dependência temporal entre rodadas consecutivas.
- **Aspectos Analisados:** Avaliação de $9.999$ pares de transições sucessivas a partir da realização amostral do Experimento 1, comparando a probabilidade condicional de vitória após rodada premiada $P(G_{i+1} \mid G_i)$ com a probabilidade condicional após perda $P(G_{i+1} \mid G_i^c)$. Os resultados confirmam a independência estocástica das rodadas e refutam a crença de que a máquina "acumula" ou "deve" prêmios.

### Experimento 5: Prêmios Maiores Tornam o Jogo Favorável?
- **Objetivo:** Testar o impacto de um aumento linear de $10\%$ em todos os valores da tabela de premiação sobre a mesma sequência amostral do Experimento 1.
- **Aspectos Analisados:** Demonstração empírica da linearidade da esperança matemática ($E[1,10 \cdot P] = 1,10 \cdot E[P]$), elevação do RTP de $84,00\%$ para $92,40\%$ e constatação de que, apesar do acréscimo nominal nas premiações, a esperança de lucro do jogador permanece negativa ($E[X] = -0,076 < 0$), preservando a vantagem estrutural da casa.

---

## Tecnologias e Bibliotecas

- **Linguagem:** Python (versão 3.10 ou superior; validado no Python 3.12)
- **Manipulação de Dados e Arrays:** `numpy`, `pandas`
- **Visualização Gráfica:** `matplotlib`
- **Testes Automatizados:** `pytest` (validação de regras e casos-limite)

---

## Estrutura do Repositório

```text
tigrinhoManipulado/
│
├── README.md                            # Apresentação do projeto e instruções de uso
├── requirements.txt                     # Relação de dependências do Python
├── .gitignore                           # Exclusões para controle de versão git
├── main.py                              # Interface de Linha de Comando (menu interativo)
│
├── src/                                 # Módulos do código-fonte
│   ├── __init__.py
│   ├── configuracao.py                  # Parâmetros globais, custos e sementes do edital
│   │
│   ├── maquina/                         # Lógica e regras de funcionamento da máquina
│   │   ├── __init__.py
│   │   ├── rolos.py                     # Sorteio do rolo circular e janela 3x3
│   │   └── pagamentos.py                # Tabelas de prêmio, cálculo de P, X e esperança
│   │
│   ├── experimentos/                    # Execução dos cinco experimentos acadêmicos
│   │   ├── __init__.py
│   │   ├── exp1_frequencias.py          # Exp 1: Frequências relativas e proporções
│   │   ├── exp2_lei_grandes_numeros.py  # Exp 2: Monte Carlo e Lei dos Grandes Números
│   │   ├── exp3_saldo_limitado.py       # Exp 3: Saldo finito, regras de parada e ruína
│   │   ├── exp4_prob_condicional.py     # Exp 4: Probabilidade condicional e independência
│   │   └── exp5_premios_maiores.py      # Exp 5: Comparação pareada (+10% de premiação)
│   │
│   └── analise/                         # Funções analíticas e persistência
│       ├── __init__.py
│       ├── metricas.py                  # Média amostral, desvio-padrão (N-1) e RTP
│       ├── exportador.py                # Utilitários de formatação e exportação CSV
│       └── graficos.py                  # Geração de figuras em formato PNG
│
├── tests/                               # Validação automatizada
│   ├── __init__.py
│   └── test_validacoes.py               # Conjunto de 9 testes de integridade via pytest
│
└── resultados/                          # Artefatos gerados pelas simulações
    ├── tabelas/                         # Arquivos .csv com as tabelas de cada experimento
    └── figuras/                         # Gráficos de alta resolução em formato .png
```

---

## Instruções de Instalação e Execução

### 1. Clonagem e Preparação do Ambiente

Recomenda-se a criação de um ambiente virtual isolado para a execução do simulador:

No terminal (Linux / macOS):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

No PowerShell (Windows):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalação das Dependências

Com o ambiente virtual ativado, instale os pacotes requeridos:
```bash
pip install -r requirements.txt
```

### 3. Execução do Simulador

O ponto de entrada principal do projeto é a interface em linha de comando interativa:
```bash
python main.py
```

O menu disponibiliza as seguintes opções:
- **Opção 1:** Realizar uma rodada demonstrativa isolada com visualização da grade $3 \times 3$ e apuração de prêmio na linha central.
- **Opções 2 a 6:** Executar individualmente os Experimentos 1, 2, 3, 4 ou 5, exibindo tabelas formatadas e estatísticas no terminal.
- **Opção 7:** Executar a bateria completa de experimentos em lote, gerando simultaneamente todos os relatórios em `.csv` e gráficos em `.png`.
- **Opção 0:** Encerrar o programa.

### 4. Execução da Suíte de Testes Automatizados

Para verificar a conformidade matemática e a integridade de regras do sistema:
```bash
pytest tests/
```

O conjunto de testes verifica:
1. Conformidade estrita dos pagamentos das 5 triplas premiadas e premiação nula para combinações divergentes.
2. Definição correta do lucro líquido $X = P - 1$ para qualquer desfecho.
3. Reprodutibilidade exata de geradores sob as sementes `10`, `2026` e `123456`.
4. Integridade da soma total de rodadas no Experimento 1 ($10.000$ observações).
5. Estrutura e formato da tabela $3 \times 3$ e trajetórias de convergência do Experimento 2.
6. Regras de parada, integridade das proporções e esgotamento orçamentário do Experimento 3.
7. Independência estocástica e validação dos $9.999$ pares consecutivos do Experimento 4.
8. Propriedades de linearidade na comparação pareada de tabelas do Experimento 5.
9. Caso-limite de saldo insuficiente impedindo a continuidade de apostas.

---

## Artefatos e Resultados Gerados

A execução dos experimentos produz automaticamente arquivos nas seguintes pastas:

- **Tabelas de Dados (`resultados/tabelas/`):**
  - `exp1_frequencias.csv`: Frequências observadas e probabilidades teóricas.
  - `exp2_medias_acumuladas.csv`: Médias acumuladas de lucro nos marcos $N = 100$, $1.000$ e $10.000$.
  - `exp3_participantes.csv`: Registro detalhado de rodadas jogadas e saldo final de cada participante.
  - `exp4_prob_condicional.csv`: Tabela de contingência e probabilidades de transição entre rodadas consecutivas.
  - `exp5_comparacao_tabelas.csv`: Tabela comparativa pareada entre a regra Base e a regra com acréscimo de $10\%$.

- **Figuras Gráficas (`resultados/figuras/`):**
  - `exp1_frequencias.png`: Gráfico de barras comparando frequência observada versus probabilidade teórica.
  - `exp2_convergencia.png`: Trajetórias de convergência da média amostral para a reta $E[X] = -0,16$.
  - `exp3_trajetorias.png`: Curvas de evolução temporal do saldo para os 5 primeiros participantes.

---

## Declaração de Uso de Ferramentas de Inteligência Artificial

Em estrito cumprimento às diretrizes éticas e acadêmicas estipuladas pelo edital do projeto:

- **Ferramenta Utilizada:** Google Antigravity / Gemini.
- **Escopo do Suporte:** Auxílio na estruturação modular do projeto, formatação de docstrings e comentários, organização dos scripts de teste automatizado e suporte à redação técnica da documentação.
- **Autoria e Conferência Humana:** Todas as implementações algorítmicas, validações de cálculo estocástico, auditoria de sementes, análise de dados e redação das discussões críticas interdisciplinares foram integralmente concebidas, conferidas e aprovadas pela equipe de discentes.
