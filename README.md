# Painel NV 2026 · Maternidades Estratégicas

Painel interativo da Qualificação do Modelo de Gestão em Maternidades Estratégicas na Rede de
Atenção à Saúde Materna e Neonatal — Coordenação de Ações Nacionais e de Cooperação em Saúde da
Mulher, da Criança e do Adolescente (IFF/Fiocruz).

**Arquivo final:** `index.html` (idêntico a `Painel_NV2026_Novo.html`) — HTML único e autocontido,
pronto para GitHub Pages. Requer internet para os mapas de fundo (Leaflet/CARTO).

## O que o painel contém

- **Mapa do Brasil**: coroplético por UF, macrorregião ou região de saúde, com recorte + zoom,
  filtros em cascata (território → estado), faixas recalculadas por recorte e tooltip com as
  maternidades de cada território.
- **Mapa de unidades**: as 59 maternidades estratégicas (Leaflet), com filtros, busca e pontos de
  contexto (estabelecimentos ≥480 partos/ano, SIH/AIH 2025).
- **Dossiê da unidade**: página própria com ficha CNES e habilitações ativas (API oficial),
  todas as tabelas da apresentação (anos clicáveis abrem gráficos) e download em PDF.
- **Comparador**: entre unidades (2 a 4, por ano) e da mesma unidade entre anos (variação e
  tendência; variação clicável abre o gráfico).
- **Comparativo 2019 × 2024**: retenção de nascimentos no território de residência, todos os
  nascimentos (por região de saúde/macro/UF) e <1500 g (por macro/UF), dois mapas lado a lado.
- **Metodologia**: página própria com fontes oficiais e ficha de numerador/denominador de cada cálculo.

## Fontes

SINASC 2019–2025 (dados sujeitos a revisão) · CNES (ficha via API de Dados Abertos; habilitações
via serviço do site do CNES) · SIH/AIH 2025 · malhas de macrorregiões e regiões de saúde.

## Como atualizar

| O quê | Como |
|---|---|
| Ficha CNES + habilitações | `py atualizar_cnes.py` (agendado no Windows para 1º jun/dez) |
| Comparativo 2019×2024 | `py build_comparativo.py "planilha_macro.xlsx" "planilha_regiao.xlsx"` |
| Dados SINASC das unidades | `py build_dados.py` (extrai do painel anterior + coordenadas) |
| Remontar o painel | `py montar_painel.py` (gera `Painel_NV2026_Novo.html` e `index.html`) |

Atalho local: `atualizar_painel.bat` roda CNES + montagem e registra em `atualizacao_cnes.log`.

## Estrutura

- `painel_base.html` — estrutura e estilos (fonte editável)
- `painel_app.js` — lógica do painel (fonte editável)
- `dados_nv2026.js`, `cnes_dados.json`, `comparativo_nv.js` — dados gerados pelos scripts
- `foto_hero.jpg`, `logos_institucionais.png` — imagens embutidas na montagem
