"""Converte as tabelas extraídas (amostras e base do §4º) em fatos Prolog para a árvore A.

Uso (na raiz do projeto):
  python scripts/gerar_fatos.py            ->  prolog/fatos_casos.pl

Cada réu vira um conjunto de fatos. Só entram réus com `incluir = sim` (ou da base do §4º)
e em que o §4º foi discutido em alguma instância (sent_p4, tj_p4, stj_p4 ou fundamento preenchido).
Campo vazio = fato AUSENTE (a árvore A trata como "desconhecido").

Todas as regras de codificação de texto livre estão neste arquivo (INDICIOS, ler_status, ...)
para que o pré-processamento seja auditável.
"""
import csv, os, re, unicodedata

RAIZ = os.path.join(os.path.dirname(__file__), "..")
D = lambda f: os.path.join(RAIZ, "dados", f)

def norm(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", t).strip()

# ---------- codificação de texto livre -> indícios (auditável) ----------
INDICIOS = {
    "petrechos":  r"balanc|embalag|sacol|eppendorf|pinos vazios|caderno|anotac|faca|tesoura|plastic|maquina de cartao|petrecho|fracionad|prensa",
    "arma":       r"\barmas?\b|revolver|pistola|municao|calibre",
    "dinheiro":   r"r\$|dinheiro|especie",
    "celular":    r"celular|mensage|conversa|whatsapp|telefon",
    "investigacao_previa": r"investigac|monitorament|campana|interceptac|inteligencia|mandado|vigilancia",
    "denuncias":  r"denuncia",
    "local_conhecido": r"local conhecido|ponto de (venda|trafico)|boca de fumo|ponto de drogas",
    "faccao":     r"faccao|\bpcc\b|comando vermelho|organizacao criminosa|gangue|\borcrim",
    "logistica":  r"logistic|rota|interestadual|fronteira|divisao de tarefas|propriedade rural|fundo falso|veiculo adulterado|\bmula|transporte|concurso",
    "variedade":  r"variedade|diversidade",
}
DROGAS = {"maconha": r"maconha|skunk|cannabis", "haxixe": r"haxixe", "cocaina": r"cocaina|pasta base",
          "crack": r"crack|\boxi\b", "sintetica": r"ecstasy|mdma|lsd|k2|sintetic|metanfetamina|lanca"}

def drogas(txt):
    t = norm(txt)
    return [d for d, p in DROGAS.items() if re.search(p, t)]

def numero(txt):
    m = re.search(r"\d+(?:\.\d+)?", (txt or "").replace(",", "."))
    return float(m.group()) if m else None

def sim_nao(txt):
    t = norm(txt)
    if t.startswith("sim"): return "sim"
    if t.startswith("nao"): return "nao"
    return None

def data(txt):
    m = re.match(r"~?(\d{4})(?:-(\d{2})-(\d{2}))?", (txt or "").strip())
    if not m: return None, None
    if m.group(2): return int(m.group(1)), f"date({int(m.group(1))},{int(m.group(2))},{int(m.group(3))})"
    return int(m.group(1)), None

def atom(s):
    return "'" + str(s).replace("\\", "\\\\").replace("'", "\\'") + "'"

def fracao(txt):
    t = norm(txt)
    m = re.search(r"(\d)/(\d)", t)
    if m: return f"concedido({m.group(1)}/{m.group(2)})"
    if t.startswith(("nao", "negado")): return "negado"
    return None

# ---------- leitura das fontes ----------
def registros():
    """Gera dicionários num formato comum, um por réu."""
    for fonte, arq in (("t5", "amostra_casos.csv"), ("t6", "amostra_t6_casos.csv"), ("contraste", "casos.csv")):
        for i, r in enumerate(csv.DictReader(open(D(arq), encoding="utf-8"))):
            if not norm(r.get("incluir", "")).startswith("sim"):
                continue
            ant = norm(r.get("antecedentes"))
            yield {
                "id": f"{fonte}_{r.get('registro') or r.get('id_caso')}_{i}", "fonte": fonte,
                "relator": r.get("relator") or r.get("relator_amostra", ""),
                "data_fato": r.get("data_fato"), "drogas": r.get("drogas"), "qtd": r.get("qtd_g"),
                "primario": sim_nao(r.get("primario")),
                "reincidente": "sim" if "reincident" in ant else None,
                "maus_antecedentes": "nao" if ant in ("bons", "nenhum") else ("sim" if ant and "primario" not in ant and "sem condenacao" not in ant else None),
                "antecedentes_txt": ant,
                "atos": sim_nao(r.get("atos_infracionais")), "atos_ano": r.get("ultimo_ato_infracional_ano"),
                "acoes_em_curso": "sim" if re.search(r"acoes? penais? em curso|ja preso|inquerito", ant + " " + norm(r.get("tj_fund_neg_p4"))) else None,
                "associacao": None,
                "texto_indicios": " ".join(r.get(c, "") for c in ("petrechos_dinheiro", "origem_abordagem", "marcadores_subjetivos", "tj_fund_neg_p4"))
                                   + (" local conhecido" if norm(r.get("local_conhecido")) == "sim" else ""),
                "texto_dinheiro": r.get("petrechos_dinheiro", ""),
                "fund_tj": r.get("tj_fund_neg_p4"), "majorante": r.get("majorante_art40"),
                "sent_p4": r.get("sent_p4"), "tj_p4": r.get("tj_p4"), "stj_p4": r.get("stj_p4"),
                "resultado": r.get("resultado_final_reu"),
            }
    for i, r in enumerate(csv.DictReader(open(D("amostra_p4_casos.csv"), encoding="utf-8"))):
        yield {
            "id": f"p4_{r['registro']}_{i}", "fonte": "p4", "relator": r.get("relator_amostra", ""),
            "data_fato": r.get("data_fato"), "drogas": r.get("drogas"), "qtd": r.get("qtd_g_total"),
            "primario": sim_nao(r.get("primario")), "reincidente": sim_nao(r.get("reincidente")),
            "maus_antecedentes": sim_nao(r.get("maus_antecedentes")), "antecedentes_txt": norm(r.get("antecedentes_desc")),
            "atos": sim_nao(r.get("atos_infracionais")), "atos_ano": r.get("ultimo_ato_infracional_ano"),
            "acoes_em_curso": sim_nao(r.get("acoes_penais_em_curso")),
            "associacao": "condenado" if norm(r.get("associacao_art35")) == "condenado" else None,
            "texto_indicios": " ".join(r.get(c, "") for c in ("petrechos", "outros_indicios_dedicacao", "tj_fundamentos_negar"))
                              + (" dinheiro" if r.get("dinheiro") else "") + (" arma" if norm(r.get("arma")) == "sim" else ""),
            "texto_dinheiro": "dinheiro" if r.get("dinheiro") else "",
            "fund_tj": r.get("tj_fundamentos_negar"), "majorante": r.get("majorante_art40"),
            "sent_p4": r.get("sent_p4"), "tj_p4": r.get("tj_p4"), "stj_p4": r.get("stj_final_p4"),
            "resultado": r.get("resultado_final_reu"),
        }

def discute_p4(r):
    return any((r.get(k) or "").strip() for k in ("sent_p4", "tj_p4", "stj_p4", "fund_tj")) or r["fonte"] == "p4"

def fatos(r):
    c, out = atom(r["id"]), []
    out.append(f"caso({c}, {r['fonte']}, {atom(r['relator'])}).")
    ano, dt = data(r["data_fato"])
    if dt: out.append(f"data_fato({c}, {dt}).")
    elif ano: out.append(f"ano_fato_informado({c}, {ano}).")
    for d in drogas(r["drogas"]): out.append(f"droga({c}, {d}).")
    q = numero(r["qtd"])
    if q is not None: out.append(f"qtd_g({c}, {q}).")
    fund = norm(r["fund_tj"])
    # fatos de status; o fundamento do TJ completa o que o texto fixou
    st = {"primario": r["primario"], "reincidente": r["reincidente"], "maus_antecedentes": r["maus_antecedentes"],
          "ato_infracional": r["atos"], "acoes_em_curso": r["acoes_em_curso"]}
    if not st["reincidente"] and "reincid" in fund: st["reincidente"] = "sim"
    if not st["maus_antecedentes"] and "maus_antecedentes" in fund.replace(" ", "_"): st["maus_antecedentes"] = "sim"
    if not st["ato_infracional"] and "atos infraciona" in fund.replace("_", " "): st["ato_infracional"] = "sim"
    if not st["acoes_em_curso"] and "acoes_em_curso" in fund.replace(" ", "_"): st["acoes_em_curso"] = "sim"
    if st["reincidente"] == "sim": st["primario"] = st["primario"] or "nao"
    for k, v in st.items():
        if v: out.append(f"{k}({c}, {v}).")
    m = re.search(r"(19|20)\d{2}", r.get("antecedentes_txt") or "")
    if m and st["maus_antecedentes"] == "sim": out.append(f"antecedente_ano({c}, {m.group()}).")
    a = numero(r["atos_ano"])
    if a: out.append(f"ultimo_ato_infracional({c}, {int(a)}).")
    if r["associacao"]: out.append(f"associacao({c}, {r['associacao']}).")
    t = norm(r["texto_indicios"])
    for k, p in INDICIOS.items():
        alvo = norm(r["texto_dinheiro"]) if k == "dinheiro" else t   # dinheiro: só o que foi apreendido
        if re.search(p, alvo): out.append(f"indicio({c}, {k}).")
    if len(drogas(r["drogas"])) >= 3: out.append(f"indicio({c}, variedade).")
    maj = norm(r["majorante"])
    if maj and maj != "nao":
        inc = re.match(r"(i|ii|iii|iv|v|vi|vii)\b", maj)
        out.append(f"majorante({c}, {inc.group(1) if inc else 'outra'}).")
    for inst in ("sent_p4", "tj_p4", "stj_p4"):
        f = fracao(r[inst])
        if f: out.append(f"referencia({c}, {inst}, {f}).")
    if r["resultado"]: out.append(f"referencia({c}, resultado, {atom(norm(r['resultado']))}).")
    return sorted(set(out), key=out.index)

def main():
    regs = [r for r in registros() if discute_p4(r)]
    os.makedirs(os.path.join(RAIZ, "prolog"), exist_ok=True)
    with open(os.path.join(RAIZ, "prolog", "fatos_casos.pl"), "w", encoding="utf-8") as f:
        f.write(":- encoding(utf8).\n")
        f.write("% Gerado por scripts/gerar_fatos.py a partir de dados/*.csv -- não editar à mão.\n")
        f.write("% Um bloco por réu em que o §4º foi discutido. Fato ausente = desconhecido.\n\n")
        for r in regs:
            f.write("\n".join(fatos(r)) + "\n\n")
    from collections import Counter
    print(len(regs), "réus ->", "prolog/fatos_casos.pl", dict(Counter(r["fonte"] for r in regs)))

if __name__ == "__main__":
    main()
