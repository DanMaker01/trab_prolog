"""Testes dos dados e da classificação das ementas.
Uso (na raiz):  python scripts/testes_dados.py      (sai com erro se algum teste falhar)
"""
import csv, os, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from analisar_ementas import recorrente, dispositivo, resultado, norm
from montar_base import MESES_FORA

RAIZ = os.path.join(os.path.dirname(__file__), "..")
D = lambda f: os.path.join(RAIZ, "dados", f)
falhas = []
def teste(nome, cond):
    print(("ok   " if cond else "FALHA"), nome)
    if not cond: falhas.append(nome)

# 1. regras de classificação (casos que já deram erro)
teste("agravo do MP que restabelece a condenação = recurso do MP",
      recorrente(norm("TRAFICO PRIVILEGIADO. INAPLICABILIDADE. AGRAVO REGIMENTAL PROVIDO."), "AgRg no HC",
                 norm("ACORDAM ... DAR PROVIMENTO AO AGRAVO REGIMENTAL PARA CASSAR A DECISAO MONOCRATICA")) == "mp")
teste("agravo da defesa negado = desfavorável",
      resultado("defesa", dispositivo(norm("ACORDAM ... NEGAR PROVIMENTO AO AGRAVO REGIMENTAL"))) == "desfavoravel")
teste("recurso do MP negado = favorável ao réu", resultado("mp", "desprovido") == "favoravel")

# 2. a base só tem meses completos e só as turmas criminais
d = pd.concat([pd.read_csv(D(f), dtype=str) for f in ("ementas_t5.csv", "ementas_t6.csv")]).fillna("")
teste("nenhum mês incompleto na base", not set(d.mes_publicacao) & MESES_FORA)
teste("só 5ª e 6ª Turma", set(d.turma) <= {"QUINTA TURMA", "SEXTA TURMA"})
teste("um processo por linha", d.processo.is_unique or d.registro.is_unique)

# 3. a classificação concorda com os processos lidos por inteiro (pelo menos 85%)
idx = d.set_index("registro").resultado_reu
for arq in ("amostra_casos.csv", "amostra_t6_casos.csv", "amostra_p4_casos.csv"):
    gold = {}
    for r in csv.DictReader(open(D(arq), encoding="utf-8")):
        if r.get("incluir", "sim").startswith("sim"):
            gold.setdefault(r["registro"], r["resultado_final_reu"])
    pares = [(g, idx[k]) for k, g in gold.items() if k in idx.index]
    acc = sum((g == "desfavoravel") == (e == "desfavoravel") for g, e in pares) / len(pares)
    teste(f"validação {arq}: {acc:.0%} de {len(pares)}", acc >= 0.85)

sys.exit(1 if falhas else 0)
