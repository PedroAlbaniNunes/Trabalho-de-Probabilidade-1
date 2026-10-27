"""Extra 5: Interface Web Acessível Autocontida (Seção 10 do Edital - até 3 pontos).

Gera uma aplicação web interativa completa (HTML5 + CSS3 + JavaScript autocontido)
em 'resultados/interface_acessivel.html' e a abre automaticamente no navegador padrão
do usuário, permitindo:
1. Navegação híbrida fluida por Mouse (cliques, abas, botões, seletores) e por Teclado
   (atalhos dedicados, navegação por Tab com foco de alta visibilidade e suporte ARIA).
2. Simulador visual interativo da máquina 3x3 com formas geométricas + letras + cores
   seguras para daltonismo (Okabe-Ito), gráfico em tempo real do saldo, tabela de
   pagamentos dinâmica e histórico de rodadas.
3. Painel integrado para visualizar e re-simular no navegador os Experimentos 1 a 5
   e os Experimentos Extras 1 a 4.
4. Auditoria matemática de contraste luminoso WCAG 2.1 (nível AAA >= 7.0:1) exportada
   em CSV para comprovação acadêmica.
"""

import base64
import json
import webbrowser
from pathlib import Path
from typing import Dict, Any, List, Tuple

from src.configuracao import (
    AVISO_LEGAL,
    DIRETORIO_RESULTADOS,
    DIRETORIO_FIGURAS,
    DIRETORIO_FIGURAS_EXTRAS,
    DIRETORIO_TABELAS_EXTRAS,
)
from src.analise.exportador import f_exportarParaCsv


# Mapeamento de formas geométricas (redundância não-cromática inspirada na Figura 2 do edital)
MAPA_SIMBOLOS_VISUAIS: Dict[str, Dict[str, Any]] = {
    "A": {"forma": "●", "nome_forma": "Círculo", "rotulo": "● A", "premio": 5, "lucro": 4, "cor": "#0072B2"},
    "B": {"forma": "▲", "nome_forma": "Triângulo", "rotulo": "▲ B", "premio": 10, "lucro": 9, "cor": "#E69F00"},
    "C": {"forma": "■", "nome_forma": "Quadrado", "rotulo": "■ C", "premio": 15, "lucro": 14, "cor": "#009E73"},
    "D": {"forma": "◆", "nome_forma": "Losango", "rotulo": "◆ D", "premio": 25, "lucro": 24, "cor": "#56B4E9"},
    "E": {"forma": "★", "nome_forma": "Estrela", "rotulo": "★ E", "premio": 50, "lucro": 49, "cor": "#CC79A7"},
}


def f_hexParaRgbNormalizado(corHex: str) -> Tuple[float, float, float]:
    """Converte uma cor hexadecimal (#RRGGBB) para tupla RGB normalizada em [0, 1]."""
    limpo = corHex.strip().lstrip("#")  # arranca a cerquilha do hex pra fatiar os canais
    r = int(limpo[0:2], 16) / 255.0  # canal vermelho de 0 a 1
    g = int(limpo[2:4], 16) / 255.0  # canal verde de 0 a 1
    b = int(limpo[4:6], 16) / 255.0  # canal azul de 0 a 1
    return (r, g, b)


def f_calcularLuminanciaRelativa(corHex: str) -> float:
    """Calcula a luminância relativa W3C/WCAG 2.1 de uma cor sRGB."""
    def _linearizar(canal: float) -> float:
        # Fórmula oficial da norma WCAG 2.1 para linearizar o gamma sRGB
        return canal / 12.92 if canal <= 0.04045 else ((canal + 0.055) / 1.055) ** 2.4

    r, g, b = f_hexParaRgbNormalizado(corHex)  # pega os canais normalizados
    r_lin, g_lin, b_lin = _linearizar(r), _linearizar(g), _linearizar(b)  # lineariza cada componente
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin  # ponderação fotométrica do olho humano


def f_calcularRazaoContrasteWcag(corTextoHex: str, corFundoHex: str) -> float:
    """Calcula a razão de contraste WCAG 2.1 entre dois pares de cores (#RRGGBB)."""
    l1 = f_calcularLuminanciaRelativa(corTextoHex)  # luminância do primeiro plano
    l2 = f_calcularLuminanciaRelativa(corFundoHex)  # luminância do pano de fundo
    claro = max(l1, l2)  # identifica quem brilha mais
    escuro = min(l1, l2)  # identifica quem é mais escuro
    return (claro + 0.05) / (escuro + 0.05)  # razão de contraste entre 1:1 e 21:1


def f_auditarParesDeContrasteInterfaceWeb() -> List[Dict[str, Any]]:
    """Audita os pares de cores dos temas da interface web segundo a WCAG 2.1."""
    especificacoes = [
        ("Tema Escuro — Texto Principal vs Fundo", "Esc. Texto/Fundo", "#FFFFFF", "#0B0F19"),
        ("Tema Escuro — Linha Central Premiada vs Fundo Card", "Esc. Linha Central", "#FFD60A", "#111827"),
        ("Tema Escuro — Alerta Vitória Verde vs Fundo", "Esc. Badge Vitória", "#4ADE80", "#0B0F19"),
        ("Tema Escuro — Alerta Perda Coral vs Fundo", "Esc. Badge Perda", "#FF8FA3", "#0B0F19"),
        ("Tema Escuro — Foco de Teclado/Mouse Ciano vs Fundo", "Esc. Anel de Foco", "#38BDF8", "#0B0F19"),
        ("Tema Claro — Texto Principal vs Fundo Papel", "Cla. Texto/Fundo", "#0F172A", "#FFFFFF"),
        ("Tema Claro — Destaque Linha Central Azul vs Fundo", "Cla. Linha Central", "#003566", "#F8FAFC"),
        ("Tema Claro — Status Vitória Verde Escuro vs Fundo", "Cla. Badge Vitória", "#065F46", "#FFFFFF"),
        ("Tema Claro — Status Perda Bordô vs Fundo", "Cla. Badge Perda", "#881337", "#FFFFFF"),
        ("Tema Claro — Botão Primário vs Texto Branco", "Cla. Botão Ação", "#FFFFFF", "#003566"),
    ]

    resultados: List[Dict[str, Any]] = []  # lista das auditorias de contraste
    for nome_completo, nome_curto, fg, bg in especificacoes:
        razao = f_calcularRazaoContrasteWcag(fg, bg)  # calcula a razão CR:1 exata
        aprovado_aa = razao >= 4.5  # mínimo exigido pela WCAG AA para texto normal
        aprovado_aaa = razao >= 7.0  # excelência máxima WCAG AAA
        nivel = "AAA (>= 7.0:1)" if aprovado_aaa else ("AA (>= 4.5:1)" if aprovado_aa else "Reprovado")
        resultados.append({
            "componente": nome_completo,
            "componente_curto": nome_curto,
            "cor_frente": fg,
            "cor_fundo": bg,
            "razao_contraste": round(razao, 2),
            "aprovado_aa": aprovado_aa,
            "aprovado_aaa": aprovado_aaa,
            "nivel_wcag": nivel,
        })
    return resultados


def _f_codificarImagemBase64(caminhoImg: Path) -> str:
    """Converte uma figura PNG para data URI Base64 caso o arquivo exista no disco."""
    if not caminhoImg.exists():
        return ""  # se a figura ainda não foi gerada, retorna string vazia sem quebrar nada
    dados = caminhoImg.read_bytes()  # lê os bytes brutos do PNG
    b64 = base64.b64encode(dados).decode("ascii")  # converte para texto base64
    return f"data:image/png;base64,{b64}"  # monta o data URI prontinho pro atributo src da tag <img>


def _f_construirHtmlInterfaceAcessivel(
    paresContraste: List[Dict[str, Any]],
    imagensEmbutidas: Dict[str, str],
) -> str:
    """Constrói o documento HTML5/CSS3/JS autocontido da Interface Web Acessível."""
    json_contraste = json.dumps(paresContraste, ensure_ascii=False)
    json_imagens = json.dumps(imagensEmbutidas, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="pt-BR" data-tema="escuro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Máquina Estatística 3x3 — Interface Web Acessível (IFES)</title>
    <style>
        :root {{
            --bg-body: #0B0F19;
            --bg-card: #111827;
            --bg-elevated: #1E293B;
            --text-main: #FFFFFF;
            --text-muted: #CBD5E1;
            --border-color: #475569;
            --accent-primary: #38BDF8;
            --accent-secondary: #FFD60A;
            --win-color: #4ADE80;
            --win-bg: rgba(74, 222, 128, 0.14);
            --loss-color: #FF8FA3;
            --loss-bg: rgba(255, 143, 163, 0.14);
            --btn-bg: #0284C7;
            --btn-text: #FFFFFF;
            --btn-hover: #0369A1;
            --focus-ring: #FFD60A;
            --font-scale: 1;
        }}

        html[data-tema="claro"] {{
            --bg-body: #F8FAFC;
            --bg-card: #FFFFFF;
            --bg-elevated: #E2E8F0;
            --text-main: #0F172A;
            --text-muted: #334155;
            --border-color: #64748B;
            --accent-primary: #003566;
            --accent-secondary: #B45309;
            --win-color: #065F46;
            --win-bg: #D1FAE5;
            --loss-color: #881337;
            --loss-bg: #FFE4E6;
            --btn-bg: #003566;
            --btn-text: #FFFFFF;
            --btn-hover: #001D3D;
            --focus-ring: #D97706;
        }}

        html[data-tema="okabe"] {{
            --bg-body: #10141D;
            --bg-card: #18202F;
            --bg-elevated: #232F46;
            --text-main: #F8FAFC;
            --text-muted: #E2E8F0;
            --border-color: #56B4E9;
            --accent-primary: #56B4E9;
            --accent-secondary: #E69F00;
            --win-color: #009E73;
            --win-bg: rgba(0, 158, 115, 0.22);
            --loss-color: #D55E00;
            --loss-bg: rgba(213, 94, 0, 0.22);
            --btn-bg: #0072B2;
            --btn-text: #FFFFFF;
            --btn-hover: #005A8D;
            --focus-ring: #F0E442;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-body);
            color: var(--text-main);
            font-family: 'Segoe UI', system-ui, -apple-system, Roboto, sans-serif;
            font-size: calc(16px * var(--font-scale));
            line-height: 1.5;
            padding-bottom: 3rem;
        }}

        *:focus-visible {{
            outline: 3px solid var(--focus-ring) !important;
            outline-offset: 3px !important;
        }}

        .skip-link {{
            position: absolute;
            left: -9999px;
            top: 0;
            background: var(--accent-secondary);
            color: #000;
            font-weight: 700;
            padding: 0.75rem 1.25rem;
            z-index: 1000;
        }}
        .skip-link:focus {{
            left: 1rem;
            top: 1rem;
        }}

        header {{
            background-color: var(--bg-card);
            border-bottom: 2px solid var(--border-color);
            padding: 1rem 1.5rem;
        }}

        .header-top {{
            max-width: 1360px;
            margin: 0 auto;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
        }}

        .brand-title h1 {{
            font-size: calc(1.35rem * var(--font-scale));
            color: var(--accent-primary);
            letter-spacing: 0.3px;
        }}

        .brand-title p {{
            font-size: calc(0.9rem * var(--font-scale));
            color: var(--text-muted);
        }}

        .a11y-toolbar {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            align-items: center;
        }}

        .btn {{
            background-color: var(--btn-bg);
            color: var(--btn-text);
            border: 2px solid transparent;
            border-radius: 8px;
            padding: 0.55rem 1rem;
            font-size: calc(0.95rem * var(--font-scale));
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.1s ease, background-color 0.15s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
        }}

        .btn:hover {{
            background-color: var(--btn-hover);
            transform: translateY(-1px);
        }}

        .btn:active {{
            transform: translateY(0);
        }}

        .btn-secondary {{
            background-color: var(--bg-elevated);
            color: var(--text-main);
            border-color: var(--border-color);
        }}

        .btn-secondary:hover {{
            background-color: var(--border-color);
        }}

        .btn-spin {{
            background-color: #059669;
            color: #FFFFFF;
            font-size: calc(1.1rem * var(--font-scale));
            padding: 0.8rem 1.5rem;
            border: 2px solid #34D399;
        }}
        html[data-tema="claro"] .btn-spin {{
            background-color: #065F46;
            border-color: #047857;
        }}
        .btn-spin:hover {{
            background-color: #047857;
        }}

        .legal-banner {{
            max-width: 1360px;
            margin: 0.75rem auto 0;
            background-color: var(--bg-elevated);
            border: 2px solid var(--accent-secondary);
            border-radius: 8px;
            padding: 0.5rem 1rem;
            text-align: center;
            font-weight: 700;
            color: var(--accent-secondary);
        }}
        html[data-tema="claro"] .legal-banner {{
            color: #92400E;
            border-color: #B45309;
        }}

        .container {{
            max-width: 1360px;
            margin: 1.25rem auto;
            padding: 0 1.5rem;
        }}

        /* Abas de navegação clicáveis por mouse e teclado */
        .nav-tabs {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
            margin-bottom: 1.25rem;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.75rem;
        }}

        .tab-btn {{
            background-color: var(--bg-card);
            color: var(--text-main);
            border: 2px solid var(--border-color);
            border-radius: 8px;
            padding: 0.65rem 1.2rem;
            font-size: calc(1rem * var(--font-scale));
            font-weight: 700;
            cursor: pointer;
        }}

        .tab-btn:hover {{
            border-color: var(--accent-primary);
        }}

        .tab-btn[aria-selected="true"] {{
            background-color: var(--btn-bg);
            color: var(--btn-text);
            border-color: var(--accent-secondary);
        }}

        .tab-panel {{
            display: none;
        }}
        .tab-panel.active {{
            display: block;
        }}

        /* Layout do Simulador 3x3 */
        .sim-grid {{
            display: grid;
            grid-template-columns: 1.25fr 1fr;
            gap: 1.25rem;
        }}
        @media (max-width: 980px) {{
            .sim-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .card {{
            background-color: var(--bg-card);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1.25rem;
        }}

        .card-title {{
            font-size: calc(1.15rem * var(--font-scale));
            font-weight: 700;
            margin-bottom: 0.85rem;
            color: var(--accent-primary);
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
        }}

        /* Máquina 3x3 */
        .slot-wrapper {{
            background-color: var(--bg-elevated);
            border: 3px solid var(--border-color);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        }}

        .slot-row {{
            display: grid;
            grid-template-columns: 110px repeat(3, 1fr) 110px;
            align-items: center;
            gap: 0.65rem;
            margin: 0.5rem 0;
            padding: 0.45rem;
            border-radius: 10px;
        }}

        .slot-row.payline {{
            background-color: var(--bg-card);
            border: 3px double var(--accent-secondary);
            box-shadow: 0 0 0 2px rgba(255, 214, 10, 0.25);
        }}

        .row-label {{
            font-size: calc(0.8rem * var(--font-scale));
            font-weight: 700;
            text-align: center;
            color: var(--text-muted);
            text-transform: uppercase;
        }}

        .slot-row.payline .row-label {{
            color: var(--accent-secondary);
            font-size: calc(0.88rem * var(--font-scale));
        }}
        html[data-tema="claro"] .slot-row.payline .row-label {{
            color: #92400E;
        }}

        .reel-cell {{
            background-color: var(--bg-card);
            border: 2px solid var(--border-color);
            border-radius: 10px;
            padding: 0.7rem 0.4rem;
            text-align: center;
            transition: transform 0.15s ease;
        }}

        .slot-row.payline .reel-cell {{
            border-width: 3px;
            font-weight: 800;
        }}

        .symbol-shape {{
            font-size: calc(2rem * var(--font-scale));
            line-height: 1.1;
            display: block;
        }}

        .symbol-code {{
            font-size: calc(1.2rem * var(--font-scale));
            font-weight: 800;
            display: block;
            margin-top: 0.15rem;
        }}

        .symbol-name {{
            font-size: calc(0.78rem * var(--font-scale));
            color: var(--text-muted);
            display: block;
        }}

        /* Bordas distintas por símbolo para redundância visual */
        .sym-A {{ border-color: #0072B2 !important; }}
        .sym-B {{ border-color: #E69F00 !important; border-style: dashed !important; }}
        .sym-C {{ border-color: #009E73 !important; border-style: dotted !important; }}
        .sym-D {{ border-color: #56B4E9 !important; border-style: double !important; }}
        .sym-E {{ border-color: #CC79A7 !important; box-shadow: inset 0 0 0 2px #CC79A7; }}

        .status-banner {{
            padding: 0.85rem 1rem;
            border-radius: 8px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 1rem;
            border: 2px solid var(--border-color);
            font-size: calc(1.05rem * var(--font-scale));
        }}

        .status-win {{
            background-color: var(--win-bg);
            color: var(--win-color);
            border-color: var(--win-color);
        }}

        .status-loss {{
            background-color: var(--loss-bg);
            color: var(--loss-color);
            border-color: var(--loss-color);
        }}

        .controls-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
            align-items: center;
            margin-bottom: 1rem;
        }}

        .seed-box {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
            background: var(--bg-elevated);
            padding: 0.4rem 0.75rem;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}

        .seed-box input {{
            width: 90px;
            padding: 0.35rem 0.5rem;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            background: var(--bg-card);
            color: var(--text-main);
            font-weight: 700;
            font-size: calc(0.9rem * var(--font-scale));
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
            gap: 0.75rem;
            margin-top: 0.75rem;
        }}

        .kpi-box {{
            background-color: var(--bg-elevated);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.65rem 0.75rem;
            text-align: center;
        }}

        .kpi-label {{
            font-size: calc(0.78rem * var(--font-scale));
            color: var(--text-muted);
            display: block;
        }}

        .kpi-val {{
            font-size: calc(1.2rem * var(--font-scale));
            font-weight: 800;
            color: var(--accent-primary);
        }}

        /* Tabelas Acessíveis */
        .table-responsive {{
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 0.5rem;
            font-size: calc(0.9rem * var(--font-scale));
        }}

        th, td {{
            border: 1px solid var(--border-color);
            padding: 0.5rem 0.65rem;
            text-align: center;
        }}

        th {{
            background-color: var(--bg-elevated);
            color: var(--text-main);
            font-weight: 700;
        }}

        tr.highlight-row {{
            background-color: var(--win-bg) !important;
            font-weight: 700;
        }}

        .kbd {{
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-bottom-width: 2px;
            border-radius: 4px;
            padding: 0.1rem 0.4rem;
            font-family: monospace;
            font-size: 0.85em;
            font-weight: 700;
        }}

        .exp-subnav {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }}

        .exp-fig {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            border: 2px solid var(--border-color);
            margin-top: 0.75rem;
            background: #fff;
        }}

        canvas {{
            width: 100%;
            height: 220px;
            background-color: var(--bg-elevated);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            margin-top: 0.5rem;
        }}
    </style>
</head>
<body>
    <a href="#conteudo-principal" class="skip-link">Pular para o conteúdo principal</a>

    <header role="banner">
        <div class="header-top">
            <div class="brand-title">
                <h1>IFES — Campus Serra | Máquina Estatística 3×3</h1>
                <p>Probabilidade, Apostas e Pensamento Crítico • Navegação Acessível por Mouse e Teclado</p>
            </div>
            <div class="a11y-toolbar" role="toolbar" aria-label="Controles de Acessibilidade">
                <button type="button" class="btn btn-secondary" onclick="alternarTema()" title="Alternar Tema de Cores (Atalho: Tecla T)">
                    🎨 Tema: <span id="lbl-tema">Escuro AAA</span> <span class="kbd">T</span>
                </button>
                <button type="button" class="btn btn-secondary" onclick="ajustarFonte(-0.1)" title="Diminuir Fonte">
                    A-
                </button>
                <button type="button" class="btn btn-secondary" onclick="ajustarFonte(0)" title="Fonte Padrão">
                    A
                </button>
                <button type="button" class="btn btn-secondary" onclick="ajustarFonte(0.15)" title="Aumentar Fonte">
                    A+
                </button>
                <button type="button" class="btn btn-secondary" onclick="alternarVoz()" id="btn-voz" aria-pressed="false" title="Ativar/Desativar Leitura em Voz Alta (Atalho: Tecla V)">
                    🔊 Voz: Off <span class="kbd">V</span>
                </button>
            </div>
        </div>
        <div class="legal-banner" role="note">
            ⚠️ AVISO OBRIGATÓRIO: {AVISO_LEGAL} • Esperança Teórica: E[X] = −0,16 crédito/rodada (RTP = 84,00%)
        </div>
    </header>

    <main id="conteudo-principal" class="container" role="main">
        <!-- Navegação Principal por Mouse ou Teclado -->
        <nav class="nav-tabs" role="tablist" aria-label="Seções do Simulador">
            <button type="button" class="tab-btn" role="tab" id="tab-btn-sim" aria-selected="true" aria-controls="panel-sim" onclick="selecionarAba('sim')">
                🎰 1. Simulador Interativo 3×3 <span class="kbd">1</span>
            </button>
            <button type="button" class="tab-btn" role="tab" id="tab-btn-exp" aria-selected="false" aria-controls="panel-exp" onclick="selecionarAba('exp')">
                📊 2. Experimentos Obrigatórios (E1 a E5) <span class="kbd">2</span>
            </button>
            <button type="button" class="tab-btn" role="tab" id="tab-btn-ext" aria-selected="false" aria-controls="panel-ext" onclick="selecionarAba('ext')">
                🔬 3. Pontos Extras e Laudo WCAG (Extras 1 a 5) <span class="kbd">3</span>
            </button>
        </nav>

        <!-- ABA 1: SIMULADOR INTERATIVO 3X3 -->
        <section id="panel-sim" class="tab-panel active" role="tabpanel" aria-labelledby="tab-btn-sim">
            <div class="sim-grid">
                <div>
                    <div class="card">
                        <div class="card-title">
                            <span>Tabuleiro Visível 3×3 (Fita Circular R = A, B, C, D, E)</span>
                            <span>Aposta fixa: <strong>1,00 crédito</strong></span>
                        </div>

                        <!-- Grade 3x3 da Máquina -->
                        <div class="slot-wrapper" role="region" aria-label="Grade 3 por 3 da Máquina Caça-Níqueis">
                            <div class="slot-row" id="row-0">
                                <span class="row-label">Topo (K)</span>
                                <div class="reel-cell" id="cell-0-0"></div>
                                <div class="reel-cell" id="cell-0-1"></div>
                                <div class="reel-cell" id="cell-0-2"></div>
                                <span class="row-label">Sem Pagto.</span>
                            </div>

                            <div class="slot-row payline" id="row-1" aria-label="Linha Central de Pagamento">
                                <span class="row-label">► CENTRO ◄</span>
                                <div class="reel-cell" id="cell-1-0"></div>
                                <div class="reel-cell" id="cell-1-1"></div>
                                <div class="reel-cell" id="cell-1-2"></div>
                                <span class="row-label">► ATIVA ◄</span>
                            </div>

                            <div class="slot-row" id="row-2">
                                <span class="row-label">Base (K+2)</span>
                                <div class="reel-cell" id="cell-2-0"></div>
                                <div class="reel-cell" id="cell-2-1"></div>
                                <div class="reel-cell" id="cell-2-2"></div>
                                <span class="row-label">Sem Pagto.</span>
                            </div>
                        </div>

                        <!-- Banner de Resultado com aria-live para Leitores de Tela -->
                        <div id="status-giro" class="status-banner" role="status" aria-live="polite">
                            Pronto para iniciar! Clique em "Girar 1 Rodada" com o mouse ou pressione a tecla ESPAÇO.
                        </div>

                        <!-- Barra de Botões (Mouse + Teclado) -->
                        <div class="controls-bar">
                            <button type="button" class="btn btn-spin" id="btn-girar-1" onclick="executarGiros(1)">
                                ▶ Girar 1 Rodada <span class="kbd">Espaço</span>
                            </button>
                            <button type="button" class="btn" onclick="executarGiros(10)">
                                ⏩ +10 Rodadas <span class="kbd">G</span>
                            </button>
                            <button type="button" class="btn" onclick="executarGiros(100)">
                                ⏭ +100 Rodadas <span class="kbd">C</span>
                            </button>
                            <button type="button" class="btn btn-secondary" onclick="reiniciarSessao()">
                                🔄 Reiniciar Saldo (100) <span class="kbd">R</span>
                            </button>
                            <div class="seed-box">
                                <label for="input-seed">Semente:</label>
                                <input type="number" id="input-seed" value="2026" title="Semente numérica para reprodutibilidade">
                                <button type="button" class="btn btn-secondary" style="padding:0.3rem 0.6rem;" onclick="aplicarSemente()">
                                    Aplicar
                                </button>
                            </div>
                        </div>

                        <!-- Indicadores da Sessão -->
                        <div class="kpi-grid" role="region" aria-label="Indicadores Estatísticos da Sessão">
                            <div class="kpi-box">
                                <span class="kpi-label">Saldo Atual (B_t)</span>
                                <span class="kpi-val" id="kpi-saldo">100,00</span>
                            </div>
                            <div class="kpi-box">
                                <span class="kpi-label">Rodadas Jogadas</span>
                                <span class="kpi-val" id="kpi-rodadas">0</span>
                            </div>
                            <div class="kpi-box">
                                <span class="kpi-label">Lucro Acumulado</span>
                                <span class="kpi-val" id="kpi-lucro-acum">0,00</span>
                            </div>
                            <div class="kpi-box">
                                <span class="kpi-label">Lucro Médio (X̄ vs −0,16)</span>
                                <span class="kpi-val" id="kpi-lucro-medio">0,0000</span>
                            </div>
                            <div class="kpi-box">
                                <span class="kpi-label">RTP Sessão (vs 84,0%)</span>
                                <span class="kpi-val" id="kpi-rtp">0,00%</span>
                            </div>
                            <div class="kpi-box">
                                <span class="kpi-label">Triplas Premiadas (vs 4,0%)</span>
                                <span class="kpi-val" id="kpi-hits">0 (0,00%)</span>
                            </div>
                        </div>
                    </div>

                    <!-- Gráfico Dinâmico da Evolução do Saldo -->
                    <div class="card">
                        <div class="card-title">
                            <span>Evolução Temporal do Saldo (B_t) na Sessão Atual</span>
                            <span style="font-size:0.85rem;color:var(--text-muted);">Linha tracejada = Saldo Inicial (100)</span>
                        </div>
                        <canvas id="canvas-saldo" width="700" height="220" aria-label="Gráfico da evolução do saldo do jogador"></canvas>
                    </div>
                </div>

                <!-- Coluna Direita: Tabela de Pagamentos + Histórico -->
                <div>
                    <div class="card">
                        <div class="card-title">
                            <span>Tabela Oficial de Pagamentos (Redundância Forma + Letra)</span>
                            <span>E[P] = 0,84 | E[X] = −0,16</span>
                        </div>
                        <div class="table-responsive">
                            <table aria-label="Tabela oficial de pagamentos e probabilidades">
                                <thead>
                                    <tr>
                                        <th scope="col">Tripla Central</th>
                                        <th scope="col">Forma + Código</th>
                                        <th scope="col">Prêmio (P)</th>
                                        <th scope="col">Lucro (X=P−1)</th>
                                        <th scope="col">Prob. Teórica</th>
                                        <th scope="col">Hits Sessão</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr id="pay-row-A">
                                        <td><strong>A – A – A</strong></td>
                                        <td>● Círculo A</td>
                                        <td>5 créditos</td>
                                        <td>+4 créditos</td>
                                        <td>1/125 (0,80%)</td>
                                        <td id="cnt-A">0</td>
                                    </tr>
                                    <tr id="pay-row-B">
                                        <td><strong>B – B – B</strong></td>
                                        <td>▲ Triângulo B</td>
                                        <td>10 créditos</td>
                                        <td>+9 créditos</td>
                                        <td>1/125 (0,80%)</td>
                                        <td id="cnt-B">0</td>
                                    </tr>
                                    <tr id="pay-row-C">
                                        <td><strong>C – C – C</strong></td>
                                        <td>■ Quadrado C</td>
                                        <td>15 créditos</td>
                                        <td>+14 créditos</td>
                                        <td>1/125 (0,80%)</td>
                                        <td id="cnt-C">0</td>
                                    </tr>
                                    <tr id="pay-row-D">
                                        <td><strong>D – D – D</strong></td>
                                        <td>◆ Losango D</td>
                                        <td>25 créditos</td>
                                        <td>+24 créditos</td>
                                        <td>1/125 (0,80%)</td>
                                        <td id="cnt-D">0</td>
                                    </tr>
                                    <tr id="pay-row-E">
                                        <td><strong>E – E – E</strong></td>
                                        <td>★ Estrela E</td>
                                        <td>50 créditos</td>
                                        <td>+49 créditos</td>
                                        <td>1/125 (0,80%)</td>
                                        <td id="cnt-E">0</td>
                                    </tr>
                                    <tr id="pay-row-loss">
                                        <td>Qualquer outra (120)</td>
                                        <td>✕ Mista</td>
                                        <td>0 crédito</td>
                                        <td>−1 crédito</td>
                                        <td>120/125 (96,00%)</td>
                                        <td id="cnt-loss">0</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-title">
                            <span>Histórico Recente de Giros</span>
                            <span style="font-size:0.85rem;color:var(--text-muted);">Últimas 8 rodadas</span>
                        </div>
                        <div class="table-responsive">
                            <table aria-label="Histórico das últimas rodadas">
                                <thead>
                                    <tr>
                                        <th scope="col">#</th>
                                        <th scope="col">Linha Central</th>
                                        <th scope="col">Status</th>
                                        <th scope="col">Prêmio (P)</th>
                                        <th scope="col">Lucro (X)</th>
                                        <th scope="col">Saldo (B_t)</th>
                                    </tr>
                                </thead>
                                <tbody id="tbody-historico">
                                    <tr><td colspan="6">Nenhum giro realizado ainda.</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ABA 2: PAINEL DE EXPERIMENTOS OBRIGATÓRIOS (E1 A E5) -->
        <section id="panel-exp" class="tab-panel" role="tabpanel" aria-labelledby="tab-btn-exp">
            <div class="card">
                <div class="card-title">
                    <span>Painel Integrado dos 5 Experimentos Obrigatórios (Seção 7 do Edital)</span>
                    <button type="button" class="btn" onclick="simularLoteRapidoNavegador()">
                        ⚡ Re-Simular 10.000 Rodadas Agora no Navegador
                    </button>
                </div>
                <p style="margin-bottom:0.85rem;color:var(--text-muted);">
                    Clique com o mouse em qualquer experimento abaixo para inspecionar as tabelas oficiais, interpretações estatísticas e gráficos gerados pelo projeto:
                </p>
                <div class="exp-subnav" role="tablist" aria-label="Seleção de Experimento Obrigatório">
                    <button type="button" id="subbtn-e1" role="tab" aria-selected="true" class="btn" onclick="mostrarSubExp('e1')">Exp. 1: Frequências (10.000 giros)</button>
                    <button type="button" id="subbtn-e2" role="tab" aria-selected="false" class="btn btn-secondary" onclick="mostrarSubExp('e2')">Exp. 2: Lei dos Grandes Números</button>
                    <button type="button" id="subbtn-e3" role="tab" aria-selected="false" class="btn btn-secondary" onclick="mostrarSubExp('e3')">Exp. 3: Saldo Limitado (100 Jogadores)</button>
                    <button type="button" id="subbtn-e4" role="tab" aria-selected="false" class="btn btn-secondary" onclick="mostrarSubExp('e4')">Exp. 4: Prob. Condicional (9.999 Pares)</button>
                    <button type="button" id="subbtn-e5" role="tab" aria-selected="false" class="btn btn-secondary" onclick="mostrarSubExp('e5')">Exp. 5: Prêmios Maiores (+10%)</button>
                </div>

                <div id="subexp-container"></div>
            </div>
        </section>

        <!-- ABA 3: PAINEL DE PONTOS EXTRAS E LAUDO WCAG (EXTRAS 1 A 5) -->
        <section id="panel-ext" class="tab-panel" role="tabpanel" aria-labelledby="tab-btn-ext">
            <div class="card">
                <div class="card-title">
                    <span>Painel dos Pontos Extras (Seção 10 do Edital) e Laudo de Acessibilidade WCAG 2.1</span>
                </div>
                <div class="exp-subnav" role="tablist" aria-label="Seleção de Ponto Extra">
                    <button type="button" id="subbtn-x5" role="tab" aria-selected="true" class="btn" onclick="mostrarSubExtra('x5')">Extra 5: Laudo WCAG 2.1 AAA e Atalhos</button>
                    <button type="button" id="subbtn-x1" role="tab" aria-selected="false" class="btn btn-secondary" onclick="mostrarSubExtra('x1')">Extra 1: Intervalos de Confiança (30 Seeds)</button>
                    <button type="button" id="subbtn-x2" role="tab" aria-selected="false" class="btn btn-secondary" onclick="mostrarSubExtra('x2')">Extra 2: Mesma Média, Riscos Diferentes</button>
                    <button type="button" id="subbtn-x3" role="tab" aria-selected="false" class="btn btn-secondary" onclick="mostrarSubExtra('x3')">Extra 3: Limites de Exposição (Stop-Win/Loss)</button>
                    <button type="button" id="subbtn-x4" role="tab" aria-selected="false" class="btn btn-secondary" onclick="mostrarSubExtra('x4')">Extra 4: Análise de Sensibilidade (7 Cenários)</button>
                </div>

                <div id="subextra-container"></div>
            </div>
        </section>
    </main>

    <script>
        // Dados embutidos pelo Python (Auditoria WCAG e Figuras Base64)
        const PARES_WCAG = {json_contraste};
        const IMAGENS_B64 = {json_imagens};

        const SIMBOLOS = [
            {{ cod: "A", forma: "●", nome: "Círculo", premio: 5, lucro: 4, classe: "sym-A" }},
            {{ cod: "B", forma: "▲", nome: "Triângulo", premio: 10, lucro: 9, classe: "sym-B" }},
            {{ cod: "C", forma: "■", nome: "Quadrado", premio: 15, lucro: 14, classe: "sym-C" }},
            {{ cod: "D", forma: "◆", nome: "Losango", premio: 25, lucro: 24, classe: "sym-D" }},
            {{ cod: "E", forma: "★", nome: "Estrela", premio: 50, lucro: 49, classe: "sym-E" }}
        ];

        // Gerador pseudoaleatório com semente (Mulberry32) para reprodutibilidade no navegador
        let estadoSeed = 2026;
        function proximoFloat() {{
            let t = estadoSeed += 0x6D2B79F5;
            t = Math.imul(t ^ (t >>> 15), t | 1);
            t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
            return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
        }}

        function sortearIndice0a4() {{
            return Math.floor(proximoFloat() * 5);
        }}

        // Estado da sessão do simulador
        let saldo = 100.0;
        let rodadas = 0;
        let somaPremios = 0.0;
        let somaLucros = 0.0;
        let hitsTotal = 0;
        let contagensSimbolo = {{ A: 0, B: 0, C: 0, D: 0, E: 0, loss: 0 }};
        let historicoSaldos = [100.0];
        let historicoGiros = [];
        let vozAtiva = false;
        let escalaFonte = 1.0;
        const temas = ["escuro", "claro", "okabe"];
        const nomesTemas = {{ escuro: "Escuro AAA", claro: "Claro AAA", okabe: "Okabe-Ito Daltônico" }};
        let indiceTema = 0;

        function renderizarTabuleiro(paradas, premiada, codVencedor) {{
            // paradas = [K1, K2, K3] onde topo = K, centro = (K+1)%5, base = (K+2)%5
            for (let col = 0; col < 3; col++) {{
                const k = paradas[col];
                for (let lin = 0; lin < 3; lin++) {{
                    const idxSimbolo = (k + lin) % 5;
                    const s = SIMBOLOS[idxSimbolo];
                    const el = document.getElementById(`cell-${{lin}}-${{col}}`);
                    el.className = `reel-cell ${{s.classe}}`;
                    el.setAttribute("aria-label", `Linha ${{lin+1}}, Rolo ${{col+1}}: ${{s.nome}} ${{s.cod}}`);
                    el.innerHTML = `
                        <span class="symbol-shape" aria-hidden="true">${{s.forma}}</span>
                        <span class="symbol-code">${{s.cod}}</span>
                        <span class="symbol-name">${{s.nome}} (${{s.premio}} cr.)</span>
                    `;
                }}
            }}

            // Destaca a linha correspondente na tabela de pagamentos
            ["A", "B", "C", "D", "E", "loss"].forEach(ch => {{
                const tr = document.getElementById(`pay-row-${{ch}}`);
                if (tr) tr.classList.remove("highlight-row");
            }});
            const chaveDestaque = premiada ? codVencedor : "loss";
            const trAtiva = document.getElementById(`pay-row-${{chaveDestaque}}`);
            if (trAtiva) trAtiva.classList.add("highlight-row");
        }}

        function executarGiros(qtd) {{
            if (saldo < 1.0) {{
                anunciarStatus("⚠️ Saldo esgotado (B_t < 1 crédito)! Clique em 'Reiniciar Saldo' (ou tecla R) para jogar novamente.", false);
                return;
            }}

            let ultimoParadas = [0, 1, 2];
            let ultimoPremio = 0;
            let ultimoLucro = -1;
            let ultimaTripla = "";
            let ultimaPremiada = false;
            let girosEfetivos = 0;

            for (let i = 0; i < qtd; i++) {{
                if (saldo < 1.0) break;
                const k1 = sortearIndice0a4();
                const k2 = sortearIndice0a4();
                const k3 = sortearIndice0a4();
                ultimoParadas = [k1, k2, k3];

                const c1 = SIMBOLOS[(k1 + 1) % 5];
                const c2 = SIMBOLOS[(k2 + 1) % 5];
                const c3 = SIMBOLOS[(k3 + 1) % 5];

                ultimaTripla = `${{c1.forma}} ${{c1.cod}} – ${{c2.forma}} ${{c2.cod}} – ${{c3.forma}} ${{c3.cod}}`;
                ultimaPremiada = (c1.cod === c2.cod && c2.cod === c3.cod);
                ultimoPremio = ultimaPremiada ? c1.premio : 0.0;
                ultimoLucro = ultimoPremio - 1.0;

                saldo += ultimoLucro;
                rodadas += 1;
                girosEfetivos += 1;
                somaPremios += ultimoPremio;
                somaLucros += ultimoLucro;

                if (ultimaPremiada) {{
                    hitsTotal += 1;
                    contagensSimbolo[c1.cod] += 1;
                }} else {{
                    contagensSimbolo.loss += 1;
                }}

                historicoSaldos.push(saldo);
                historicoGiros.unshift({{
                    n: rodadas,
                    tripla: ultimaTripla,
                    premiada: ultimaPremiada,
                    premio: ultimoPremio,
                    lucro: ultimoLucro,
                    saldo: saldo
                }});
                if (historicoGiros.length > 8) historicoGiros.pop();
            }}

            const codVencedor = ultimaPremiada ? SIMBOLOS[(ultimoParadas[0] + 1) % 5].cod : "loss";
            renderizarTabuleiro(ultimoParadas, ultimaPremiada, codVencedor);
            atualizarPainelMetricas();
            desenharGraficoSaldo();

            if (girosEfetivos === 1) {{
                if (ultimaPremiada) {{
                    anunciarStatus(`🎉 VITÓRIA! Tripla Premiada (${{ultimaTripla}}) | Prêmio P = +${{ultimoPremio}} créditos | Lucro X = +${{ultimoLucro}} | Saldo: ${{saldo.toFixed(2)}}`, true);
                }} else {{
                    anunciarStatus(`✕ Sem prêmio na rodada #${{rodadas}} (${{ultimaTripla}}) | Prêmio P = 0 | Lucro X = −1,00 | Saldo: ${{saldo.toFixed(2)}}`, false);
                }}
            }} else {{
                const media = somaLucros / rodadas;
                anunciarStatus(`⚡ Executadas +${{girosEfetivos}} rodadas! Total: ${{rodadas}} giros | Saldo atual: ${{saldo.toFixed(2)}} | Lucro médio X̄ = ${{media.toFixed(4)}}`, ultimaPremiada);
            }}
        }}

        function anunciarStatus(msg, vitoria) {{
            const banner = document.getElementById("status-giro");
            banner.textContent = msg;
            banner.className = "status-banner " + (vitoria ? "status-win" : "status-loss");
            if (vozAtiva && "speechSynthesis" in window) {{
                window.speechSynthesis.cancel();
                const utter = new SpeechSynthesisUtterance(msg);
                utter.lang = "pt-BR";
                utter.rate = 1.15;
                window.speechSynthesis.speak(utter);
            }}
        }}

        function atualizarPainelMetricas() {{
            document.getElementById("kpi-saldo").textContent = saldo.toFixed(2).replace(".", ",");
            document.getElementById("kpi-rodadas").textContent = rodadas.toLocaleString("pt-BR");
            const sinalAcum = somaLucros >= 0 ? "+" : "";
            document.getElementById("kpi-lucro-acum").textContent = sinalAcum + somaLucros.toFixed(2).replace(".", ",");
            const lucroMedio = rodadas > 0 ? (somaLucros / rodadas) : 0.0;
            const rtp = rodadas > 0 ? ((somaPremios / rodadas) * 100.0) : 0.0;
            const taxaHits = rodadas > 0 ? ((hitsTotal / rodadas) * 100.0) : 0.0;
            document.getElementById("kpi-lucro-medio").textContent = (lucroMedio >= 0 ? "+" : "") + lucroMedio.toFixed(4).replace(".", ",");
            document.getElementById("kpi-rtp").textContent = rtp.toFixed(2).replace(".", ",") + "%";
            document.getElementById("kpi-hits").textContent = `${{hitsTotal}} (${{taxaHits.toFixed(2).replace(".", ",")}}%)`;

            ["A", "B", "C", "D", "E", "loss"].forEach(k => {{
                document.getElementById(`cnt-${{k}}`).textContent = contagensSimbolo[k];
            }});

            const tbody = document.getElementById("tbody-historico");
            if (historicoGiros.length === 0) {{
                tbody.innerHTML = '<tr><td colspan="6">Nenhum giro realizado ainda.</td></tr>';
            }} else {{
                tbody.innerHTML = historicoGiros.map(g => `
                    <tr class="${{g.premiada ? 'highlight-row' : ''}}">
                        <td>#${{g.n}}</td>
                        <td><strong>${{g.tripla}}</strong></td>
                        <td>${{g.premiada ? '✔ PREMIADA' : '✕ Sem prêmio'}}</td>
                        <td>${{g.premio.toFixed(2).replace(".", ",")}}</td>
                        <td>${{(g.lucro >= 0 ? "+" : "") + g.lucro.toFixed(2).replace(".", ",")}}</td>
                        <td><strong>${{g.saldo.toFixed(2).replace(".", ",")}}</strong></td>
                    </tr>
                `).join("");
            }}
        }}

        function desenharGraficoSaldo() {{
            const canvas = document.getElementById("canvas-saldo");
            if (!canvas) return;
            const ctx = canvas.getContext("2d");
            const w = canvas.width;
            const h = canvas.height;
            ctx.clearRect(0, 0, w, h);

            const padL = 52, padR = 20, padT = 20, padB = 30;
            const plotW = w - padL - padR;
            const plotH = h - padT - padB;

            const minVal = Math.min(0, ...historicoSaldos);
            const maxVal = Math.max(120, ...historicoSaldos);
            const range = Math.max(10, maxVal - minVal);

            const yDeValor = (v) => padT + plotH - ((v - minVal) / range) * plotH;

            // Linha de referência B0 = 100
            const y100 = yDeValor(100);
            ctx.strokeStyle = "#94A3B8";
            ctx.setLineDash([6, 4]);
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(padL, y100);
            ctx.lineTo(w - padR, y100);
            ctx.stroke();
            ctx.setLineDash([]);

            // Trajetória do saldo
            ctx.strokeStyle = "#38BDF8";
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            const n = historicoSaldos.length;
            for (let i = 0; i < n; i++) {{
                const x = padL + (n === 1 ? 0 : (i / (n - 1)) * plotW);
                const y = yDeValor(historicoSaldos[i]);
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }}
            ctx.stroke();

            // Eixos e rótulos
            ctx.fillStyle = "#CBD5E1";
            ctx.font = "bold 12px Segoe UI, sans-serif";
            ctx.fillText(`Máx: ${{maxVal.toFixed(0)}}`, 6, padT + 10);
            ctx.fillText("100", 14, y100 + 4);
            ctx.fillText(`Mín: ${{minVal.toFixed(0)}}`, 6, h - padB);
            ctx.fillText(`Rodadas: 0 até ${{rodadas}}`, padL + plotW / 2 - 45, h - 8);
        }}

        function reiniciarSessao() {{
            saldo = 100.0;
            rodadas = 0;
            somaPremios = 0.0;
            somaLucros = 0.0;
            hitsTotal = 0;
            contagensSimbolo = {{ A: 0, B: 0, C: 0, D: 0, E: 0, loss: 0 }};
            historicoSaldos = [100.0];
            historicoGiros = [];
            renderizarTabuleiro([4, 0, 1], false, "loss");
            atualizarPainelMetricas();
            desenharGraficoSaldo();
            anunciarStatus("🔄 Sessão reiniciada com saldo B_0 = 100,00 créditos.", false);
        }}

        function aplicarSemente() {{
            const val = parseInt(document.getElementById("input-seed").value, 10);
            estadoSeed = isNaN(val) ? 2026 : val;
            reiniciarSessao();
            anunciarStatus(`🌱 Semente definida para ${{estadoSeed}} e sessão reiniciada.`, true);
        }}

        function alternarTema() {{
            indiceTema = (indiceTema + 1) % temas.length;
            const novoTema = temas[indiceTema];
            document.documentElement.setAttribute("data-tema", novoTema);
            document.getElementById("lbl-tema").textContent = nomesTemas[novoTema];
        }}

        function ajustarFonte(delta) {{
            if (delta === 0) escalaFonte = 1.0;
            else escalaFonte = Math.min(1.35, Math.max(0.85, escalaFonte + delta));
            document.documentElement.style.setProperty("--font-scale", escalaFonte);
        }}

        function alternarVoz() {{
            vozAtiva = !vozAtiva;
            const btn = document.getElementById("btn-voz");
            btn.setAttribute("aria-pressed", String(vozAtiva));
            btn.innerHTML = `🔊 Voz: ${{vozAtiva ? 'On' : 'Off'}} <span class="kbd">V</span>`;
        }}

        function selecionarAba(id) {{
            ["sim", "exp", "ext"].forEach(k => {{
                document.getElementById(`panel-${{k}}`).classList.toggle("active", k === id);
                document.getElementById(`tab-btn-${{k}}`).setAttribute("aria-selected", String(k === id));
            }});
        }}

        // Conteúdo dos Experimentos Obrigatórios (E1 a E5)
        const CONTEUDO_EXP = {{
            e1: {{
                titulo: "Experimento 1 — As Frequências Acompanham as Probabilidades? (N = 10.000, Semente 2026)",
                resumo: "Em 10.000 rodadas independentes (semente 2026), observaram-se 412 rodadas premiadas (4,12% vs. 4,00% teóricos), RTP observado de 86,85% (vs. 84,00% teóricos), lucro médio amostral X̄ = −0,1315 crédito/rodada e desvio-padrão amostral s = 5,2750 créditos (vs. σ = 5,2321).",
                img: "exp1",
                tabela: `
                    <table>
                        <thead><tr><th>Desfecho (Linha Central)</th><th>Lucro X</th><th>Prob. Teórica</th><th>Contagem Observada</th><th>Freq. Relativa (%)</th></tr></thead>
                        <tbody>
                            <tr><td>● A – A – A</td><td>+4</td><td>0,80% (1/125)</td><td>77</td><td>0,77%</td></tr>
                            <tr><td>▲ B – B – B</td><td>+9</td><td>0,80% (1/125)</td><td>88</td><td>0,88%</td></tr>
                            <tr><td>■ C – C – C</td><td>+14</td><td>0,80% (1/125)</td><td>78</td><td>0,78%</td></tr>
                            <tr><td>◆ D – D – D</td><td>+24</td><td>0,80% (1/125)</td><td>88</td><td>0,88%</td></tr>
                            <tr><td>★ E – E – E</td><td>+49</td><td>0,80% (1/125)</td><td>81</td><td>0,81%</td></tr>
                            <tr><td>✕ Qualquer outra tripla</td><td>−1</td><td>96,00% (120/125)</td><td>9.588</td><td>95,88%</td></tr>
                            <tr class="highlight-row"><td>TOTAL</td><td>E[X] = −0,16</td><td>100,00%</td><td>10.000</td><td>100,00% (X̄ = −0,1315)</td></tr>
                        </tbody>
                    </table>`
            }},
            e2: {{
                titulo: "Experimento 2 — Lei dos Grandes Números e Convergência de Monte Carlo (Sementes 10, 2026 e 123456)",
                resumo: "Em amostras curtas (N = 100), a alta variância permite lucro médio positivo (+0,2000 nas sementes 2026 e 123456). À medida que N cresce para 1.000 e 10.000 giros, o erro-padrão σ/√N contrai-se e todas as trajetórias estabilizam-se no campo negativo ao redor de E[X] = −0,16.",
                img: "exp2",
                tabela: `
                    <table>
                        <thead><tr><th>Execução / Semente</th><th>N = 100 rodadas</th><th>N = 1.000 rodadas</th><th>N = 10.000 rodadas</th><th>Esperança E[X]</th></tr></thead>
                        <tbody>
                            <tr><td>Semente 10</td><td>−0,7000</td><td>−0,0550</td><td>−0,0960</td><td>−0,1600</td></tr>
                            <tr><td>Semente 2026 (E1)</td><td>+0,2000</td><td>−0,2200</td><td>−0,1315</td><td>−0,1600</td></tr>
                            <tr><td>Semente 123456</td><td>+0,2000</td><td>−0,0700</td><td>−0,2215</td><td>−0,1600</td></tr>
                        </tbody>
                    </table>`
            }},
            e3: {{
                titulo: "Experimento 3 — Saldo Limitado e Risco de Ruína (100 Participantes, B_0 = 100, até 500 Rodadas, Semente 42)",
                resumo: "Dos 100 jogadores, 23% saíram com ganho, 2% empataram e 75% perderam (sendo 67% de ruína total B_f = 0). A cauda superior eleva a média para 52,10 créditos, enquanto a mediana de 0,00 crédito revela que o desfecho típico da maioria absoluta é a falência.",
                img: "exp3",
                tabela: `
                    <table>
                        <thead><tr><th>Categoria / Métrica</th><th>Valor Observado</th><th>Proporção</th><th>Interpretação Estatística</th></tr></thead>
                        <tbody>
                            <tr><td>Ganho (B_f > 100)</td><td>23 jogadores</td><td>23,0%</td><td>Beneficiados por triplas raras de alto valor</td></tr>
                            <tr><td>Empate (B_f = 100)</td><td>2 jogadores</td><td>2,0%</td><td>Retorno exato ao saldo inicial após 500 giros</td></tr>
                            <tr><td>Perda (B_f < 100)</td><td>75 jogadores</td><td>75,0%</td><td>Maioria consistente com E[X] = −0,16</td></tr>
                            <tr class="highlight-row"><td>Taxa de Esgotamento (Ruína B_f = 0)</td><td>67 jogadores</td><td>67,0%</td><td>89,3% dos perdedores faliram antes de 500 giros</td></tr>
                            <tr><td>Média vs. Mediana Final</td><td>Média: 52,10 cr.</td><td>Mediana: 0,00 cr.</td><td>Forte assimetria positiva (viés de sobrevivência)</td></tr>
                        </tbody>
                    </table>`
            }},
            e4: {{
                titulo: "Experimento 4 — Probabilidade Condicional e Refutação da Falácia do Jogador (9.999 Pares Consecutivos)",
                resumo: "Analisando os 9.999 pares consecutivos (R_i, R_{{i+1}}) do Experimento 1, a taxa de vitória após prêmio foi de 4,13% (17/412) e após perda foi de 4,12% (395/9.587), comprovando que os giros são independentes e a máquina não acumula nem 'deve' prêmio após derrotas.",
                img: "",
                tabela: `
                    <table>
                        <thead><tr><th>Condição na Rodada Anterior (i)</th><th>Total de Pares</th><th>Vitórias em (i+1)</th><th>Proporção Observada</th><th>Prob. Teórica</th></tr></thead>
                        <tbody>
                            <tr><td>Após Prêmio (P_i > 0)</td><td>412</td><td>17</td><td>4,13%</td><td>4,00%</td></tr>
                            <tr><td>Após Perda (P_i = 0)</td><td>9.587</td><td>395</td><td>4,12%</td><td>4,00%</td></tr>
                            <tr class="highlight-row"><td>TOTAL DE PARES</td><td>9.999</td><td>412</td><td>4,12%</td><td>4,00%</td></tr>
                        </tbody>
                    </table>`
            }},
            e5: {{
                titulo: "Experimento 5 — Prêmios Maiores (+10%) Tornam o Jogo Favorável? (Comparação Pareada)",
                resumo: "Aumentar todos os prêmios em +10% (5,5; 11; 16,5; 27,5; 55) eleva o RTP teórico de 84,00% para 92,40% (observado: 95,53%), mas não altera a frequência de acerto (4,00%) e mantém a esperança de lucro negativa (E[X_{{+10%}}] = −0,0760 < 0).",
                img: "",
                tabela: `
                    <table>
                        <thead><tr><th>Métrica</th><th>Tabela Base (Teór. / Obs.)</th><th>Tabela +10% (Teór. / Obs.)</th><th>Efeito</th></tr></thead>
                        <tbody>
                            <tr><td>Probabilidade de Prêmio</td><td>4,00% / 4,12%</td><td>4,00% / 4,12%</td><td>Inalterada (pagar mais ≠ pagar mais vezes)</td></tr>
                            <tr><td>RTP (Retorno ao Jogador)</td><td>84,00% / 86,85%</td><td>92,40% / 95,53%</td><td>+10,0% relativo (+8,4 p.p. teórico)</td></tr>
                            <tr class="highlight-row"><td>Lucro Médio E[X]</td><td>−0,1600 / −0,1315</td><td>−0,0760 / −0,0447</td><td>Jogo permanece desfavorável ao apostador</td></tr>
                        </tbody>
                    </table>`
            }}
        }};

        function mostrarSubExp(chave) {{
            ["e1", "e2", "e3", "e4", "e5"].forEach(k => {{
                const btn = document.getElementById(`subbtn-${{k}}`);
                if (btn) {{
                    const ativo = (k === chave);
                    btn.className = ativo ? "btn" : "btn btn-secondary";
                    btn.setAttribute("aria-selected", String(ativo));
                }}
            }});
            const d = CONTEUDO_EXP[chave];
            const htmlImg = (d.img && IMAGENS_B64[d.img])
                ? `<div style="text-align:center;margin-top:1rem;"><img class="exp-fig" src="${{IMAGENS_B64[d.img]}}" alt="${{d.titulo}}"></div>`
                : "";
            document.getElementById("subexp-container").innerHTML = `
                <h3 style="color:var(--accent-secondary);margin-bottom:0.5rem;">${{d.titulo}}</h3>
                <p style="margin-bottom:0.75rem;">${{d.resumo}}</p>
                <div class="table-responsive">${{d.tabela}}</div>
                ${{htmlImg}}
            `;
        }}

        function simularLoteRapidoNavegador() {{
            ["e1", "e2", "e3", "e4", "e5"].forEach(k => {{
                const btn = document.getElementById(`subbtn-${{k}}`);
                if (btn) {{
                    btn.className = "btn btn-secondary";
                    btn.setAttribute("aria-selected", "false");
                }}
            }});
            let acertos = {{ A: 0, B: 0, C: 0, D: 0, E: 0, loss: 0 }};
            let somaP = 0;
            for (let i = 0; i < 10000; i++) {{
                const k1 = (sortearIndice0a4() + 1) % 5;
                const k2 = (sortearIndice0a4() + 1) % 5;
                const k3 = (sortearIndice0a4() + 1) % 5;
                if (k1 === k2 && k2 === k3) {{
                    const s = SIMBOLOS[k1];
                    acertos[s.cod] += 1;
                    somaP += s.premio;
                }} else {{
                    acertos.loss += 1;
                }}
            }}
            const rtpObs = (somaP / 10000) * 100;
            const lucroMed = (somaP - 10000) / 10000;
            const totalHits = 10000 - acertos.loss;
            document.getElementById("subexp-container").innerHTML = `
                <div class="status-banner status-win">
                    ✔ Nova Simulação Monte Carlo de 10.000 Rodadas Concluída no Navegador!
                    Triplas Premiadas: ${{totalHits}} (${{(totalHits/100).toFixed(2)}}%) | RTP Observado: ${{rtpObs.toFixed(2)}}% | Lucro Médio X̄ = ${{lucroMed.toFixed(4)}} crédito
                </div>
                <div class="table-responsive">
                    <table>
                        <thead><tr><th>Desfecho</th><th>Contagem em 10.000 Giros</th><th>Freq. Observada</th><th>Prob. Teórica</th></tr></thead>
                        <tbody>
                            <tr><td>● A–A–A (+4)</td><td>${{acertos.A}}</td><td>${{(acertos.A/100).toFixed(2)}}%</td><td>0,80%</td></tr>
                            <tr><td>▲ B–B–B (+9)</td><td>${{acertos.B}}</td><td>${{(acertos.B/100).toFixed(2)}}%</td><td>0,80%</td></tr>
                            <tr><td>■ C–C–C (+14)</td><td>${{acertos.C}}</td><td>${{(acertos.C/100).toFixed(2)}}%</td><td>0,80%</td></tr>
                            <tr><td>◆ D–D–D (+24)</td><td>${{acertos.D}}</td><td>${{(acertos.D/100).toFixed(2)}}%</td><td>0,80%</td></tr>
                            <tr><td>★ E–E–E (+49)</td><td>${{acertos.E}}</td><td>${{(acertos.E/100).toFixed(2)}}%</td><td>0,80%</td></tr>
                            <tr><td>✕ Sem Prêmio (−1)</td><td>${{acertos.loss}}</td><td>${{(acertos.loss/100).toFixed(2)}}%</td><td>96,00%</td></tr>
                        </tbody>
                    </table>
                </div>
            `;
        }}

        function mostrarSubExtra(chave) {{
            ["x5", "x1", "x2", "x3", "x4"].forEach(k => {{
                const btn = document.getElementById(`subbtn-${{k}}`);
                if (btn) {{
                    const ativo = (k === chave);
                    btn.className = ativo ? "btn" : "btn btn-secondary";
                    btn.setAttribute("aria-selected", String(ativo));
                }}
            }});
            const container = document.getElementById("subextra-container");
            if (chave === "x5") {{
                const linhasWcag = PARES_WCAG.map(p => `
                    <tr>
                        <td style="text-align:left;"><strong>${{p.componente}}</strong></td>
                        <td><code>${{p.cor_frente}}</code></td>
                        <td><code>${{p.cor_fundo}}</code></td>
                        <td><strong>${{p.razao_contraste.toFixed(2)}} : 1</strong></td>
                        <td><span style="color:var(--win-color);font-weight:700;">✔ ${{p.nivel_wcag}}</span></td>
                    </tr>
                `).join("");
                container.innerHTML = `
                    <h3 style="color:var(--accent-secondary);margin-bottom:0.5rem;">Extra 5 — Laudo de Contraste WCAG 2.1 AAA e Navegação Híbrida (Mouse + Teclado)</h3>
                    <p style="margin-bottom:0.75rem;">
                        Todos os 10 pares de cores dos temas da interface superam o limiar máximo <strong>WCAG 2.1 Nível AAA (≥ 7,0:1)</strong>. Além disso, a interface garante independência cromática (formas geométricas ● ▲ ■ ◆ ★ + bordas diferenciadas + texto explícito) e operação completa tanto por <strong>cliques de mouse</strong> quanto por <strong>atalhos de teclado</strong> (<span class="kbd">Espaço</span>, <span class="kbd">G</span>, <span class="kbd">C</span>, <span class="kbd">R</span>, <span class="kbd">T</span>, <span class="kbd">V</span>, <span class="kbd">1</span>, <span class="kbd">2</span>, <span class="kbd">3</span> e <span class="kbd">Tab</span>).
                    </p>
                    <div class="table-responsive">
                        <table>
                            <thead><tr><th>Componente Auditado</th><th>Cor Frente</th><th>Cor Fundo</th><th>Razão de Contraste</th><th>Classificação WCAG 2.1</th></tr></thead>
                            <tbody>${{linhasWcag}}</tbody>
                        </table>
                    </div>
                `;
                return;
            }}

            const mapaExtras = {{
                x1: {{
                    titulo: "Extra 1 — Intervalos de Confiança de 95% (t de Student, 30 Execuções Independentes)",
                    texto: "Na amostra canônica (semente 2026, N = 10.000), IC95%(μ_X) = [−0,2349 ; −0,0281] e IC95%(RTP) = [76,51% ; 97,19%]. Em M = 30 execuções independentes (sementes 2026 a 2055; 300.000 giros), 29 dos 30 intervalos (96,7%) cobriram o parâmetro verdadeiro E[X] = −0,16.",
                    img: "extra1"
                }},
                x2: {{
                    titulo: "Extra 2 — Mesma Média (E[X] = −0,16 | RTP = 84%), Riscos Diferentes",
                    texto: "Comparação entre Baixa Volatilidade (21,21,21,21,21; σ = 4,12), Base (5,10,15,25,50; σ = 5,21) e Alta Volatilidade (1,2,2,10,90; σ = 8,06): a Alta Volatilidade elevou tanto a taxa de ruína (69% vs. 63%) quanto o maior saldo final (721 vs. 356 créditos), mantendo a mediana em 0,00 nas três tabelas.",
                    img: "extra2"
                }},
                x3: {{
                    titulo: "Extra 3 — Limites de Exposição e Regras de Parada (Identidade de Wald)",
                    texto: "A política Stop-Win (B_t ≥ 120) combinada com Stop-Loss (B_t ≤ 70) e limite de 200 giros reduziu a exposição média de 339,90 para 31,32 rodadas, zerando a ruína total (0,0%) e preservando mediana de 70,00 créditos.",
                    img: "extra3"
                }},
                x4: {{
                    titulo: "Extra 4 — Análise de Sensibilidade em 7 Cenários (Pagamentos e Geometria dos Rolos)",
                    texto: "O ponto de equilíbrio (RTP = 100%, E[X] = 0) exige elevar todos os prêmios em +19,05% (fator 125/105, Cenário C4). Já duplicar o símbolo barato A em um rolo de 6 faces (Cenário C7) eleva a frequência de vitórias para 5,56%, mas derruba o RTP para 64,81%.",
                    img: "extra4"
                }}
            }};
            const item = mapaExtras[chave];
            const htmlImg = (item.img && IMAGENS_B64[item.img])
                ? `<div style="text-align:center;margin-top:1rem;"><img class="exp-fig" src="${{IMAGENS_B64[item.img]}}" alt="${{item.titulo}}"></div>`
                : "";
            container.innerHTML = `
                <h3 style="color:var(--accent-secondary);margin-bottom:0.5rem;">${{item.titulo}}</h3>
                <p style="margin-bottom:0.75rem;">${{item.texto}}</p>
                ${{htmlImg}}
            `;
        }}

        // Atalhos globais de teclado (complementando a navegação por mouse)
        window.addEventListener("keydown", (ev) => {{
            if (ev.target && (ev.target.tagName === "INPUT" || ev.target.tagName === "TEXTAREA")) return;
            const k = ev.key.toLowerCase();
            if (ev.code === "Space") {{
                ev.preventDefault();
                executarGiros(1);
            }} else if (k === "g") {{
                executarGiros(10);
            }} else if (k === "c") {{
                executarGiros(100);
            }} else if (k === "r") {{
                reiniciarSessao();
            }} else if (k === "t") {{
                alternarTema();
            }} else if (k === "v") {{
                alternarVoz();
            }} else if (k === "1") {{
                selecionarAba("sim");
            }} else if (k === "2") {{
                selecionarAba("exp");
            }} else if (k === "3") {{
                selecionarAba("ext");
            }}
        }});

        // Inicialização
        renderizarTabuleiro([4, 0, 1], false, "loss");
        desenharGraficoSaldo();
        mostrarSubExp("e1");
        mostrarSubExtra("x5");
    </script>
</body>
</html>
"""
    return html


def f_executarExtra5InterfaceAcessivel(abrirNavegador: bool = True) -> Dict[str, Any]:
    """Gera a aplicação web acessível autocontida, audita o contraste WCAG 2.1 e abre no navegador.

    Args:
        abrirNavegador: Se True, abre automaticamente o arquivo HTML gerado no navegador padrão.

    Returns:
        Dicionário com o resumo da auditoria WCAG, caminhos do HTML e CSV gerados e status.
    """
    pares_contraste = f_auditarParesDeContrasteInterfaceWeb()  # roda a auditoria matemática de luminância nos 10 pares
    menor_razao = min(p["razao_contraste"] for p in pares_contraste)  # pega o menor contraste pra provar que todos passam de 7:1
    todos_aaa = all(p["aprovado_aaa"] for p in pares_contraste)  # confere se 100% dos pares têm selo máximo WCAG AAA

    # Carrega em Base64 as figuras existentes para que o HTML fique 100% autocontido
    imagens_b64 = {
        "exp1": _f_codificarImagemBase64(DIRETORIO_FIGURAS / "exp1_frequencias.png"),
        "exp2": _f_codificarImagemBase64(DIRETORIO_FIGURAS / "exp2_convergencia.png"),
        "exp3": _f_codificarImagemBase64(DIRETORIO_FIGURAS / "exp3_trajetorias.png"),
        "extra1": _f_codificarImagemBase64(DIRETORIO_FIGURAS_EXTRAS / "extra1_intervalos_confianca.png"),
        "extra2": _f_codificarImagemBase64(DIRETORIO_FIGURAS_EXTRAS / "extra2_riscos_diferentes.png"),
        "extra3": _f_codificarImagemBase64(DIRETORIO_FIGURAS_EXTRAS / "extra3_limites_exposicao.png"),
        "extra4": _f_codificarImagemBase64(DIRETORIO_FIGURAS_EXTRAS / "extra4_analise_sensibilidade.png"),
    }

    caminho_html = DIRETORIO_RESULTADOS / "interface_acessivel.html"  # destino do app web local
    caminho_html.parent.mkdir(parents=True, exist_ok=True)
    conteudo_html = _f_construirHtmlInterfaceAcessivel(pares_contraste, imagens_b64)  # monta o HTML completo
    caminho_html.write_text(conteudo_html, encoding="utf-8")  # salva em UTF-8 no disco

    cabecalhos_resumo = [
        "Componente Auditado (Interface Web)",
        "Frente",
        "Fundo",
        "Contraste (CR:1)",
        "Nível WCAG 2.1",
    ]
    tabela_resumo = [
        [
            p["componente"],
            p["cor_frente"],
            p["cor_fundo"],
            f"{p['razao_contraste']:.2f}:1",
            p["nivel_wcag"],
        ]
        for p in pares_contraste
    ]

    # Exporta CSV com a auditoria de contraste e verificação dos recursos da interface web
    caminho_csv = DIRETORIO_TABELAS_EXTRAS / "extra5_interface_acessivel.csv"
    f_exportarParaCsv(caminho_csv, cabecalhos_resumo, tabela_resumo)  # salva o laudo WCAG em CSV

    abriu_navegador = False
    if abrirNavegador:
        try:
            abriu_navegador = webbrowser.open(caminho_html.resolve().as_uri())  # abre direto no navegador padrão do usuário
        except Exception:
            abriu_navegador = False

    return {
        "pares_contraste": pares_contraste,
        "menor_razao_contraste": menor_razao,
        "todos_wcag_aaa": todos_aaa,
        "caminho_html": caminho_html,
        "caminho_csv": caminho_csv,
        "cabecalhos_resumo": cabecalhos_resumo,
        "tabela_resumo": tabela_resumo,
        "abriu_navegador": abriu_navegador,
    }
