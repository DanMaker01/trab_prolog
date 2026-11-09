"""Visualizador simples das árvores (pygame).

Uso (na raiz do projeto; precisa de SWI-Prolog e de: pip install pygame pandas scikit-learn):
  python scripts/ver_arvore.py

Teclas:
  TAB        troca entre o juiz virtual (árvore A) e a árvore aprendida (árvore B)
  ← →        réu / processo anterior e seguinte
  ↑ ↓        troca a leitura da lei (só na árvore A)
  T          só os réus inventados dos testes  /  todos
  ESC        sair

Ao abrir, roda os testes em Prolog e mostra o resultado no topo da tela.
"""
import os, re, subprocess, sys
import pygame

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PROLOG = os.path.join(RAIZ, "prolog")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BRANCO, PRETO, CINZA = (250, 250, 250), (30, 30, 30), (170, 170, 170)
VERDE, VERMELHO, AMARELO, AZUL = (60, 160, 80), (200, 70, 60), (220, 170, 40), (60, 110, 200)
L, A = 1100, 720


# ---------------- dados ----------------
def swipl(*args):
    r = subprocess.run(["swipl", *args], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8")
    return r.stdout + r.stderr

def rodar_testes():
    """Roda cada arquivo de testes. O código de saída do swipl diz se passou (0) ou não;
    o número de testes vem do resumo, que muda de formato entre versões do SWI-Prolog
    (ex.: "All 26 tests passed" ou "All 14 (+12 sub-tests) tests passed")."""
    linhas = []
    for f in ("testes_arvore_a.pl", "testes_arvore_b.pl", "testes_casos_reais.pl"):
        r = subprocess.run(["swipl", "-g", "run_tests", "-t", "halt", os.path.join("prolog", f)],
                           cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace")
        s = r.stdout + r.stderr
        n = re.search(r"All ([\d,]+)(?: \(\+([\d,]+) sub-tests\))? tests passed", s)
        total = (int(n.group(1).replace(",", "")) + int((n.group(2) or "0").replace(",", ""))) if n else None
        if r.returncode == 0:
            linhas.append(f"{f}: {total if total else ''} ok".replace(":  ok", ": ok"))
        else:
            linhas.append(f"{f}: FALHOU (rode no terminal: swipl -g run_tests -t halt prolog/{f})")
    return linhas

def caminhos_a():
    """Uma linha por réu x leitura, vinda de prolog/exporta_caminhos.pl."""
    s = swipl("-g", "main", "-t", "halt", os.path.join("prolog", "exporta_caminhos.pl"))
    casos = {}
    for l in s.splitlines():
        p = l.split("\t")
        if len(p) != 9:
            continue
        c, leitura, lei, *req, dec, ind = p
        casos.setdefault(c, {})[leitura] = {"lei": lei, "req": req, "dec": dec, "ind": ind}
    return casos

def arvore_b():
    import arvore_b as B
    from sklearn.tree import DecisionTreeClassifier
    d = B.carregar(); X = B.matriz(d, True)
    m = DecisionTreeClassifier(**B.PARAMS).fit(X, d.y)
    return m.tree_, list(X.columns), d, X


# ---------------- desenho ----------------
def caixa(tela, fonte, texto, x, y, cor, largura=230):
    r = pygame.Rect(0, 0, largura, 44); r.center = (x, y)
    pygame.draw.rect(tela, cor, r, border_radius=8)
    pygame.draw.rect(tela, PRETO, r, 2, border_radius=8)
    for i, linha in enumerate(texto.split("\n")):
        t = fonte.render(linha, True, PRETO)
        tela.blit(t, t.get_rect(center=(x, y - 8 * (len(texto.split("\n")) - 1) + 16 * i)))
    return r

def seta(tela, a, b, cor, rotulo, fonte):
    pygame.draw.line(tela, cor, a, b, 3)
    t = fonte.render(rotulo, True, cor)
    tela.blit(t, ((a[0] + b[0]) // 2 + 6, (a[1] + b[1]) // 2 - 10))

PERGUNTAS = [("lei", "Fato depois da\nLei de 2006?"), (0, "É primário?"), (1, "Bons antecedentes?"),
             (2, "Não se dedica a\natividades criminosas?"), (3, "Não integra\norganização criminosa?")]

def desenha_a(tela, f, fp, caso, leitura, dados):
    x, y0, dy = 330, 150, 90
    falhou = False
    for i, (chave, texto) in enumerate(PERGUNTAS):
        y = y0 + i * dy
        if chave == "lei":
            v = "atende" if dados["lei"] == "lei_11343" else "nao_atende"
        else:
            v = dados["req"][chave]
        cor = CINZA if falhou else {"atende": VERDE, "nao_atende": VERMELHO}.get(v, AMARELO)
        caixa(tela, f, texto, x, y, cor)
        if not falhou:
            if v == "nao_atende":
                caixa(tela, f, "NEGA a redução", x + 330, y, VERMELHO, 200)
                seta(tela, (x + 115, y), (x + 230, y), VERMELHO, "não", fp)
                falhou = True
            elif v == "desconhecido":
                t = fp.render("não informado no processo: conta conforme a política de dado faltante", True, AMARELO)
                tela.blit(t, (x + 125, y - 8))
        if i < len(PERGUNTAS) - 1:
            seta(tela, (x, y + 22), (x, y + dy - 22), CINZA if falhou else VERDE, "sim", fp)
    if not falhou:
        y = y0 + len(PERGUNTAS) * dy
        txt = dados["dec"].replace("concede", "CONCEDE ").replace("(", "").replace(")", "") if "concede" in dados["dec"] else "NEGA (dado faltante)"
        caixa(tela, f, txt, x, y, VERDE if "concede" in dados["dec"] else VERMELHO)
    tela.blit(f.render(f"Réu: {caso}", True, PRETO), (20, 60))
    tela.blit(f.render(f"Leitura: {leitura}   (↑ ↓ troca)", True, AZUL), (20, 84))
    tela.blit(fp.render(f"Decisão: {dados['dec']}    indicadores de dedicação: {dados['ind']}", True, PRETO), (20, A - 30))

def desenha_b(tela, f, fp, arv, nomes, x_linha, n_proc, real):
    folhas = []
    def ordem(i):
        if arv.children_left[i] == -1 or uma_classe(i):
            folhas.append(i); return
        ordem(arv.children_left[i]); ordem(arv.children_right[i])
    def uma_classe(i):
        cl = set()
        def junta(j):
            if arv.children_left[j] == -1:
                v = arv.value[j][0]; cl.add(v[1] > v[0])
            else:
                junta(arv.children_left[j]); junta(arv.children_right[j])
        junta(i); return len(cl) == 1
    ordem(0)
    pos = {}
    def posicao(i, prof):
        if i in folhas:
            pos[i] = (80 + folhas.index(i) * (L - 160) // max(1, len(folhas) - 1), 120 + prof * 120)
        else:
            posicao(arv.children_left[i], prof + 1); posicao(arv.children_right[i], prof + 1)
            pos[i] = ((pos[arv.children_left[i]][0] + pos[arv.children_right[i]][0]) // 2, 120 + prof * 120)
    posicao(0, 0)
    # caminho do processo escolhido
    caminho, i = [0], 0
    while i not in folhas:
        i = arv.children_right[i] if x_linha[arv.feature[i]] > 0.5 else arv.children_left[i]
        caminho.append(i)
    for i in pos:
        if i not in folhas:
            for filho, rot in ((arv.children_left[i], "não"), (arv.children_right[i], "sim")):
                cor = AZUL if (i in caminho and filho in caminho) else CINZA
                seta(tela, pos[i], pos[filho], cor, rot, fp)
    for i, (x, y) in pos.items():
        if i in folhas:
            v = arv.value[i][0]; vence = v[1] > v[0]
            caixa(tela, fp, ("vence" if vence else "perde"), x, y, VERDE if vence else VERMELHO, 90)
        else:
            nome = nomes[arv.feature[i]].replace("=", " = ") + "?"
            caixa(tela, fp, nome[:30], x, y, AZUL if i in caminho else BRANCO, 200)
    tela.blit(f.render(f"Processo {n_proc}   (resultado real: {real})", True, PRETO), (20, 60))
    tela.blit(fp.render("Árvore aprendida (com relator). Caminho deste processo em azul.", True, AZUL), (20, 84))


# ---------------- laço ----------------
def main():
    pygame.init()
    tela = pygame.display.set_mode((L, A)); pygame.display.set_caption("Juiz virtual x árvore aprendida")
    f, fp = pygame.font.SysFont("arial", 18), pygame.font.SysFont("arial", 14)
    tela.fill(BRANCO); tela.blit(f.render("Rodando os testes e o Prolog...", True, PRETO), (20, 20)); pygame.display.flip()
    testes = rodar_testes()
    casos = caminhos_a()
    arv, nomes, dB, XB = arvore_b()
    leituras = ["garantista", "intermediario", "restritivo"]
    modo, k, j, kb, so_testes = "A", 0, 0, 0, False
    relogio = pygame.time.Clock()
    while True:
        lista = [c for c in casos if (c.startswith("t_") or not so_testes)]
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                pygame.quit(); return
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_TAB: modo = "B" if modo == "A" else "A"
                if ev.key == pygame.K_t: so_testes, k = not so_testes, 0
                if ev.key in (pygame.K_RIGHT, pygame.K_LEFT):
                    d = 1 if ev.key == pygame.K_RIGHT else -1
                    if modo == "A": k = (k + d) % len(lista)
                    else: kb = (kb + d) % len(dB)
                if ev.key in (pygame.K_UP, pygame.K_DOWN):
                    j = (j + (1 if ev.key == pygame.K_DOWN else -1)) % 3
        tela.fill(BRANCO)
        tela.blit(fp.render("Testes: " + "   |   ".join(testes), True, VERDE if all("ok" in t for t in testes) else VERMELHO), (20, 10))
        tela.blit(fp.render("TAB troca de árvore   ← → próximo   ↑ ↓ leitura   T só réus de teste   ESC sai", True, CINZA), (20, 32))
        if modo == "A":
            c = lista[k % len(lista)]
            desenha_a(tela, f, fp, c, leituras[j], casos[c][leituras[j]])
        else:
            r = dB.iloc[kb]
            desenha_b(tela, f, fp, arv, nomes, XB.iloc[kb].values, f"{r.processo} - {r.relator} - {r.turma}",
                      "vence" if r.y else "perde")
        pygame.display.flip(); relogio.tick(30)

if __name__ == "__main__":
    main()
