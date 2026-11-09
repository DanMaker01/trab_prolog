# Trabalho IA e Justiça

**Tese:** uma IA que segue um protocolo formal (a lei) ainda pode produzir decisões enviesadas, porque os critérios de entrada são vagos ou socialmente carregados.

**Plano:** transformar a lei de drogas em uma árvore de decisão (Prolog), montar um banco de casos reais do STJ, passar os casos pela árvore e analisar os resultados.

Este arquivo é o único documento de acompanhamento do projeto: estrutura, decisões, achados e próximos passos. Última revisão: 06/11/2026.

---

## 1. Decisões de método

- **Recorte:** tráfico de drogas (Lei 11.343/2006, art. 33 e §4º), com o Código Penal como parte geral (arts. 33, 44, 59, 63–64).
- **Fora do recorte:** associação (art. 35) sem art. 33, prisão preventiva e outras cautelares, execução penal e casos anteriores à condenação (trancamento de ação ou de inquérito).
- **Fontes:**
  - JSONs mensais da 5ª e da 6ª Turma do STJ (jun, jul e ago/2026). Só trazem acórdãos.
  - CSV de cada processo, exportado de https://consulta-processo.web.stj.jus.br/: partes, advogados, UF, fases, recursos e trânsito.
  - PDFs dos acórdãos: fatos, penas e fundamentos.
- **Duas árvores (Prolog):**
  - **A:** escrita a partir da lei, o "juiz virtual".
  - **B:** aprendida a partir das decisões.
  - O trabalho compara as duas entre si e com os indicadores socioeconômicos.
- **Unidade de análise:** uma linha por réu (casos) e uma por tese (teses). Embargos de declaração e repetições do mesmo processo ficam de fora.
- **Alvo:** o resultado *para o réu* (favorável, parcial ou desfavorável), e não "provido/desprovido", porque às vezes quem recorre é o MP.
- **Lei no tempo:** coluna `data_fato`. A árvore A aplica a lei vigente na data do fato, salvo lei posterior mais benéfica (art. 2º do CP). Quando o texto não dá a data, usamos o ano da ação penal de 1º grau, marcado com "~".
- **Extração por IA:** os fatos e as teses das amostras foram extraídos por IA (Claude), seguindo `extracao/protocolo_extracao.md`. Isso precisa constar no trabalho, junto com uma conferência manual de parte dos casos.

---

## 2. Estrutura das pastas

```
README.md              este arquivo

fontes/                tudo o que veio de fora, sem alteração
  json/                JSONs da 5ª Turma (20260630, 20260731, 20260831)
    sexta_turma/       JSONs da 6ª Turma, mesmos meses
  stj/<registro>_<processo>/
                       um diretório por processo: PDFs (acórdãos, monocráticas, íntegras do DJe)
                       e processo-<registro>.csv exportado do site do STJ

leis/                  Código Penal e Lei de Drogas compilados (github.com/ctresb/leis,
                       baixados em 13/10/2026; última alteração incluída: Lei 15.517 de 22/9/2026)

extracao/              passo intermediário
  protocolo_extracao.md   regras da extração por IA (campos e valores permitidos)
  textos/                 texto dos PDFs dos 40 sorteados da 5ª Turma, um .txt por registro
  saidas/                 JSON da extração (casos e teses) de cada um dos 40
  textos_t6/, saidas_t6/  o mesmo para a amostra da 6ª Turma
  textos_contraste/       texto dos PDFs dos 14 casos de contraste (lidos à mão)

dados/                 tabelas finais
  casos.csv, teses.csv          14 casos de contraste, escolhidos à mão (qualitativos)
  amostra.csv                   40 sorteados da 5ª Turma
  amostra_t6.csv                40 sorteados da 6ª Turma
  amostra_t6_casos.csv, amostra_t6_teses.csv   extração da amostra da 6ª Turma (coluna `incluir`)
  metadados.csv                 metadados de todos os processos em fontes/stj (92 até agora; gerado por script)
  amostra_casos.csv, amostra_teses.csv   extração dos 40 da 5ª Turma (coluna `incluir`)
  ementas_t5.csv, ementas_t6.csv         todos os acórdãos de tráfico classificados pela ementa (gerado por script)

scripts/               rodar sempre a partir da raiz do projeto
  ler_processos.py      fontes/stj/*/processo-*.csv  ->  dados/metadados.csv
  sortear_amostra.py    JSONs de uma turma           ->  amostra sorteada
  pdf_para_txt.py       PDFs de cada processo        ->  um .txt por registro, sem duplicatas
  analisar_ementas.py   JSONs de uma turma           ->  dados/ementas_t*.csv (resultado, barreiras, marcadores)
  protocolo_extracao.md cópia do protocolo de extração

_/                     (criar quando precisar) pasta de entrada para downloads novos;
                       depois de organizados em fontes/, esvaziar
```

### Comandos

```
python scripts\ler_processos.py
python scripts\sortear_amostra.py fontes\json\*.json --n 40 --seed 2026 --manter-pre-condenacao --saida dados\amostra.csv
python scripts\sortear_amostra.py fontes\json\sexta_turma\*.json --n 40 --seed 2026 --saida dados\amostra_t6.csv
python scripts\pdf_para_txt.py fontes\stj extracao\textos
python scripts\analisar_ementas.py fontes\json\*.json --saida dados\ementas_t5.csv
python scripts\analisar_ementas.py fontes\json\sexta_turma\*.json --saida dados\ementas_t6.csv
```

Os dois sorteios são reproduzíveis: os comandos acima geram exatamente as amostras salvas. A opção `--manter-pre-condenacao` existe porque o sorteio da 5ª Turma foi feito antes do filtro de casos anteriores à condenação; ali, esses casos foram excluídos à mão (coluna `incluir`). O `pdf_para_txt.py` precisa do `pdftotext` (Poppler) instalado.

### Fluxo para um processo novo

1. No site do STJ, buscar `CLASSE+número` (ex.: `ARESP3187666`) ou o número de registro.
2. Baixar o CSV do processo, o "EMENTA / ACORDAO" e o "RELATORIO E VOTO" do acórdão mais recente. A monocrática só é necessária se o acórdão for curto. Embargos de declaração ficam de fora.
3. Salvar em `_/`. Depois, mover para `fontes/stj/<registro>_<processo>/`.

---

## 3. Achados qualitativos (14 casos escolhidos à mão)

Estes casos foram **escolhidos por contraste** e não são representativos. Servem como exemplos.

1. **Instâncias discordam:** os mesmos fatos recebem respostas diferentes em cada instância. No 1071846, no 3224879 e no 1082334, sentença, TJ e STJ discordaram sobre o §4º.
2. **Passado medido de forma desigual:** uma condenação de adulto com pena extinta há mais de 10 anos foi desconsiderada (1071846), enquanto atos infracionais de quando o réu era menor serviram para negar o §4º (3224879, 3013966).
3. **Pena alta para quantidade mínima:** no 3013966, 0,23 g de crack resultou em 5a10m de pena. O MPF pediu insignificância e não foi atendido. Os fundamentos usam marcadores subjetivos ("sem ocupação lícita", "gangue", família).
4. **Súmula 7 assimétrica:** ela pesa de forma diferente conforme quem recorre. No 2270993 (Ribeiro), a "revaloração jurídica" pedida pelo MP foi aceita e o §4º caiu. O mesmo argumento, vindo da defesa, foi rejeitado no 3252357 (Ribeiro) e no 3235521 (Messod).
5. **Mesmo juiz, duas leituras:** no 1052086, Joel considerou "próximos" de um crime de jan/2024 os atos infracionais de 2019 (nov/2025) e negou o §4º. Em abr/2026, sobre os mesmos fatos, considerou-os "distantes" e concedeu.
6. **Mesma abordagem, resultados opostos:** o 3027384 ("local de tráfico + mudança de direção + tentativa de evasão") terminou em condenação; o 3285713 ("local de tráfico + mudança de direção"), em absolvição.
7. **O mesmo fato recontado:** no 3027384, o TJRS chamou o fato de "mudou de direção" e "mera intuição policial". O STJ recontou como "manobra de evasão deliberada" e "bruscamente", acrescentou que o réu "portava uma bolsa" e usou a droga achada para "ratificar" a suspeita.
8. **Divergência na Turma:** o 985389 foi decidido por maioria (busca ilícita, absolvição), com Messod vencido. O voto vencido não foi publicado.
9. **Recursos do MP contra vitórias da defesa:** no 1082334, depois que o réu ganhou o §4º, o MP entrou com AgRg, EDcl, RE e ARE. Os resultados favoráveis ao réu são os menos estáveis.
10. **Erros nas ementas:** o 985389 cita "MP de SP" e "TJSP" num caso de GO em que o agravante é o MPF. O JSON não pode ser tratado como verdade absoluta.
11. **Tema 506 relativizado:** no 3187666, 12,19 g de maconha (abaixo dos 40 g do Tema 506) resultaram em 7a11m em regime fechado, por causa de 15 porções e do ambiente prisional. O recurso também caiu por erro técnico do advogado (artigo errado, Súm. 284).

---

## 4. Amostra aleatória da 5ª Turma (40 sorteados, todos extraídos)

- **Recorte:** 7 dos 40 ficam fora (art. 35 sem art. 33: 2; falsa médica: 1; cautelar: 2; antes da condenação: 2). Restam 33 processos, 34 réus e 109 teses.
- **Resultado para o réu:** 32 desfavoráveis, 2 parciais, nenhum totalmente favorável.
- **Mérito:** só 44 das 109 teses tiveram o mérito analisado, e 2 dessas foram favoráveis. A barreira mais comum é "HC substitutivo" (34 teses). Em 13 de 34 réus, o recurso veio depois do trânsito em julgado (HC ou revisão criminal).
- **Erro técnico da defesa** apontado pelo STJ: 21 de 34 réus (18 de 25 com advogado particular, 3 de 9 com a Defensoria).
- **Mérito analisado por relator:** Ribeiro 11/19, Reynaldo 12/26, Joel 9/20, Messod 7/24, Maria Marluce 5/20.
- **Metadados (40):** 32 com advogado particular e 8 com Defensoria. Todos os recursos ao STJ foram da defesa, e o MP recorreu depois em só 1. Todos unânimes. 35 já transitaram. Ações penais de 2012 a 2026.
- **Os fatos aparecem pouco:** droga 19/34, quantidade 13/34, primariedade 11/34, data do fato 4/34.
- **Marcadores subjetivos** aparecem em 12/34: "vulgo", nome da comunidade, "conhecido da polícia", facção, "bairro".

**Leitura:** na prática, o primeiro nó de decisão do STJ é processual, e não "o réu é primário?". Uma árvore B treinada nisso acerta cerca de 94% dizendo sempre "nega".

**Cuidado:** a amostra só tem acórdãos. Quando a defesa ganha na monocrática e o MP não agrava, o caso nunca vira acórdão. Por isso, a taxa desfavorável está inflada por construção (ver item 1 das ideias).

## 4b. Ementas em escala: 5ª × 6ª Turma (todos os acórdãos de tráfico, jun–ago/2026)

`scripts/analisar_ementas.py` classifica cada processo só pelo texto do JSON: quem recorreu, o dispositivo, o resultado para o réu, as barreiras e os marcadores. **Validação:** acertou o resultado para o réu em 32 de 33 casos da amostra extraída e em 11 de 12 casos de contraste. O erro conhecido é quando a ementa não diz que quem recorreu foi o MP (1082334). Na amostra da 6ª Turma, acertou 29 de 30; na base do §4º (Sebastião Reis), 16 de 19 depois da correção de 08/11 (antes, 13 de 19). O erro (AREsp 3285685) é uma vitória parcial na monocrática seguida de AgRg da defesa desprovido: a ementa só mostra o AgRg.

| | 5ª Turma | 6ª Turma |
|---|---|---|
| Processos | 879 | 678 |
| Resultado favorável ou parcial ao réu | 5,3% | 7,5% |
| **Defesa vence quando é ela que recorre** | **0,8% (7/836)** | **5,4% (36/661)** |
| Recurso do MP | 4,9% | 2,5% |
| Decisão por maioria | 0,2% | 2,2% |
| Súmula 7 citada | 54% | 52% |
| HC substitutivo citado | 32% | 24% |
| Súmula 182 citada | 17% | 23% |

**Por relator (defesa vence quando recorre):**
- 5ª Turma: Maria Marluce 2,1%, Ribeiro 2,1%, Messod 0%, Reynaldo 0%, Joel 0%.
- 6ª Turma: **Sebastião Reis 12,0%**, Og Fernandes 6,7%, Schietti 3,0%, Carlos Pires 0%, Nilsoni 0%.

**Leitura:** a mesma lei, no mesmo tribunal e no mesmo período, dá taxas diferentes conforme a turma e, dentro dela, conforme o relator sorteado. Na 5ª Turma, quase todo resultado favorável ao réu vem de recurso do MP que perdeu; a defesa quase nunca ganha. Na 6ª, a chance da defesa varia de 0% a 12% conforme o relator.

**Cuidados:**
- Só há acórdãos: monocráticas favoráveis sem agravo do MP não aparecem.
- A classificação é heurística.
- Os relatores recebem casos de tipos diferentes.

**Marcadores na ementa** (5ª / 6ª): facção 13% / 9%; fuga ou mudança de direção 9% / 8%; denúncia anônima 7% / 7%; local conhecido 5% / 5%; nervosismo 4% / 2%; atos infracionais 3% / 2%.

## 5. Amostra aleatória da 6ª Turma (40 sorteados, todos extraídos)

- `dados/amostra_t6.csv`: 8 por relator (Carlos Pires Brandão, Nilsoni de Freitas, Og Fernandes, Rogerio Schietti, Sebastião Reis). Antonio Saldanha ficou fora da cota porque só tem 4 casos. O nome dos relatores é normalizado ("ROGERIO SCHIETTI CRUZ" = "ROGERIO SCHIETTI").
- **População:** 631 processos de tráfico. Os JSONs têm 2.538 (jun), 232 (jul) e 2.289 (ago) acórdãos.
- **Extração:** 40 processos e 43 réus, em `dados/amostra_t6_casos.csv` e `dados/amostra_t6_teses.csv`.
  - 12 réus ficam fora do recorte: antes da condenação/preventiva/inquérito (5); ato infracional/ECA (2); art. 35 sem art. 33 (2); só organização criminosa, Lei 12.850 (2); art. 37, "olheiro" (1).
  - Restam 31 réus (30 processos) e 92 teses.
- **Resultado para o réu:** 29 desfavoráveis, 1 favorável e 1 parcial.
  - Favorável: REsp 2255646 (Carlos Pires), recurso do MP que perdeu; o §4º foi mantido.
  - Parcial: AREsp 3285685 (Sebastião Reis), confissão reconhecida na monocrática; o AgRg da defesa foi desprovido.
  - Por relator: Carlos Pires 4/5 desfavoráveis; Nilsoni 8/8; Og 4/4; Schietti 8/8; Sebastião Reis 5/6.
- **Mérito:** 29 das 92 teses tiveram o mérito analisado, e só 3 foram favoráveis. Barreiras: Súmula 7 (20), HC substitutivo (16), Súmula 182 (13), Súmula 284/STF (5).
- **Erro técnico da defesa:** 21 de 31 (particular 15/20, Defensoria 6/11).
- **Metadados:** 27 particular e 13 Defensoria. A defesa recorreu ao STF (RE) em 8 dos 40, bem mais que na 5ª Turma, e no AREsp 3185153 entrou com embargos de divergência. Em vários processos o relator mudou depois (redistribuição da convocada Nilsoni); para a análise vale o relator do acórdão (JSON).
- **Fatos disponíveis:** droga 17/31, quantidade 13/31, primariedade 6/31, data do fato 2/31. Marcadores em 15/31 ("namorada do líder", "membros de facção", "faz da traficância seu modus vivendi", "local conhecido como ponto de venda", "companheira de faccionado", "boca de fumo").
- **HC contra trânsito em julgado:** 3 dos 8 de Schietti são HC usados no lugar da revisão criminal, barrados de saída.
- **Leitura:** a amostra não separa os relatores. Com 6 a 8 casos por relator, uma taxa de 12% (Sebastião Reis nas ementas) dá zero vitórias em cerca de 1 de cada 3 sorteios. A diferença entre relatores tem que vir da base de ementas (seção 4b); a amostra serve para mostrar *como* se perde (barreiras, erro técnico, falta de dados para a lei).

## 6. Ideias para explorar

**Amostras mais variadas**
1. **Monocráticas (prioridade).** Sem elas, qualquer taxa calculada está distorcida (ver o "Cuidado" da seção 4).
2. ~~6ª Turma~~ (JSONs obtidos; amostra sorteada).
3. **Outros períodos (2024–2025):** efeito dos precedentes que mudaram as regras (HC 877.943, abr/2024, sobre busca pessoal; Tema 506, jun/2024, sobre 40 g de maconha; Tema 1139, sobre ações em curso). É a lei mudando por interpretação.
4. **Crime com critério mais objetivo** (ex.: furto e insignificância), para contrastar.
5. **Base 2, direcionada:** só acórdãos que analisaram o mérito do §4º ou da busca pessoal. É ela que alimenta a árvore A.

**Análises com o que já temos**
6. ~~Ementas em escala~~ (feito, seção 4b). Próximo: testar se a diferença entre relatores se mantém dentro do mesmo assunto (p. ex., só §4º).
7. **Sensibilidade da árvore A:** critérios vagos obrigam a escolher números (ex.: ato infracional a menos de X anos). Variar X e ver quem ganha ou perde o §4º. O caso 1052086 ilustra.
8. **Paradoxo da precisão na árvore B:** ela acerta cerca de 94% dizendo sempre "nega".
9. **Auditar a extração por IA:** conferir 5 casos à mão e medir a concordância.

**Outras fontes**
10. **DataJud (API pública do CNJ):** metadados de todos os tribunais, inclusive a 1ª instância.
11. **Estudos sobre o perfil dos processados por tráfico, com dados de raça** (há um do IPEA; confirmar): referência externa, porque o STJ não registra raça.

---

## 7. Pendências

- Contraste: PDFs não lidos de 994055, 2254195, 1062417 e 3164469 (registro 2026/0032892-0). O 1093945 (cautelar, fora do recorte) não tem CSV.
- 3189948 (amostra da 5ª Turma): só vieram os EDcl; falta o AgRg.
- `scripts/protocolo_extracao.md` e `extracao/protocolo_extracao.md` são iguais; o oficial é o de `extracao/`.

## 8. Próximos passos

1. ~~Amostra da 6ª Turma~~ (feito: 40/40, validação 29/30). Próximo: comparar as amostras das duas turmas lado a lado.
2. Árvore B com a base de ementas (teste rápido em 08/11: nos recursos da defesa, o 1º nó aprendido é "relator = Sebastião Reis?" e o 2º "relator = Og?"; acha 29 das 43 vitórias com 233 alarmes falsos). Refazer com cuidado.
3. **Base do §4º** (`dados/amostra_p4.csv`, gerada por `scripts/sortear_p4.py`, semente 2026): 99 processos em que a defesa pediu o §4º, de 10 relatores das duas turmas. Desenho caso-controle: entram todas as 19 vitórias da defesa e 8 derrotas sorteadas por relator (coluna `peso` para re-ponderar). Objetivo: extrair os fatos do texto integral (quantidade, antecedentes, atos infracionais) e testar se o relator continua decisivo com os fatos controlados.
   - JSONs de mar–mai/2026 (enviados em 08/11) não entram: têm poucas decisões por mês e taxa de vitória da defesa de 60%+, ou seja, parecem uma seleção, não o conjunto completo. Os de jan–fev vieram da 1ª Turma.
   - **Sebastião Reis (19 processos, 22 réus) extraído** → `dados/amostra_p4_casos.csv` (protocolo em `extracao/protocolo_p4.md`). Os fatos aparecem bem mais que nas outras amostras: droga 18/22, quantidade 14/22, primariedade 10/22, fundamento do TJ para negar o §4º 22/22 (quantidade em 13).
   - **Achado: o relator concede, a turma derruba.** Em 4 das 11 "vitórias" da ementa, Sebastião Reis tinha concedido o §4º na monocrática, o MP agravou e a Turma retirou o benefício. Em 3 delas ele ficou vencido (AREsp 2946226: 432 kg de maconha; HC 1060758: 308 kg; HC 1017077: 2 kg de cocaína, fração reduzida de 2/3 para 1/6). Mesmos fatos, mesma lei, resposta diferente conforme quem decide: o critério "não se dedicar a atividades criminosas" é lido de dois jeitos.
   - **Correção do `analisar_ementas.py`:** esses casos eram lidos como vitória da defesa (o agravo "provido" era do MP). Nova regra: agravo provido que cassa a monocrática / restabelece o acórdão / declara a minorante inaplicável = recurso do MP. Nova coluna `relator_vencido`. Efeito: Sebastião Reis cai de 12% para 10,8%; a diferença entre turmas continua (0,8% × 5,0%, p ≈ 10⁻⁶). Erro restante conhecido: HC 1017077 (redução da fração).
4. Tentar obter as monocráticas.
5. Conferir à mão 5 casos da extração por IA.
6. Fechar o dicionário de colunas (base: `extracao/protocolo_extracao.md`).
7. Montar a árvore A em Prolog a partir de `leis/`, já pensando no teste de sensibilidade.

## 9. Árvores em Prolog (09/11)

```
prolog/
  arvore_a.pl          árvore A: o § 4º como regras; critérios vagos = parâmetros de 3 perfis
  testes_arvore_a.pl   26 testes com casos sintéticos (plunit)
  experimento_a.pl     roda os 3 perfis sobre os réus reais -> resultados/arvore_a*.csv
  fatos_casos.pl       GERADO por scripts/gerar_fatos.py (63 réus em que o § 4º foi discutido)
  arvore_b.pl          GERADO por scripts/arvore_b.py: árvores aprendidas (com e sem relator)
  fatos_ementas.pl     GERADO: entradas dos 1.494 recursos da defesa
  pred_sklearn.pl      GERADO: previsões do scikit-learn, para o teste de equivalência
  testes_arvore_b.pl   confere que as regras em Prolog decidem igual ao modelo treinado
tex/trabalho.tex       subseções Metodologia e Experimentos Computacionais (esta ainda por escrever)
resultados/            saídas dos experimentos
```

Comandos (na raiz; requer SWI-Prolog e Python com pandas e scikit-learn):
```
python scripts/gerar_fatos.py
python scripts/arvore_b.py
swipl -g run_tests -t halt prolog/testes_arvore_a.pl
swipl -g run_tests -t halt prolog/testes_arvore_b.pl
swipl -g main -t halt prolog/experimento_a.pl
```
Consultas úteis: `swipl prolog/arvore_a.pl prolog/fatos_casos.pl` e depois
`explica(restritivo, 'p4_202501891953_10').`

- **Perfis da árvore A** (parametrizações ilustrativas, não retratos de ministros): `garantista`
  (quantidade só modula a fração), `intermediario` (quantidade grande + outro indício; atos
  infracionais até 3 anos; Tema 1.139), `restritivo` (quantidade sozinha basta; qualquer indício).
  O dado faltante (primariedade não informada etc.) é um eixo separado: a favor do réu ou contra.
- **Primeira rodada (sem análise ainda):** com dado faltante a favor do réu, concedem o § 4º
  57/63 (garantista), 26/63 (intermediário) e 7/63 (restritivo); os perfis discordam em 50 dos 63.
  Com o dado faltante contra o réu: 13, 4 e 0.
- **Árvore B:** a raiz é "classe = REsp"; no modelo com relator, os nós seguintes são relatores
  (Sebastião Reis, Maria Marluce, Og Fernandes). Sem relator, ela passa a usar marcadores da
  ementa (fuga, denúncia anônima, local conhecido).
- **Opinião externa sobre o modelo preditivo (registro):** adotados a lista de variáveis com
  vazamento, a validação "deixa um relator fora" e a prioridade à interpretabilidade. Não
  adotados, por ora: prever o § 4º com ~60 casos (poucas vitórias) e a comparação com regressão
  logística/McNemar. Podem entrar quando a base do § 4º estiver completa.

## 10. Experimentos (09/11)

Rodar, na raiz: `swipl -g main -t halt prolog/experimentos.pl` e depois `python scripts/experimentos.py`.
Saídas em `resultados/` (CSVs, `experimentos.json` e as tabelas `tab_*.tex`, incluídas no `tex/trabalho.tex`).

- **E1 (mesma lei, leituras diferentes):** 63 réus; com fato faltante a favor do réu, a redução sai para
  57 (garantista), 26 (intermediária) e 7 (restritiva); as leituras discordam em 50; a pena do mesmo réu
  varia em média 26 meses (até 47). Com o fato faltante contra o réu: 13, 4 e 0. A escolha que mais pesa
  é QUAIS indícios contam (muda até 24 réus), depois QUANTOS bastam (13).
- **E2 (mesmo processo, dois julgamentos):** nos 4 casos em que Sebastião Reis deu a redução sozinho e a
  Turma tirou, o relator coincide com a leitura garantista e a Turma com a intermediária/restritiva.
- **E3 (o que a árvore aprendida aprende):** depois de "é REsp?", todas as perguntas são sobre o relator.
  Trocando só o relator, a resposta muda em 292 de 1.494 processos. Acha 27/40 vitórias com 171 alarmes falsos.
- **E4 (juiz virtual x tribunais):** a leitura restritiva é a que mais coincide com o STJ (41/52), mas o STJ
  negou em 42/52: concordar com ele é, sobretudo, negar.
- `tex/trabalho.tex` reescrito em linguagem comum, com "fichas" de cada tabela (o que é a linha, quantas, colunas).
