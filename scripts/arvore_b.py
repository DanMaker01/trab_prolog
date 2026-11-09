"""Árvore B: árvore de decisão APRENDIDA das decisões do STJ e exportada para Prolog.

Uso (na raiz do projeto):
  python scripts/arvore_b.py
Gera:
  prolog/fatos_ementas.pl   fatos de cada processo (o que se sabia ANTES do julgamento)
  prolog/arvore_b.pl        as árvores aprendidas, como regras Prolog
  prolog/pred_sklearn.pl    previsões do scikit-learn (para o teste de equivalência em Prolog)
  resultados/arvore_b.json  métricas de validação cruzada e regras em texto

Dados: dados/ementas_t5.csv + dados/ementas_t6.csv, só recursos da DEFESA
(no recurso do MP, "o réu ganha" quase sempre: é uma regra trivial que esconderia o resto).
Alvo: defesa_vence = resultado_reu != desfavoravel.

Variáveis de entrada (sem vazamento): turma, relator, classe do processo, assunto (objeto),
marcadores da ementa. FICAM DE FORA, por serem parte da própria decisão: barreiras
(Súmula 7 etc.), dispositivo, votação, relator_vencido.

Dois modelos:
  com_relator  todas as variáveis
  sem_relator  sem turma e sem relator (só "o caso")
A pergunta não é quanto acertam, e sim O QUE aprendem.
"""
import json, os, re
import numpy as np, pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import StratifiedKFold, cross_val_predict, LeaveOneGroupOut
from sklearn.metrics import balanced_accuracy_score, recall_score, precision_score, confusion_matrix

RAIZ = os.path.join(os.path.dirname(__file__), "..")
P = lambda *a: os.path.join(RAIZ, *a)
PARAMS = dict(max_depth=4, min_samples_leaf=10, class_weight="balanced", random_state=0)

def carregar():
    d = pd.concat([pd.read_csv(P("dados", f), dtype=str) for f in ("ementas_t5.csv", "ementas_t6.csv")],
                  ignore_index=True).fillna("")
    d = d[d.recorrente == "defesa"].copy()
    d["classe"] = d.processo.str.split().str[0]
    d["y"] = (d.resultado_reu != "desfavoravel").astype(int)
    return d.reset_index(drop=True)

def matriz(d, com_relator):
    cols = (["turma", "relator"] if com_relator else []) + ["classe", "objeto"]
    X = pd.get_dummies(d[cols], prefix_sep="=").astype(int)
    for m in sorted({m for s in d.marcadores for m in s.split()}):
        X[f"marcador={m}"] = d.marcadores.str.split().apply(lambda l: int(m in l))
    return X

def metricas(y, p):
    tn, fp, fn, tp = confusion_matrix(y, p, labels=[0, 1]).ravel()
    return {"acuracia_balanceada": round(balanced_accuracy_score(y, p), 3),
            "recall_vitorias": round(recall_score(y, p, zero_division=0), 3),
            "precisao_vitorias": round(precision_score(y, p, zero_division=0), 3),
            "vp": int(tp), "fp": int(fp), "fn": int(fn), "vn": int(tn)}

# ---------- exportação para Prolog ----------
def q(s):
    return "'" + str(s).replace("\\", "\\\\").replace("'", "\\'") + "'"

def teste_prolog(nome):
    var, val = nome.split("=", 1)
    return f"tem(C, {var}, {q(val)})"

def classes(t, i):
    """Conjunto das classes das folhas abaixo do nó i."""
    if t.children_left[i] == -1:
        v = t.value[i][0]
        return {"vence" if v[1] > v[0] else "perde"}
    return classes(t, t.children_left[i]) | classes(t, t.children_right[i])

def corpo(t, nos, i, ind):
    pad = "    " * ind
    cs = classes(t, i)
    if len(cs) == 1:   # subárvore com uma só resposta: colapsa (o teste não muda nada)
        return f"{pad}Classe = {cs.pop()}"
    f = nos[t.feature[i]]
    # todas as variáveis são 0/1; o limiar é 0.5: esquerda = não tem, direita = tem
    return (f"{pad}(   {teste_prolog(f)}\n"
            f"{pad}->\n{corpo(t, nos, t.children_right[i], ind + 1)}\n"
            f"{pad};\n{corpo(t, nos, t.children_left[i], ind + 1)}\n"
            f"{pad})")

def main():
    d = carregar()
    out, regras, preds = {"n": int(len(d)), "vitorias": int(d.y.sum())}, [], []
    with open(P("prolog", "arvore_b.pl"), "w", encoding="utf-8") as f:
        f.write(":- encoding(utf8).\n% Gerado por scripts/arvore_b.py -- não editar à mão.\n"
                "% arvore_b(+Modelo, +Caso, -Classe): Classe = vence | perde (para a defesa)\n"
                ":- discontiguous arvore_b/3.\n\n")
        for nome, com in (("com_relator", True), ("sem_relator", False)):
            X = matriz(d, com)
            cv = StratifiedKFold(5, shuffle=True, random_state=2026)
            p_cv = cross_val_predict(DecisionTreeClassifier(**PARAMS), X, d.y, cv=cv)
            m = DecisionTreeClassifier(**PARAMS).fit(X, d.y)
            out[nome] = {"validacao_cruzada_5": metricas(d.y, p_cv),
                         "variaveis_usadas": sorted({X.columns[i] for i in m.tree_.feature if i >= 0}),
                         "importancia": {X.columns[i]: round(v, 3) for i, v in
                                         sorted(enumerate(m.feature_importances_), key=lambda t: -t[1]) if v > 0},
                         "raiz": X.columns[m.tree_.feature[0]]}
            if not com:   # sem relator: treinar com uns relatores e testar em outro
                logo = cross_val_predict(DecisionTreeClassifier(**PARAMS), X, d.y, groups=d.relator,
                                         cv=LeaveOneGroupOut())
                out[nome]["deixa_um_relator_fora"] = metricas(d.y, logo)
            regras.append(f"## {nome}\n" + export_text(m, feature_names=list(X.columns)))
            f.write(f"arvore_b({nome}, C, Classe) :-\n{corpo(m.tree_, list(X.columns), 0, 1)}.\n\n")
            for reg, p in zip(d.registro, m.predict(X)):
                preds.append(f"pred_sklearn({nome}, {q(reg)}, {'vence' if p else 'perde'}).")
    with open(P("prolog", "fatos_ementas.pl"), "w", encoding="utf-8") as f:
        f.write(":- encoding(utf8).\n% Gerado por scripts/arvore_b.py. tem(Processo, Variavel, Valor).\n"
                ":- discontiguous tem/3, resultado_real/2.\n")
        for _, r in d.iterrows():
            c = q(r.registro)
            f.write(f"tem({c}, turma, {q(r.turma)}). tem({c}, relator, {q(r.relator)}). "
                    f"tem({c}, classe, {q(r.classe)}). tem({c}, objeto, {q(r.objeto)}).\n")
            for mk in r.marcadores.split():
                f.write(f"tem({c}, marcador, {q(mk)}).\n")
            f.write(f"resultado_real({c}, {'vence' if r.y else 'perde'}).\n")
    with open(P("prolog", "pred_sklearn.pl"), "w", encoding="utf-8") as f:
        f.write(":- encoding(utf8).\n% Gerado por scripts/arvore_b.py (teste de equivalência)\n" + "\n".join(preds) + "\n")
    out["regras_texto"] = regras
    os.makedirs(P("resultados"), exist_ok=True)
    json.dump(out, open(P("resultados", "arvore_b.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "regras_texto"}, ensure_ascii=False, indent=1))
    print("\n".join(regras))

if __name__ == "__main__":
    main()
