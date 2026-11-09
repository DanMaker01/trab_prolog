"""Contagens da seção "Os dados em números" (tex/secao_dados.tex).
Uso (na raiz):  python scripts/contagens.py
"""
import os
import pandas as pd
from scipy.stats import fisher_exact, chi2_contingency

RAIZ = os.path.join(os.path.dirname(__file__), "..")
D = lambda f: os.path.join(RAIZ, "dados", f)

d = pd.concat([pd.read_csv(D(f), dtype=str) for f in ("ementas_t5.csv", "ementas_t6.csv")], ignore_index=True).fillna("")
d["classe"] = d.processo.str.split().str[0]
print("processos por turma:", d.turma.value_counts().to_dict())
for col in ("classe", "objeto", "recorrente", "resultado_reu", "votacao", "relator_vencido"):
    print(f"\n{col}\n", pd.crosstab(d[col], d.turma, margins=True))
print("\nbarreiras:")
for b in ["Sum7", "HC_substitutivo", "Sum182", "revisao_criminal", "Sum83", "supressao_instancia", "Sum284"]:
    print(f"  {b}:", d.groupby("turma").barreiras.apply(lambda s: s.str.contains(b).sum()).to_dict())
print("  pelo menos uma:", d.groupby("turma").barreiras.apply(lambda s: (s != "").sum()).to_dict())
print("\nmarcadores:")
for m in ["faccao", "fuga_mudanca_direcao", "denuncia_anonima", "local_conhecido", "nervosismo", "atos_infracionais"]:
    print(f"  {m}:", d.marcadores.str.contains(m).sum())
print("  pelo menos um:", (d.marcadores != "").sum())

d["ano"] = d.mes_publicacao.str[:4]
print("\nprocessos por ano:", d.ano.value_counts().to_dict())
x = d[d.recorrente == "defesa"].copy()
x["vence"] = (x.resultado_reu != "desfavoravel").astype(int)
print("\nrecursos da defesa por turma:\n", x.groupby("turma").vence.agg(["sum", "count"]))
print("Fisher (turma):", fisher_exact(pd.crosstab(x.turma, x.vence).values).pvalue)
print("\npor turma e ano:\n", x.groupby(["turma", "ano"]).vence.agg(["sum", "count", "mean"]))
print("\npor relator e ano:\n", x.groupby(["turma", "relator", "ano"]).vence.agg(["sum", "count"]).unstack(fill_value=0))
s5 = x[(x.turma == "QUINTA TURMA") & (x.ano == "2025")]
dan = s5.relator.str.startswith("DANIELA")
print("\n5ª Turma 2025 - Daniela Teixeira:", s5[dan].vence.sum(), "/", dan.sum(),
      "| demais relatores:", s5[~dan].vence.sum(), "/", (~dan).sum(),
      "| vitórias dela por unanimidade:", (s5[dan & (s5.vence == 1)].votacao == "unanime").sum(),
      "| Fisher:", fisher_exact(pd.crosstab(dan, s5.vence).values).pvalue)
g = x.groupby(["turma", "relator"]).vence.agg(["sum", "count"]); g["%"] = (100 * g["sum"] / g["count"]).round(1)
print("\npor relator:\n", g)
for t in x.turma.unique():
    s = x[x.turma == t]
    print(f"qui-quadrado relatores ({t}):", chi2_contingency(pd.crosstab(s.relator, s.vence))[1])
print("\n§ 4º por relator:\n", x[x.objeto == "p4"].groupby(["turma", "relator"]).vence.agg(["sum", "count"]))
print("\npor assunto:\n", x.groupby("objeto").vence.agg(["sum", "count"]))
print("\ncom/sem barreira:\n", pd.crosstab(x.barreiras != "", x.vence))
t = pd.crosstab(x.marcadores != "", x.vence)
print("\ncom/sem marcador:\n", t, "\nFisher:", fisher_exact(t.values).pvalue)

for nome, casos, teses in (("5ª", "amostra_casos.csv", "amostra_teses.csv"), ("6ª", "amostra_t6_casos.csv", "amostra_t6_teses.csv")):
    c = pd.read_csv(D(casos), dtype=str).fillna(""); c = c[c.incluir.str.startswith("sim")]
    t = pd.read_csv(D(teses), dtype=str).fillna(""); t = t[t.incluir.str.startswith("sim")]
    print(f"\namostra {nome}: réus {len(c)}, resultado {c.resultado_final_reu.value_counts().to_dict()}, "
          f"defesa {c.defesa_meta.value_counts().to_dict()}, erro técnico {(c.erro_tecnico_defesa.str.strip() != '').sum()}, "
          f"teses {len(t)}, mérito {(t.analisou_merito == 'sim').sum()}, aceitas {(t.resultado_reu == 'favoravel').sum()}")
