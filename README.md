# Máquina Estatística: Probabilidade, Apostas e Pensamento Crítico

Projeto acadêmico desenvolvido para a disciplina de **Probabilidade e Estatística I** do curso de **Bacharelado em Sistemas de Informação** do **Instituto Federal do Espírito Santo (IFES) – Campus Serra**.

**Professor:** Fidelis Zanetti de Castro  
**Aviso Obrigatório:** *Simulador acadêmico - somente créditos fictícios.*

---

## 👥 Integrantes da Equipe

- **Nome do Integrante 1:** [Seu Nome Completo] - [Matrícula]
- **Nome do Integrante 2:** [Nome Completo] - [Matrícula]
- **Nome do Integrante 3:** [Nome Completo] - [Matrícula]

---

## 🎯 Objetivo do Projeto

Construir um simulador computacional com regras transparentes e públicas baseado em um modelo de máquina caça-níqueis (rolos digitais 3×3), permitindo:
1. Calcular probabilidades teóricas e esperanças matemáticas ($E[P]$, $E[X]$, $RTP$).
2. Executar simulações estocásticas e confrontar a teoria com os dados empíricos por meio de cinco experimentos.
3. Fornecer base quantitativa sólida para uma discussão crítica e interdisciplinar sobre saúde pública, renda familiar, tecnologia e políticas públicas de regulação de apostas no Brasil.

---

## 🛠️ Tecnologias e Bibliotecas

- **Linguagem:** Python (versão 3.10 ou superior recomendada)
- **Cálculo Numérico e Manipulação de Dados:** `numpy`, `pandas`
- **Visualização Gráfica:** `matplotlib`
- **Testes Automatizados:** `pytest` (para validações dos pontos extras)

---

## 📁 Estrutura de Diretórios

```text
tigrinhoManipulado/
│
├── README.md                            # Documentação, instruções e declaração de IA
├── requirements.txt                     # Dependências do projeto
├── .gitignore                           # Exclusões para controle de versão
├── main.py                              # Ponto de entrada CLI (menu interativo no terminal)
│
├── src/                                 # Código-fonte da aplicação
│   ├── __init__.py
│   ├── configuracao.py                  # Parâmetros e sementes fixadas pelo edital
│   │
│   ├── maquina/                         # Mecânica e regras da máquina
│   │   ├── __init__.py
│   │   ├── rolos.py                     # Sorteio dos rolos circulares e montagem da janela 3x3
│   │   └── pagamentos.py                # Tabelas de pagamento, cálculo de prêmio P e lucro X
│   │
│   ├── experimentos/                    # Módulos para os cinco experimentos obrigatórios
│   │   ├── __init__.py
│   │   ├── exp1_frequencias.py          # Exp 1: Frequências relativas vs probabilidades teóricas
│   │   ├── exp2_lei_grandes_numeros.py  # Exp 2: Monte Carlo, convergência e Lei dos Grandes Números
│   │   ├── exp3_saldo_limitado.py       # Exp 3: Simulação de 100 jogadores com saldo finito e ruína
│   │   ├── exp4_prob_condicional.py     # Exp 4: Probabilidade condicional e falácia do apostador
│   │   └── exp5_premios_maiores.py      # Exp 5: Comparação com tabela de pagamentos inflacionada (+10%)
│   │
│   └── analise/                         # Funções auxiliares estatísticas e exportações
│       ├── __init__.py
│       ├── metricas.py                  # Média, desvio-padrão amostral (N-1), RTP e proporções
│       ├── exportador.py                # Exportação de resultados tabulares em CSV
│       └── graficos.py                  # Geração de gráficos para o relatório acadêmico
│
├── tests/                               # Testes e validações automatizadas (pontos extras)
│   ├── __init__.py
│   └── test_validacoes.py               # Verificações de regras, lucros, sementes e casos-limite
│
├── resultados/                          # Saídas geradas pelas simulações
│   ├── tabelas/                         # Arquivos .csv com as tabelas geradas
│   └── figuras/                         # Imagens .png dos gráficos prontos para o relatório
│
└── relatorio/                           # Documentos de suporte à redação do relatório em PDF
    ├── referencias.md                   # Fichamento das fontes (OMS, Lancet, LENAD III, TCU, IEPS)
    └── roteiro_discussao.md             # Guia dos 4 eixos de discussão crítica do edital
```

---

## 🚀 Como Executar o Projeto

### 1. Criar e ativar o ambiente virtual (recomendado)

No terminal (Linux/macOS):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

No PowerShell (Windows):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o simulador

```bash
python main.py
```

### 4. Executar os testes automatizados

```bash
pytest tests/
```

---

## 📊 Localização dos Resultados Gerados

- As tabelas numéricas dos experimentos serão gravadas em formato `.csv` dentro da pasta:
  `resultados/tabelas/`
- Os gráficos de apoio para o relatório em PDF serão salvos em formato `.png` na pasta:
  `resultados/figuras/`

---

## 🤖 Declaração de Uso de Ferramentas de Inteligência Artificial

Em estrito cumprimento às instruções do trabalho acadêmico (Seções 4 e 11 do edital):

- **Uso de IA:** [Declarar aqui se utilizou IA no desenvolvimento, por exemplo: Google Antigravity / Gemini / ChatGPT].
- **Escopo do Apoio:** A IA foi utilizada no suporte ao planejamento da arquitetura de pastas, sugestão de assinaturas de funções e organização do esqueleto do projeto.
- **Conferência e Autoria Humana:** Toda a lógica matemática, implementação das simulações, conferência das sementes, análise de dados e redação das discussões críticas foram integralmente realizadas e revisadas pelos integrantes do grupo.
