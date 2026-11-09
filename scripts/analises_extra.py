"""Análises complementares da base de decisões (Tabela 1).

Uso (na raiz):  python scripts/analises_extra.py
Gera:
  tex/Imagens/taxa_mensal.pdf     gráfico: vitória da defesa por mês, 5ª x 6ª Turma
  resultados/tab_relator_ic.tex   vitórias por relator com intervalo de confiança de 95% (Wilson)
  resultados/tab_regressao.tex    regressão logística: o relator continua importando com o caso controlado?
  resultados/analises_extra.json  todos os números
Requer: pandas, matplotlib, statsmodels.
"""
import json, os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.stats.proportion import proportion_confint
from scipy.stats import chi2

RAIZ = os.path.join(os.path.dirname(__file__), "..")
P = lambda *a: os.path.join(RAIZ, *a)
res = {}

d = pd.concat([pd.read_csv(P("dados", f), dtype=str) for f in ("ementas_t5.csv", "ementas_t6.csv")],
              ignore_index=True).fillna("")
x = d[d.recorrente == "defesa"].copy()
x["vence"] = (x.resultado_reu != "desfavoravel").astype(int)
x["classe"] = x.processo.str.split().str[0].where(lambda s: s.isin(["HC", "AREsp", "REsp", "RHC"]), "outra")
x["ano"] = x.mes_publicacao.str[:4]
NOMES = {"DANIELA TEIXEIRA": "Daniela Teixeira", "REYNALDO SOARES": "Reynaldo Soares da Fonseca",
         "RIBEIRO DANTAS": "Ribeiro Dantas", "CARLOS CINI": "Carlos Cini (convocado)",
         "MARIA MARLUCE": "Maria Marluce Caldas", "MESSOD AZULAY": "Messod Azulay Neto",
         "JOEL ILAN": "Joel Ilan Paciornik", "SEBASTIAO REIS": "Sebastião Reis Júnior",
         "OTAVIO DE": "Otávio de Almeida Toledo (convocado)", "ROGERIO SCHIETTI": "Rogerio Schietti Cruz",
         "OG FERNANDES": "Og Fernandes", "ANTONIO SALDANHA": "Antonio Saldanha Palheiro",
         "CARLOS PIRES": "Carlos Pires Brandão", "NILSONI DE": "Nilsoni de Freitas (convocada)"}
pct = lambda v: f"{100 * v:.1f}".replace(".", ",")
mil = lambda n: f"{n:,}".replace(",", ".")

def tabela(nome, cab, linhas, legenda, rotulo, alin):
    t = [r"\begin{table}[h]", r"\centering\small", rf"\caption{{{legenda}}}", rf"\label{{{rotulo}}}",
         r"\begin{adjustbox}{max width=\textwidth}", rf"\begin{{tabular}}{{{alin}}}", r"\toprule",
         " & ".join(cab) + r" \\", r"\midrule"]
    for l in linhas:
        t.append(r"\midrule" if l == "---" else " & ".join(str(c) for c in l) + r" \\")
    t += [r"\bottomrule", r"\end{tabular}", r"\end{adjustbox}", r"\end{table}"]
    open(P("resultados", f"tab_{nome}.tex"), "w", encoding="utf-8").write("\n".join(t) + "\n")

# ---------- 1. gráfico mensal ----------
m = x.groupby(["turma", "mes_publicacao"]).vence.agg(["sum", "count"]).reset_index()
m["taxa"] = 100 * m["sum"] / m["count"]
meses = sorted(m.mes_publicacao.unique())
rot = {mm: f"{['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'][int(mm[4:])-1]}/{mm[2:4]}" for mm in meses}
plt.rcParams["font.size"] = 11
fig, ax = plt.subplots(figsize=(7.5, 3.6))
for turma, cor, nome in (("QUINTA TURMA", "#c0392b", "5ª Turma"), ("SEXTA TURMA", "#2c6fbb", "6ª Turma")):
    s = m[m.turma == turma].set_index("mes_publicacao").reindex(meses)
    xs = np.arange(len(meses))
    corte = 10   # primeiro mês de 2026: a linha não liga os dois períodos
    ax.plot(xs[:corte], s.taxa[:corte], marker="o", color=cor, label=nome)
    ax.plot(xs[corte:], s.taxa[corte:], marker="o", color=cor)
    for xi, (n, t) in enumerate(zip(s["count"], s.taxa)):   # meses com poucos recursos: ponto vazio
        if n < 100: ax.plot(xi, t, "o", color="white", mec=cor, ms=7, zorder=3)
ax.axvline(9.5, color="gray", ls="--", lw=1)
ax.text(9.6, ax.get_ylim()[1] * 0.92, "meses sem dados completos\n(nov/25 a mai/26)", fontsize=9, color="gray")
ax.set_xticks(range(len(meses))); ax.set_xticklabels([rot[mm] for mm in meses], rotation=45, fontsize=10)
ax.set_ylabel("defesa vence (% dos recursos)")
ax.plot([], [], "o", color="white", mec="gray", label="menos de 100 recursos no mês"); ax.grid(alpha=.3); ax.legend()
fig.tight_layout()
os.makedirs(P("tex", "Imagens"), exist_ok=True)
fig.savefig(P("tex", "Imagens", "taxa_mensal.pdf")); fig.savefig(P("resultados", "taxa_mensal.png"), dpi=150)
res["mensal"] = m.to_dict(orient="records")

# ---------- 2. relatores com intervalo de confiança ----------
g = x.groupby(["turma", "relator"]).vence.agg(["sum", "count"]).reset_index()
g = g[g["count"] >= 30].sort_values(["turma", "sum"], ascending=[True, False])
linhas, ic = [], {}
for i, r in enumerate(g.itertuples()):
    lo, hi = proportion_confint(r.sum, r.count, method="wilson")
    ic[r.relator] = [r.sum, r.count, lo, hi]
    if i and r.turma != g.iloc[i - 1].turma:
        linhas.append("---")
    linhas.append([r.turma[:5].replace("QUINT", "5ª").replace("SEXTA", "6ª"), NOMES.get(r.relator, r.relator),
                   mil(r.count), r.sum, pct(r.sum / r.count) + r"\%", f"{pct(lo)} a {pct(hi)}"])
tabela("relator_ic", ["Turma", "Relator", "Recursos da defesa", "Vitórias", "Defesa vence", "Margem (95\\%)"],
       linhas, "Vitórias da defesa por relator, com a margem de erro de 95\\% (relatores com 30 recursos ou mais).",
       "tab:dados-relator", "llrrrr")
res["relator_ic"] = ic

# ---------- 3. regressão logística ----------
x["relator_ref"] = x.relator.replace({"REYNALDO SOARES": "AAA_REYNALDO"})   # referência: taxa perto da mediana
# relatores sem nenhuma vitória ficam fora: o modelo não consegue estimar uma chance "zero"
sem_vitoria = sorted(g[g["sum"] == 0].relator)
x = x[x.relator.isin(g.relator) & ~x.relator.isin(sem_vitoria)]
base = "vence ~ C(classe) + C(objeto) + C(ano)"
completo = smf.logit(base + " + C(relator_ref)", data=x).fit(disp=0, maxiter=200)
sem_rel = smf.logit(base, data=x).fit(disp=0, maxiter=200)
blocos = {}
for nome, termo in (("relator", "C(relator_ref)"), ("tipo de recurso", "C(classe)"), ("assunto", "C(objeto)"), ("ano", "C(ano)")):
    f = "vence ~ " + " + ".join(t for t in ["C(classe)", "C(objeto)", "C(ano)", "C(relator_ref)"] if t != termo)
    red = smf.logit(f, data=x).fit(disp=0, maxiter=200)
    lr = 2 * (completo.llf - red.llf); gl = completo.df_model - red.df_model
    blocos[nome] = {"lr": round(lr, 1), "gl": int(gl), "p": float(chi2.sf(lr, gl))}
ors = {}
for k, v in completo.params.items():
    if k.startswith("C(relator_ref)"):
        rel = k.split("T.")[1].rstrip("]")
        lo, hi = completo.conf_int().loc[k]
        ors[rel] = [float(np.exp(v)), float(np.exp(lo)), float(np.exp(hi)), float(completo.pvalues[k])]
res["regressao"] = {"n": int(len(x)), "blocos": blocos, "odds_ratios": ors,
                    "referencia": "REYNALDO SOARES", "fora_sem_vitoria": sem_vitoria, "pseudo_r2": float(completo.prsquared),
                    "pseudo_r2_sem_relator": float(sem_rel.prsquared)}
fmt = lambda v: f"{v:.2f}".replace(".", ",")
linhas = [[NOMES.get(r, r), fmt(o), f"{fmt(lo)} a {fmt(hi)}"]
          for r, (o, lo, hi, p) in sorted(ors.items(), key=lambda t: -t[1][0])]
tabela("regressao", ["Relator", "Chance de vitória (vezes a do relator de referência)", "Margem (95\\%)"], linhas,
       "Chance de a defesa vencer com cada relator, comparada à de Reynaldo Soares da Fonseca, "
       "para o mesmo tipo de recurso, assunto e ano (regressão logística).", "tab:dados-regressao", "lrr")
json.dump(res, open(P("resultados", "analises_extra.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(res["regressao"], ensure_ascii=False, indent=1))
