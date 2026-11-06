"""Junta os PDFs de cada processo (pasta _/) num único texto por registro, sem rodapés de assinatura
e sem documentos repetidos. Requer pdftotext (poppler).
Uso: python scripts/pdf_para_txt.py fontes/stj extracao/textos [registro ...]
O registro (12 dígitos) é lido do nome do arquivo ou, se não estiver lá, do nome da pasta.
Procura PDFs em subpastas também."""
import glob, hashlib, os, re, subprocess, sys

RODAPE = re.compile(r"Documento eletr|Signatário|Publicação no DJEN|Código de Controle|Assinado em|^\s*C5\d")

def texto_pdf(path):
    t = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    linhas = [re.sub(r" {2,}", " ", l).strip() for l in t.splitlines()]
    return "\n".join(l for l in linhas if l and not RODAPE.search(l))

def main(origem, destino, registros=None):
    os.makedirs(destino, exist_ok=True)
    por_reg = {}
    for p in sorted(glob.glob(os.path.join(origem, "**", "*.pdf"), recursive=True)):
        m = (re.search(r"(?<!\d)(\d{12})(?!\d)", os.path.basename(p))
             or re.search(r"(?<!\d)(\d{12})(?!\d)", os.path.basename(os.path.dirname(p))))
        if m and (not registros or m.group(1) in registros):
            por_reg.setdefault(m.group(1), []).append(p)
    for reg, pdfs in por_reg.items():
        vistos, partes = set(), []
        for p in pdfs:
            t = texto_pdf(p)
            h = hashlib.md5(t.encode()).hexdigest()
            if h in vistos:
                continue
            vistos.add(h)
            partes.append(f"########## {os.path.basename(p)}\n{t}")
        with open(os.path.join(destino, f"{reg}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(partes))
        print(reg, len(pdfs), "pdfs,", len(partes), "unicos")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], set(sys.argv[3:]) or None)
