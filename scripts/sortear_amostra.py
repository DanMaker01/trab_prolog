"""Sorteia a amostra de processos de tráfico a partir dos JSONs mensais de uma Turma do STJ.

Uso (na raiz do projeto):
  5ª Turma: python scripts/sortear_amostra.py fontes/json/*.json --n 40 --seed 2026 --manter-pre-condenacao
  6ª Turma: python scripts/sortear_amostra.py fontes/json/sexta_turma/*.json --n 40 --seed 2026 --saida dados/amostra_t6.csv
Saída: CSV com uma linha por processo, com a string de busca no site do STJ.

Regras do recorte:
  - ementa trata de tráfico (art. 33 da Lei 11.343/2006);
  - fica fora: EDcl (embargos de declaração), prisão cautelar, execução penal e
    pedidos de trancamento antes da condenação;
  - um processo entra uma vez só (fica o acórdão mais recente);
  - processos já estudados à mão (dados/casos.csv) não são sorteados de novo;
  - sorteio estratificado por relator (mesmo número por ministro, quando possível);
    relatores com poucos casos (< --min-relator) entram só no sorteio do restante;
    o nome do relator é normalizado (ex.: "ROGERIO SCHIETTI CRUZ" = "ROGERIO SCHIETTI").
"""
import argparse, csv, json, os, random, re, unicodedata

def norm(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().upper()
    return re.sub(r"\s+", " ", t)

def relator_norm(nome):
    """Normaliza o nome do relator: tira o cargo entre parênteses e usa os dois primeiros nomes."""
    n = norm(re.sub(r"\(.*?\)", "", nome or "")).strip()
    return " ".join(n.split()[:2])

def objeto(e):
    """Classifica do que trata a ementa (primeira tese que aparecer)."""
    if re.search(r"PRISAO PREVENTIVA|PRISAO DOMICILIAR|LIBERDADE PROVISORIA|MEDIDAS CAUTELARES|RECORRER EM LIBERDADE", e[:600]):
        return "cautelar"
    if re.search(r"EXECUCAO PENAL|PROGRESSAO DE REGIME|LIVRAMENTO CONDICIONAL|REMICAO", e[:600]):
        return "execucao"
    if re.search(r"TRANCAMENTO (DA|DO) (ACAO PENAL|INQUERITO)|RECEBIMENTO DA DENUNCIA", e[:600]):
        return "pre_condenacao"
    if re.search(r"BUSCA PESSOAL|BUSCA DOMICILIAR|BUSCA VEICULAR|INGRESSO (EM|NO) DOMICILIO|INVIOLABILIDADE|FUNDADA[S]? (SUSPEITA|RAZOES)|PROVA[S]? ILICITA", e):
        return "nulidade_busca"
    if re.search(r"33, ?§ ?4|TRAFICO PRIVILEGIADO|MINORANTE|CAUSA (ESPECIAL )?DE DIMINUICAO", e):
        return "p4"
    if re.search(r"DESCLASSIFICA|ART\. ?28|USO PESSOAL|CONSUMO PESSOAL", e):
        return "desclassificacao"
    if re.search(r"DOSIMETRIA|PENA-BASE|REGIME INICIAL|SUBSTITUICAO DA PENA", e):
        return "dosimetria"
    if re.search(r"ABSOLVI|AUTORIA|INSUFICIENCIA PROBATORIA", e):
        return "autoria"
    return "outro"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsons", nargs="+")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--ja-estudados", default=os.path.join("dados", "casos.csv"))
    ap.add_argument("--saida", default=os.path.join("dados", "amostra.csv"))
    ap.add_argument("--min-relator", type=int, default=20)
    ap.add_argument("--manter-pre-condenacao", action="store_true",
                    help="não exclui trancamento/pré-condenação (reproduz o sorteio da 5ª Turma, feito antes desse filtro)")
    a = ap.parse_args()

    ja = set()
    if os.path.exists(a.ja_estudados):
        for r in csv.DictReader(open(a.ja_estudados, encoding="utf-8")):
            ja.add(r["processo"].split()[-1])

    por_proc = {}
    for f in a.jsons:
        for x in json.load(open(f, encoding="utf-8")):
            classe = x.get("siglaClasse") or ""
            if classe.startswith("EDcl"):
                continue
            e = norm(x.get("ementa"))
            if not re.search(r"TRAFICO (ILICITO )?DE (DROGAS|ENTORPECENTES)|ART\. ?33,? (CAPUT|§)|11\.343", e):
                continue
            obj = objeto(e)
            if obj in ("cautelar", "execucao") or (obj == "pre_condenacao" and not a.manter_pre_condenacao):
                continue
            num = x["numeroProcesso"]
            if num in ja:
                continue
            base = classe.split(" no ")[-1].split(" nos ")[-1].strip()   # 'AgRg no AREsp' -> 'AREsp'
            reg = {
                "processo": f"{base} {num}",
                "busca_stj": f"{base.upper()}{num}",
                "registro": x.get("numeroRegistro", ""),
                "classe_acordao": classe,
                "relator": relator_norm(x.get("ministroRelator", "")),
                "relator_original": x.get("ministroRelator", ""),
                "turma": x.get("nomeOrgaoJulgador", ""),
                "data_decisao": x.get("dataDecisao", ""),
                "objeto": obj,
                "inicio_ementa": (x.get("ementa") or "").replace("\n", " ")[:200],
            }
            if num not in por_proc or reg["data_decisao"] > por_proc[num]["data_decisao"]:
                por_proc[num] = reg

    pop = list(por_proc.values())
    from collections import Counter
    cont = Counter(r["relator"] for r in pop)
    rel = sorted(m for m, c in cont.items() if c >= a.min_relator)
    rnd = random.Random(a.seed)
    cota = a.n // len(rel)
    amostra = []
    for m in rel:
        grupo = [r for r in pop if r["relator"] == m]
        rnd.shuffle(grupo)
        amostra += grupo[:cota]
    resto = [r for r in pop if r not in amostra]
    rnd.shuffle(resto)
    amostra += resto[: a.n - len(amostra)]
    amostra.sort(key=lambda r: (r["relator"], r["processo"]))

    os.makedirs(os.path.dirname(a.saida) or ".", exist_ok=True)
    with open(a.saida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(amostra[0].keys()))
        w.writeheader(); w.writerows(amostra)

    print(f"populacao: {len(pop)} processos de trafico (sem cautelar/execucao/EDcl/ja estudados)")
    for m in sorted(cont):
        print(f"  {m}: {cont[m]} na populacao, {sum(r['relator']==m for r in amostra)} na amostra")
    print("objeto na populacao:", dict(Counter(r["objeto"] for r in pop)))
    print("objeto na amostra:  ", dict(Counter(r["objeto"] for r in amostra)))
    print(f"amostra: {len(amostra)} -> {a.saida}")

if __name__ == "__main__":
    main()
