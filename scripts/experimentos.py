"""Experimentos E1-E4. Lê as saídas do Prolog e das árvores e gera tabelas LaTeX.

Uso (na raiz, depois de gerar_fatos.py, arvore_b.py e prolog/experimentos.pl):
  python scripts/experimentos.py
Gera resultados/tab_*.tex (incluídas em tex/trabalho.tex) e resultados/experimentos.json.
"""
import csv, json, os, re, sys
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

RAIZ = os.path.join(os.path.dirname(__file__), "..")
P = lambda *a: os.path.join(RAIZ, *a)
sys.path.insert(0, os.path.dirname(__file__))
import arvore_b as B

PERFIS = ["garantista", "intermediario", "restritivo"]
NOME = {"garantista": "garantista", "intermediario": "intermediário", "restritivo": "restritivo",
        "pro_reo": "a favor do réu", "onus_defesa": "contra o réu"}
PCT = lambda x: f"{100*x:.0f}"
res = {}

def tabela(nome, cab, linhas, legenda, rotulo, alin=None):
    alin = alin or "l" + "r" * (len(cab) - 1)
    t = [r"\begin{table}[h]", r"\centering\small", rf"\caption{{{legenda}}}", rf"\label{{{rotulo}}}",
         r"\begin{adjustbox}{max width=\textwidth}", rf"\begin{{tabular}}{{{alin}}}", r"\toprule", " & ".join(cab) + r" \\", r"\midrule"]
    t += [" & ".join(str(c) for c in l) + r" \\" for l in linhas]
    t += [r"\bottomrule", r"\end{tabular}", r"\end{adjustbox}", r"\end{table}"]
    open(P("resultados", f"tab_{nome}.tex"), "w", encoding="utf-8").write("\n".join(t) + "\n")

def fr(x):  # fração como texto
    return {"1/6": "1/6", "1/3": "1/3", "1/2": "1/2", "2/3": "2/3"}.get(str(x), str(x))

# ---------------- E1: sensibilidade ----------------
d = pd.read_csv(P("resultados", "e1_decisoes.csv"), dtype=str).fillna("")
d["meses"] = d.meses.astype(float)
n = d.caso.nunique()
lin = []
for pol in ["pro_reo", "onus_defesa"]:
    for p in PERFIS:
        x = d[(d.perfil == p) & (d.politica == pol)]
        lin.append([NOME[p], NOME[pol], f"{(x.decisao == 'concede').sum()}/{n}",
                    f"{x.meses.mean():.1f}", (x.regime == "aberto").sum(), (x.regime == "fechado").sum()])
tabela("e1_resumo", ["Leitura (perfil)", "Dado que falta conta", "Réus com redução", "Pena média (meses)",
                     "Regime aberto", "Regime fechado"],
       lin, f"E1 -- Os mesmos {n} réus julgados pelo juiz virtual com leituras diferentes da lei.", "tab:e1", "llrrrr")

piv = d[d.politica == "pro_reo"].pivot(index="caso", columns="perfil", values="decisao")
dif = (piv.nunique(axis=1) > 1).sum()
pena = d[d.politica == "pro_reo"].pivot(index="caso", columns="perfil", values="meses")
amp = (pena.max(axis=1) - pena.min(axis=1))
res["E1"] = {"n": n, "discordam": int(dif), "amplitude_pena_media_meses": round(amp.mean(), 1),
             "amplitude_pena_max_meses": float(amp.max()),
             "concede": {f"{p}|{pol}": int(((d.perfil == p) & (d.politica == pol) & (d.decisao == "concede")).sum())
                         for p in PERFIS for pol in ["pro_reo", "onus_defesa"]}}
# motivo da negativa quando o dado faltante pesa contra o réu
on = d[(d.politica == "onus_defesa") & (d.perfil == "garantista") & (d.decisao == "nega")]
res["E1"]["onus_so_por_faltante"] = int(on.motivos.str.fullmatch(r"\[(nao_comprovado\(\w+\),?)+\]").sum())

ab = pd.read_csv(P("resultados", "e1_ablacao.csv"))
nomes = {"quantidade_isolada_basta": "quantidade sozinha basta", "limites_menores": "limites de quantidade menores",
         "janela_atos_5_anos": "atos infracionais até 5 anos", "ato_sem_data_conta": "ato infracional sem data conta",
         "acoes_em_curso_contam": "ações em curso contam (contra o Tema 1.139)",
         "indicios_amplos": "indícios aceitos: lista ampla", "minimo_1_indicador": "basta 1 indicador",
         "fracao_restritiva": "faixas de fração restritivas", "quantidade_nao_indica": "quantidade não indica dedicação",
         "atos_nao_contam": "atos infracionais não contam", "esquecimento_5_anos": "esquecimento de antecedentes (5 anos)",
         "indicios_restritos": "indícios aceitos: só arma e facção", "fracao_garantista": "faixas de fração garantistas"}
ab = ab.sort_values(["mudam_decisao", "mudam_fracao"], ascending=False)
tabela("e1_ablacao", ["Escolha trocada (partindo da leitura intermediária)", "Na direção", "Réus que mudam de decisão",
                      "Réus que mudam de fração", "Réus com redução (antes $\\to$ depois)"],
       [[nomes[r.variante], r.origem, r.mudam_decisao, r.mudam_fracao, f"{r.concede_base} $\\to$ {r.concede_variante}"]
        for r in ab.itertuples()],
       f"E1 -- Trocando uma escolha de cada vez ({n} réus).", "tab:e1b", "p{5.6cm}lp{1.9cm}p{1.9cm}p{2.4cm}")
res["E1"]["ablacao"] = ab.to_dict(orient="records")

# ---------------- E2: relator vencido / monocrática reformada ----------------
p4 = list(csv.DictReader(open(P("dados", "amostra_p4_casos.csv"), encoding="utf-8")))
casos_ids = sorted(d.caso.unique())
lin, e2 = [], []
for i, r in enumerate(p4):
    mono, fin = r["stj_mono_p4"], r["stj_final_p4"]
    if not mono.startswith("conced") or fin.startswith("concedido"):
        continue   # só os casos em que a Turma reformou a monocrática
    cid = f"p4_{r['registro']}_{i}"
    dd = d[(d.caso == cid) & (d.politica == "pro_reo")].set_index("perfil")
    fmt = lambda p: ("concede " + fr(dd.loc[p, "fracao"])) if dd.loc[p, "decisao"] == "concede" else dd.loc[p, "decisao"]
    g = r["qtd_g_total"]
    qtd = (f"{float(g)/1000:.0f} kg" if float(g) >= 1000 else f"{float(g):.0f} g") if g else "?"
    item = {"processo": r["processo"], "droga": r["drogas"], "qtd": qtd, "monocratica": mono, "acordao": fin,
            "votacao": r["votacao"].split(";")[0].replace("unanime", "unânime"), **{p: fmt(p) for p in PERFIS}}
    e2.append(item)
    lin.append([r["processo"], f"{qtd} ({r['drogas'].split('+')[0].replace('cocaina', 'cocaína')})", mono.replace("_oficio", " (ofício)").replace("concedeu", "concede"),
                fin.replace("redimensionado_fracao", "reduz a").replace("concedido_oficio", "concede (ofício)"),
                item["votacao"], fmt("garantista"), fmt("intermediario"), fmt("restritivo")])
tabela("e2", ["Processo", "Droga apreendida", "Relator (sozinho)", "Turma", "Votação", "Garant.", "Interm.", "Restrit."], lin,
       "E2 -- O relator deu a redução sozinho e a Turma tirou (relator: Sebastião Reis; recurso do MP).",
       "tab:e2", "llllllll")
res["E2"] = e2

# ---------------- E3: o que a árvore B aprende ----------------
jb = json.load(open(P("resultados", "arvore_b.json"), encoding="utf-8"))
lin = []
for m in ["com_relator", "sem_relator"]:
    v = jb[m]["validacao_cruzada_5"]
    lin.append([m.replace("_", " "), jb[m]["raiz"].replace("classe=", "é ").replace("=", " = "), PCT(v["acuracia_balanceada"]),
                PCT(v["recall_vitorias"]), PCT(v["precisao_vitorias"]), f"{v['vp']}/{v['vp'] + v['fn']}", v["fp"]])
v = jb["sem_relator"]["deixa_um_relator_fora"]
lin.append(["sem relator, testada num relator que não viu", "", PCT(v["acuracia_balanceada"]), PCT(v["recall_vitorias"]),
            PCT(v["precisao_vitorias"]), f"{v['vp']}/{v['vp'] + v['fn']}", v["fp"]])
tabela("e3", ["Versão", "1ª pergunta", "Acerto equilibrado (\\%)", "Vitórias achadas (\\%)", "Quando diz vence, acerta (\\%)",
              "Vitórias achadas", "Alarmes falsos"], lin,
       "E3 -- Árvore aprendida: " + f"{jb['n']:,}".replace(",", ".") + f" recursos da defesa, dos quais {jb['vitorias']} vitórias. "
       + "Testada em casos que ela não viu no treino.",
       "tab:e3", "p{3.4cm}lp{1.6cm}p{1.6cm}p{1.9cm}p{1.4cm}p{1.3cm}")
# contrafactual: mesmo processo, outro relator da mesma turma
dB = B.carregar(); X = B.matriz(dB, True)
mdl = DecisionTreeClassifier(**B.PARAMS).fit(X, dB.y)
muda, por_rel = 0, {}
rels = {t: sorted(dB[dB.turma == t].relator.unique()) for t in dB.turma.unique()}
for i, r in dB.iterrows():
    preds = {}
    for rel in rels[r.turma]:
        x = X.loc[[i]].copy()
        for c in X.columns:
            if c.startswith("relator="): x[c] = int(c == f"relator={rel}")
        preds[rel] = int(mdl.predict(x)[0])
    if len(set(preds.values())) > 1:
        muda += 1
        por_rel[r.turma] = por_rel.get(r.turma, 0) + 1
res["E3"] = {"metricas": {k: jb[k] for k in ["com_relator", "sem_relator"]}, "n": jb["n"], "vitorias": jb["vitorias"],
             "contrafactual_mudam": muda, "contrafactual_por_turma": por_rel, "regras": jb["regras_texto"]}

# ---------------- E4: árvore A x decisão real ----------------
fatos = open(P("prolog", "fatos_casos.pl"), encoding="utf-8").read()
ref = {}
for c, inst, v in re.findall(r"referencia\('([^']+)', (tj_p4|stj_p4), (\w+)", fatos):
    ref.setdefault(c, {})[inst] = "concede" if v == "concedido" else "nega"
lin, e4 = [], {}
for pol in ["pro_reo", "onus_defesa"]:
    for p in PERFIS:
        x = d[(d.perfil == p) & (d.politica == pol)]
        row = [NOME[p], NOME[pol]]
        for inst in ["tj_p4", "stj_p4"]:
            pares = [(r.decisao, ref[r.caso][inst]) for r in x.itertuples() if inst in ref.get(r.caso, {})]
            ok = sum(a == b for a, b in pares)
            row.append(f"{ok}/{len(pares)}")
            e4[f"{p}|{pol}|{inst}"] = [ok, len(pares)]
        lin.append(row)
real_stj = [v["stj_p4"] for v in ref.values() if "stj_p4" in v]
real_tj = [v["tj_p4"] for v in ref.values() if "tj_p4" in v]
tabela("e4", ["Leitura (perfil)", "Dado que falta conta", "Igual ao TJ", "Igual ao STJ"], lin,
       f"E4 -- Juiz virtual $\\times$ decisão real sobre o § 4º. O TJ concedeu em {real_tj.count('concede')} de "
       f"{len(real_tj)} réus; o STJ, em {real_stj.count('concede')} de {len(real_stj)}.", "tab:e4", "llrr")
res["E4"] = {"concordancia": e4, "stj_concede": [real_stj.count("concede"), len(real_stj)],
             "tj_concede": [real_tj.count("concede"), len(real_tj)]}

json.dump(res, open(P("resultados", "experimentos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: v for k, v in res.items() if k != "E3"}, ensure_ascii=False, indent=1, default=str)[:4000])
print("E3 contrafactual:", muda, por_rel)
