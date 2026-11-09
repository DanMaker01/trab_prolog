"""Classifica, só pelo texto do JSON (ementa + dispositivo), todos os acórdãos de tráfico de uma ou mais turmas.

Uso (na raiz do projeto):
  python scripts/analisar_ementas.py fontes/json/*.json --saida dados/ementas_t5.csv
  python scripts/analisar_ementas.py fontes/json/sexta_turma/*.json --saida dados/ementas_t6.csv

Para cada processo (o acórdão mais recente, sem EDcl e sem cautelar/execução/pré-condenação), gera:
  objeto            assunto principal (mesma regra de sortear_amostra.py)
  recorrente        mp | defesa (quem interpôs o recurso julgado no acórdão; heurística pela ementa)
  dispositivo       provido | parcial | desprovido | nao_conhecido | concedido_oficio
  resultado_reu     favoravel | parcial | desfavoravel (combinação dos dois anteriores)
  barreiras         súmulas/óbices citados na ementa (Sum7, Sum182, Sum284, Sum83, HC_substitutivo, ...)
  marcadores        expressões sobre a pessoa ou o lugar (vulgo, comunidade, facção, ...)
  votacao           unanime | maioria

É uma aproximação: os 40 sorteados extraídos à mão/IA servem de gabarito (ver README).
"""
import argparse, csv, json, os, re, sys, unicodedata
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from sortear_amostra import objeto, relator_norm  # mesma classificação de assunto

def norm(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().upper()
    return re.sub(r"\s+", " ", t)

BARREIRAS = {
    "Sum7": r"SUMULA (N\. ?)?7\b|SUMULA 7/STJ|REEXAME (DO CONJUNTO )?FATICO|REVOLVIMENTO",
    "Sum182": r"SUMULA (N\. ?)?182|IMPUGNACAO ESPECIFICA|DIALETICIDADE",
    "Sum284": r"SUMULA (N\. ?)?284",
    "Sum83": r"SUMULA (N\. ?)?83\b",
    "HC_substitutivo": r"SUBSTITUTIVO|SUCEDANEO|INADEQUACAO DA VIA",
    "revisao_criminal": r"REVISAO CRIMINAL",
    "supressao_instancia": r"SUPRESSAO DE INSTANCIA",
    "reiteracao": r"REITERACAO DE PEDIDO|MERA REITERACAO",
}
MARCADORES = {
    "vulgo": r"\bVULGO\b|\bALCUNHA\b",
    "comunidade_bairro": r"\bCOMUNIDADE\b|\bFAVELA\b|\bMORRO\b|\bBAIRRO\b",
    "local_conhecido": r"LOCAL (CONHECIDO|NOTORIAMENTE|DE INTENSO)|PONTO DE (VENDA|TRAFICO)|AREA DE (ALTA )?(INCIDENCIA|CRIMINALIDADE)|REGIAO CONFLAGRADA",
    "faccao": r"FACCAO|\bPCC\b|COMANDO VERMELHO|ORGANIZACAO CRIMINOSA",
    "conhecido_policia": r"CONHECIDO (DA|PELA|NO MEIO) POLIC|JA CONHECIDO",
    "ocupacao": r"OCUPACAO LICITA|DESEMPREG",
    "atos_infracionais": r"ATOS? INFRACIONA",
    "nervosismo": r"NERVOSISMO|ATITUDE SUSPEITA",
    "fuga_mudanca_direcao": r"\bFUGA\b|EMPREENDEU FUGA|MUDANCA (REPENTINA )?DE DIRECAO|MUDOU DE DIRECAO|EVASAO",
    "denuncia_anonima": r"DENUNCIA[S]? ANONIMA",
}

def dispositivo(dec):
    m = re.search(r"ACORDAM[^,]*,(.*?)(OS SRS\.|OS EXMOS|$)", dec)
    t = m.group(1) if m else dec
    if re.search(r"CONCEDER (A|DE OFICIO A) ORDEM DE OFICIO|CONCEDER(?:-LHE)? A ORDEM,? DE OFICIO|CONCEDENDO.*OFICIO|ORDEM DE OFICIO", t):
        return "concedido_oficio"
    if re.search(r"DAR PARCIAL PROVIMENTO|DAR-LHE PARCIAL|PARCIALMENTE PROVIDO|CONCEDER PARCIALMENTE", t):
        return "parcial"
    if re.search(r"DAR PROVIMENTO AO AGRAVO REGIMENTAL PARA CONHECER DO AGRAVO (E|PARA) (NAO CONHECER|NEGAR)", t):
        return "desprovido"   # vitória só procedural
    if re.search(r"DAR PROVIMENTO|DAR-LHE PROVIMENTO|CONCEDER A ORDEM|ACOLHER OS EMBARGOS, COM EFEITOS", t):
        return "provido"
    if re.search(r"NAO CONHECER|NAO CONHECEU", t) and not re.search(r"PROVIMENTO", t):
        return "nao_conhecido"
    return "desprovido"

def recorrente(e, classe, dec=""):
    """Quem interpôs o recurso julgado no acórdão. Na dúvida, 'defesa' (é o caso mais comum)."""
    cab = e[:1500]
    if re.search(r"(INTERPOSTO|OPOSTO|MANEJADO|AJUIZADO)S? PEL[OA] (MINISTERIO PUBLICO|PARQUET|MPF\b|ORGAO MINISTERIAL)"
                 r"|IRRESIGNACAO MINISTERIAL|AGRAVO (REGIMENTAL )?MINISTERIAL", cab):
        return "mp"
    if re.search(r"QUE (DEU|DAR) (PARCIAL )?PROVIMENTO AO RECURSO ESPECIAL (DO|INTERPOSTO PELO) (MINISTERIO|PARQUET)", cab):
        return "defesa"
    if classe.startswith("AgRg") and re.search(
            r"DECISAO (MONOCRATICA )?QUE (CONCEDEU|ABSOLVEU|RECONHECEU A (ILICITUDE|NULIDADE)|APLICOU A (MINORANTE|CAUSA)"
            r"|DEU (PARCIAL )?PROVIMENTO AO (AGRAVO|RECURSO|HABEAS)|DESCLASSIFICOU|REDUZIU|REDIMENSIONOU)", cab):
        return "mp"   # a defesa não agrava da própria vitória
    if classe.startswith("AgRg") and dec and re.search(r"DAR(-LHE)? PROVIMENTO", dec) and (
            re.search(r"CASSAR A DECISAO|RESTABELEC|DENEGAR A ORDEM", dec)
            or re.search(r"INAPLICABILIDADE|NAO INCIDENCIA|AFASTAMENTO DA (MINORANTE|CAUSA)|RESTABELEC\w* (O|DO) ACORDAO|DENEGA", cab)):
        return "mp"   # agravo provido que retira o benefício dado na monocrática: só pode ser do MP
    if not classe.startswith(("AgRg", "EDcl")) and re.search(
            r"(RECURSO ESPECIAL|AGRAVO) (INTERPOSTO PELO|DO) (MINISTERIO|PARQUET)|RESTABELEC\w* (DA|A) (SENTENCA|CONDENA)", cab):
        return "mp"
    return "defesa"

def resultado(rec, disp):
    favor_recorrente = disp in ("provido", "concedido_oficio")
    if rec == "defesa":
        return "favoravel" if favor_recorrente else "parcial" if disp == "parcial" else "desfavoravel"
    # recurso do MP: perder o recurso é bom para o réu
    return "desfavoravel" if disp == "provido" else "parcial" if disp == "parcial" else "favoravel"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsons", nargs="+")
    ap.add_argument("--saida", required=True)
    a = ap.parse_args()
    por_proc = {}
    for f in a.jsons:
        for x in json.load(open(f, encoding="utf-8")):
            classe = x.get("siglaClasse") or ""
            if classe.startswith("EDcl"):
                continue
            e = norm(x.get("ementa"))
            if not re.search(r"TRAFICO (ILICITO )?DE (DROGAS|ENTORPECENTES)|ART\. ?33,? (CAPUT|§)|11\.343|\bDROGAS?\b|ENTORPECENTE", e):
                continue
            obj = objeto(e)
            if obj in ("cautelar", "execucao", "pre_condenacao"):
                continue
            dec = norm(x.get("decisao"))
            rec, disp = recorrente(e, classe, dec), dispositivo(dec)
            base = classe.split(" no ")[-1].split(" nos ")[-1].strip()
            reg = {
                "registro": x.get("numeroRegistro", ""),
                "processo": f"{base} {x['numeroProcesso']}",
                "classe_acordao": classe,
                "turma": x.get("nomeOrgaoJulgador", ""),
                "relator": relator_norm(x.get("ministroRelator", "")),
                "data_decisao": x.get("dataDecisao", ""),
                "objeto": obj,
                "recorrente": rec,
                "dispositivo": disp,
                "resultado_reu": resultado(rec, disp),
                "barreiras": " ".join(k for k, p in BARREIRAS.items() if re.search(p, e)),
                "marcadores": " ".join(k for k, p in MARCADORES.items() if re.search(p, e)),
                "votacao": "maioria" if "POR MAIORIA" in dec else "unanime",
                "relator_vencido": "sim" if re.search(r"QUE LAVRARA O ACORDAO", dec) else "nao",
            }
            num = x["numeroProcesso"]
            if num not in por_proc or reg["data_decisao"] > por_proc[num]["data_decisao"]:
                por_proc[num] = reg
    linhas = sorted(por_proc.values(), key=lambda r: (r["relator"], r["processo"]))
    os.makedirs(os.path.dirname(a.saida) or ".", exist_ok=True)
    with open(a.saida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader(); w.writerows(linhas)
    n = len(linhas)
    print(f"{n} processos -> {a.saida}")
    for campo in ("resultado_reu", "recorrente", "dispositivo", "objeto", "votacao"):
        print(f"  {campo}:", dict(Counter(r[campo] for r in linhas).most_common()))
    print("  barreiras:", dict(Counter(b for r in linhas for b in r["barreiras"].split()).most_common()))
    print("  marcadores:", dict(Counter(m for r in linhas for m in r["marcadores"].split()).most_common()))

if __name__ == "__main__":
    main()
