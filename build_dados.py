# -*- coding: utf-8 -*-
"""
Consolida os dados do novo Painel NV2026:
  1. DADOS  - 59 maternidades estratégicas (blocos SINASC) extraídos do painel antigo
              + coordenadas lat/lon dos CSVs GEO (Volume de partos Maio26)
  2. GEO    - polígonos compactados (uf / macro / rs) da página de referência (somente leitura)
  3. PONTOS - todos os estabelecimentos com partos (contexto no mapa), com CNES, nome,
              lat/lon, UF, macrorregião e volume anual de partos

Saída: dados_nv2026.js (const GEO / DADOS / PONTOS prontos para embutir no HTML)
"""
import re, json, csv, glob, os, sys, unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(BASE)
DOCS = os.path.dirname(PROJ)

PAINEL_ANTIGO = os.path.join(PROJ, "Apresentacoes_2026_NovoTemplate", "Painel_NV2026.html")
REF_PAGE      = os.path.join(DOCS, "Indicadores Partos", "index.html")   # leitura apenas
CSV_GEO_DIR   = os.path.join(DOCS, "Volume de partos Maio26", "Planilhas com GEO")

def norm(s):
    s = unicodedata.normalize("NFD", str(s or ""))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").upper().strip()

# ---------- 1. DADOS do painel antigo ----------
html = open(PAINEL_ANTIGO, encoding="utf-8").read()
m = re.search(r'const DADOS =\n(\{.*?\})\n;', html, re.S)
dados = json.loads(m.group(1))
mats = dados["maternidades"]
for mt in mats:                      # nomes sem travessão (padrão tipográfico do painel)
    mt["nome"] = mt["nome"].replace("—", "-")
print(f"[1] {len(mats)} maternidades extraídas do painel antigo")

# ---------- 2. pontos com coordenadas ----------
pontos = {}
for f in glob.glob(os.path.join(CSV_GEO_DIR, "*_GEO.csv")):
    uf = re.search(r'[_\s-]([A-Z]{2})_GEO\.csv$', os.path.basename(f)).group(1)
    with open(f, encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            c = str(row.get("CNES", "")).strip()
            lat, lon = row.get("LATITUDE"), row.get("LONGITUDE")
            if not (c and lat and lon):
                continue
            try:
                total = float(row.get("TOTAL") or 0)
            except ValueError:
                total = 0
            pontos[c] = {
                "cnes": c,
                "nome": (row.get("NOME_LIMPO") or "").title(),
                "uf": uf,
                "mun": (row.get("MUNICÍPIO") or row.get("MUNICIPIO_API") or "").title(),
                "macro": row.get("MACRO") or "",
                "lat": round(float(lat), 5),
                "lon": round(float(lon), 5),
                "partos": int(total),
            }
print(f"[2] {len(pontos)} estabelecimentos com coordenadas")

# coordenadas nas maternidades estratégicas
sem = []
for mt in mats:
    p = pontos.get(mt["cnes"])
    if p:
        mt["lat"], mt["lon"] = p["lat"], p["lon"]
        mt["partosAIH"] = p["partos"]
    else:
        sem.append(mt["nome"])
if sem:
    print("   ATENÇÃO — sem coordenada:", sem)
else:
    print("   todas as maternidades estratégicas têm lat/lon")

# ---------- 3. GEO compactado da referência ----------
ref = open(REF_PAGE, encoding="utf-8").read()
m = re.search(r'const GEO = (\{.*?\});', ref, re.S)
geo = json.loads(m.group(1))
print(f"[3] GEO: {', '.join(f'{k}={len(v)}' for k, v in geo['niveis'].items())}")

# ---------- 4. PONTOS de contexto (>=480 partos/ano, critério da apresentação) ----------
estrategicos = {mt["cnes"] for mt in mats}
contexto = [p for p in pontos.values()
            if p["partos"] >= 480 and p["cnes"] not in estrategicos]
contexto.sort(key=lambda p: -p["partos"])
print(f"[4] {len(contexto)} pontos de contexto (>=480 partos, não estratégicos)")

# ---------- 5. saída ----------
out = os.path.join(BASE, "dados_nv2026.js")
with open(out, "w", encoding="utf-8") as fh:
    fh.write("/* Gerado por build_dados.py — não editar à mão */\n")
    fh.write("const GEO = ")
    json.dump(geo, fh, ensure_ascii=False, separators=(",", ":"))
    fh.write(";\nconst DADOS = ")
    json.dump(dados, fh, ensure_ascii=False, separators=(",", ":"))
    fh.write(";\nconst PONTOS = ")
    json.dump(contexto, fh, ensure_ascii=False, separators=(",", ":"))
    fh.write(";\n")
print(f"[5] gravado {out} ({os.path.getsize(out)//1024} KB)")
