"""Monta a base de decisões (Tabela 1) a partir de todos os JSONs mensais do STJ.

Uso (na raiz):  python scripts/montar_base.py
Lê:   fontes/json/AAAAMMDD.json (5ª Turma) e fontes/json/sexta_turma/AAAAMMDD.json (6ª Turma)
Gera: dados/meses.csv        volume de cada arquivo mensal e se entrou na base
      dados/ementas_t5.csv   um processo por linha (só meses completos)
      dados/ementas_t6.csv

Meses incompletos: de novembro/2025 a maio/2026 os arquivos trazem só uma fração do volume
habitual (5% a 30%) e uma taxa de vitória da defesa muito acima dos outros meses, o que indica
uma seleção de decisões, e não o conjunto. Esses meses ficam fora (lista MESES_FORA).
Janeiro e fevereiro/2026 baixados eram da 1ª Turma (cível) e são descartados pelo filtro de turma.
"""
import csv, glob, json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from analisar_ementas import classificar, gravar

RAIZ = os.path.join(os.path.dirname(__file__), "..")
P = lambda *a: os.path.join(RAIZ, *a)
MESES_FORA = {"202511", "202512", "202601", "202602", "202603", "202604", "202605"}
FONTES = {"QUINTA TURMA": sorted(glob.glob(P("fontes", "json", "*.json"))),
          "SEXTA TURMA": sorted(glob.glob(P("fontes", "json", "sexta_turma", "*.json")))}

def main():
    meses = []
    for turma, arqs in FONTES.items():
        for f in arqs:
            mes = os.path.basename(f)[:6]
            dados = json.load(open(f, encoding="utf-8"))
            n_turma = sum(1 for x in dados if x.get("nomeOrgaoJulgador") == turma)
            linhas = classificar([f], turmas=(turma,))
            dfs = [l for l in linhas if l["recorrente"] == "defesa"]
            meses.append({"turma": turma, "mes": mes, "acordaos_no_arquivo": n_turma,
                          "processos_trafico": len(linhas), "recursos_defesa": len(dfs),
                          "vitorias_defesa": sum(l["resultado_reu"] != "desfavoravel" for l in dfs),
                          "incluido": "nao" if (mes in MESES_FORA or n_turma == 0) else "sim"})
    with open(P("dados", "meses.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(meses[0].keys())); w.writeheader(); w.writerows(meses)
    for turma, saida in (("QUINTA TURMA", "ementas_t5.csv"), ("SEXTA TURMA", "ementas_t6.csv")):
        ok = [f for f in FONTES[turma] if os.path.basename(f)[:6] not in MESES_FORA]
        linhas = classificar(ok, turmas=(turma,))
        gravar(linhas, P("dados", saida))
        print(f"{turma}: {len(ok)} meses, {len(linhas)} processos -> dados/{saida}",
              dict(Counter(l["resultado_reu"] for l in linhas)))

if __name__ == "__main__":
    main()
