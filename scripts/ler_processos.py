"""Lê todos os processo-*.csv exportados do STJ (pasta fontes/stj/<registro>/ ou _/) e gera dados/metadados.csv,
com uma linha por processo. Uso: python scripts/ler_processos.py  (rodar na raiz do projeto)"""
import csv, glob, os, re

def secoes(path):
    """Divide o arquivo em seções '=== NOME ===' -> lista de linhas (já parseadas com ';')."""
    out, atual = {}, None
    with open(path, encoding="utf-8-sig") as f:
        texto = f.read()
    # algumas linhas têm quebra dentro de aspas; o csv.reader trata isso
    for bloco in re.split(r"^=== (.+?) ===\s*$", texto, flags=re.M)[1:]:
        if atual is None:
            atual = bloco.strip(); continue
        linhas = [l for l in csv.reader(bloco.strip().splitlines(), delimiter=";") if l]
        out[atual] = linhas; atual = None
    return out

def tabela(linhas):
    """Seção em formato cabeçalho + linhas -> lista de dicts."""
    if not linhas: return []
    h = linhas[0]
    return [dict(zip(h, l)) for l in linhas[1:]]

def tipo_defesa(advs):
    a = advs.upper()
    if "DEFENSORIA" in a: return "defensoria"
    if a.strip(): return "particular"
    return ""

def ano_origem(numeros):
    """Ano do processo de 1º grau (ano da ação penal; o fato pode ser do ano anterior) a partir do número CNJ (NNNNNNN-DD.AAAA.J.TR.OOOO).
    Pega o menor ano entre os números de 20 dígitos que não são do próprio STJ (J.TR = 3.00)."""
    anos = []
    for n in numeros:
        n = re.sub(r"\D", "", n)
        if len(n) == 20 and n[13:16] != "300":
            anos.append(int(n[9:13]))
    return min(anos) if anos else ""

PAPEIS_REU = {"PACIENTE", "AGRAVANTE", "AGRAVADO", "RECORRENTE", "RECORRIDO",
              "EMBARGANTE", "EMBARGADO", "REQUERENTE", "REQUERIDO"}

def eh_mp(nome):
    n = nome.upper()
    return "MINISTÉRIO PÚBLICO" in n or "MPF" in n

def relator_real(p, fases):
    """Se o processo foi para a Vice-Presidência (recurso ao STF), recupera o relator nas fases."""
    rel = p.get("Ministro Relator", "")
    if "PRESIDENTE" not in rel.upper():
        return rel
    cont = {}
    for f in fases:
        m = re.search(r"Ministro\(a\) ([A-ZÁÉÍÓÚÂÊÔÃÕÇ ]+) \(Relator\)", f.get("Descricao", ""))
        if m: cont[m.group(1).strip()] = cont.get(m.group(1).strip(), 0) + 1
    return max(cont, key=cont.get) if cont else rel

def ler(path):
    s = secoes(path)
    p = {l[0]: l[1] for l in s.get("PROCESSO", [])[1:] if len(l) >= 2}
    partes = tabela(s.get("PARTES", []))
    fases = tabela(s.get("FASES", []))
    peticoes = [x for x in tabela(s.get("PETICOES", [])) if x.get("Numero")]
    origem = [r.get("Numero", "") for r in tabela(s.get("NUMEROS ORIGEM", []))]

    reus = [x for x in partes if x.get("Tipo Parte", "").upper() in PAPEIS_REU
            and not eh_mp(x.get("Nome", "")) and "TRIBUNAL" not in x.get("Nome", "").upper()]
    nomes_reus = {x["Nome"].upper() for x in reus}
    impetrantes = [x for x in partes if x.get("Tipo Parte", "").upper() == "IMPETRANTE"]
    apelidos = [x for x in partes if x.get("Tipo Parte", "").upper() == "OUTRO NOME"]  # grafia alternativa do réu
    advs = sorted({a.strip() for x in reus + impetrantes + apelidos
                   for a in re.split(r"[|,]", x.get("Advogados", "")) if a.strip()})
    if not advs:  # impetrante sem advogado listado (ex.: a própria Defensoria)
        advs = [x["Nome"] for x in impetrantes]

    mp_recorrente = any(eh_mp(x.get("Nome", "")) and x.get("Tipo Parte", "").upper() in ("RECORRENTE", "AGRAVANTE")
                        for x in partes)
    def quem(pet):
        nome = pet.get("Peticionario", "").upper()
        if eh_mp(nome): return "mp"
        if nome in nomes_reus or any(nome == i["Nome"].upper() for i in impetrantes): return "defesa"
        return "?"
    recursos = [pet for pet in peticoes if pet.get("Sigla") in ("AgRg", "EDcl", "RE", "ARE", "RO")]
    rec_mp = [pet["Sigla"] for pet in recursos if quem(pet) == "mp"]
    rec_def = [pet["Sigla"] for pet in recursos if quem(pet) == "defesa"]
    rec_stf = [pet for pet in recursos if pet["Sigla"] in ("RE", "ARE")]

    transito = next((re.search(r"(\d{2}/\d{2}/\d{4})", f["Descricao"]).group(1)
                     for f in fases if "Transitado em Julgado" in f.get("Descricao", "")), "")
    proclam = [f["Descricao"] for f in fases if "Proclamação Final" in f.get("Descricao", "")]
    votacao = ""
    if proclam:
        t = proclam[0].lower()
        votacao = "maioria" if "maioria" in t else "unanime" if "unanimidade" in t else ""
    return {
        "registro": p.get("Numero Registro", ""),
        "processo": f'{p.get("Classe","")} {p.get("Numero Classe","")}',
        "uf": p.get("UF", ""),
        "relator": relator_real(p, fases),
        "status": p.get("Status", ""),
        "reus": " | ".join(x["Nome"] for x in reus),
        "advogados": " | ".join(advs),
        "defesa": tipo_defesa(" ".join(advs)),
        "n_advogados": len(advs),
        "mp_recorrente_original": "sim" if mp_recorrente else "nao",
        "recursos_mp": " ".join(rec_mp),
        "recursos_defesa": " ".join(rec_def),
        "recurso_stf": " ".join(f'{x["Sigla"]}({quem(x)})' for x in rec_stf),
        "ano_origem_1grau": ano_origem(origem),
        "transito_em_julgado": transito,
        "votacao_ultima": votacao,
        "data_autuacao": next((l[1] for l in s.get("DATAS", []) if l and l[0] == "Data Autuacao"), ""),
    }

if __name__ == "__main__":
    arquivos = sorted(glob.glob(os.path.join("fontes", "stj", "*", "processo-*.csv")) +
                      glob.glob(os.path.join("_", "processo-*.csv")))
    vistos = {}
    for a in arquivos:  # um arquivo por registro
        vistos.setdefault(os.path.basename(a), a)
    arquivos = sorted(vistos.values())
    linhas = [ler(a) for a in arquivos]
    os.makedirs("dados", exist_ok=True)
    with open(os.path.join("dados", "metadados.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()) if linhas else ["registro"])
        w.writeheader(); w.writerows(linhas)
    print(f"{len(linhas)} processos -> dados/metadados.csv")
