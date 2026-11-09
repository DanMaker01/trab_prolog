"""Sorteia a base direcionada do §4º (tráfico privilegiado) a partir das tabelas de ementas.

Uso (na raiz do projeto):
  python scripts/sortear_p4.py dados/ementas_t5.csv dados/ementas_t6.csv --ja-baixados dados/metadados.csv --saida dados/amostra_p4.csv

Desenho (caso-controle):
  - só processos cujo assunto principal é o §4º (objeto = p4) e em que quem recorreu foi a DEFESA;
  - entram TODAS as vitórias da defesa (favoravel/parcial), porque são raras;
  - e um sorteio de N derrotas por relator (semente 2026);
  - ficam de fora processos já baixados (metadados.csv) e relatores com menos de 5 casos.
Na análise, as derrotas devem ser re-ponderadas (peso = derrotas do relator / derrotas sorteadas).
"""
import argparse, csv, random
from collections import defaultdict

ap = argparse.ArgumentParser()
ap.add_argument("ementas", nargs="+")
ap.add_argument("--ja-baixados", default="")
ap.add_argument("--saida", required=True)
ap.add_argument("--n", type=int, default=8, help="derrotas sorteadas por relator")
ap.add_argument("--seed", type=int, default=2026)
a = ap.parse_args()

ja = set()
if a.ja_baixados:
    ja = {r["registro"] for r in csv.DictReader(open(a.ja_baixados, encoding="utf-8"))}

linhas = []
for f in a.ementas:
    linhas += [r for r in csv.DictReader(open(f, encoding="utf-8"))
               if r["objeto"] == "p4" and r["recorrente"] == "defesa" and r["registro"] not in ja]

por_rel = defaultdict(list)
for r in sorted(linhas, key=lambda r: r["registro"]):
    por_rel[r["relator"]].append(r)

rng = random.Random(a.seed)
saida = []
for rel in sorted(por_rel):
    casos = por_rel[rel]
    if len(casos) < 5:
        continue
    vit = [r for r in casos if r["resultado_reu"] != "desfavoravel"]
    der = [r for r in casos if r["resultado_reu"] == "desfavoravel"]
    sort = rng.sample(der, min(a.n, len(der)))
    peso = round(len(der) / len(sort), 3) if sort else 0
    for r, grupo, p in [(x, "vitoria", 1) for x in vit] + [(x, "derrota", peso) for x in sort]:
        classe, num = r["processo"].split()
        saida.append({"busca_stj": f"{classe.upper()}{num}", "processo": r["processo"], "registro": r["registro"],
                      "turma": r["turma"], "relator": rel, "data_decisao": r["data_decisao"],
                      "resultado_ementa": r["resultado_reu"], "grupo": grupo, "peso": p})

with open(a.saida, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(saida[0].keys()))
    w.writeheader(); w.writerows(saida)
print(len(saida), "processos ->", a.saida)
for rel in sorted({s["relator"] for s in saida}):
    x = [s for s in saida if s["relator"] == rel]
    print(f"  {rel:18s} {len(x):3d}  vitorias={sum(s['grupo']=='vitoria' for s in x)}")
