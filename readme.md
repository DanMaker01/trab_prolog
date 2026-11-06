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
  textos_contraste/       texto dos PDFs dos 14 casos de contraste (lidos à mão)

dados/                 tabelas finais
  casos.csv, teses.csv          14 casos de contraste, escolhidos à mão (qualitativos)
  amostra.csv                   40 sorteados da 5ª Turma
  amostra_t6.csv                40 sorteados da 6ª Turma
  metadados.csv                 metadados de todos os processos em fontes/stj (gerado por script)
  amostra_casos.csv, amostra_teses.csv   extração dos 40 da 5ª Turma (coluna `incluir`)

scripts/               rodar sempre a partir da raiz do projeto
  ler_processos.py      fontes/stj/*/processo-*.csv  ->  dados/metadados.csv
  sortear_amostra.py    JSONs de uma turma           ->  amostra sorteada
  pdf_para_txt.py       PDFs de cada processo        ->  um .txt por registro, sem duplicatas
  protocolo_extracao.md cópia do protocolo de extração

_/                     pasta de entrada para downloads novos; depois de organizados em fontes/, esvaziar
```

### Comandos

```
python scripts\ler_processos.py
python scripts\sortear_amostra.py fontes\json\*.json --n 40 --seed 2026 --manter-pre-condenacao --saida dados\amostra.csv
python scripts\sortear_amostra.py fontes\json\sexta_turma\*.json --n 40 --seed 2026 --saida dados\amostra_t6.csv
python scripts\pdf_para_txt.py fontes\stj extracao\textos
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

## 5. Amostra aleatória da 6ª Turma (40 sorteados)

- `dados/amostra_t6.csv`: 8 por relator (Carlos Pires Brandão, Nilsoni de Freitas, Og Fernandes, Rogerio Schietti, Sebastião Reis). Antonio Saldanha ficou fora da cota porque só tem 4 casos. O nome dos relatores é normalizado ("ROGERIO SCHIETTI CRUZ" = "ROGERIO SCHIETTI").
- **População:** 631 processos de tráfico. Os JSONs têm 2.538 (jun), 232 (jul) e 2.289 (ago) acórdãos.
- **Status:** esperando os CSVs e os PDFs. Strings de busca:
  - Carlos Pires: ARESP2981531 · ARESP3129963 · ARESP3165049 · ARESP3182130 · ARESP3243065 · ARESP3244452 · HC1065723 · RESP2255646
  - Nilsoni: ARESP2718305 · ARESP3185153 · ARESP3191865 · ARESP3224072 · ARESP3240954 · ARESP3252448 · HC1094990 · RESP2259260
  - Og Fernandes: ARESP3103548 · HC1075836 · HC1080301 · HC1090661 · HC936798 · RESP2178527 · RHC204466 · RHC235243
  - Schietti: ARESP2869502 · ARESP3139305 · ARESP3238765 · HC1057736 · HC1076501 · HC1086770 · HC1088909 · HC1089400
  - Sebastião Reis: ARESP3181652 · ARESP3216220 · ARESP3216334 · ARESP3264809 · ARESP3285685 · HC1093112 · HC1096435 · RESP2178919

---

## 6. Ideias para explorar

**Amostras mais variadas**
1. **Monocráticas (prioridade).** Sem elas, qualquer taxa calculada está distorcida (ver o "Cuidado" da seção 4).
2. ~~6ª Turma~~ (JSONs obtidos; amostra sorteada).
3. **Outros períodos (2024–2025):** efeito dos precedentes que mudaram as regras (HC 877.943, abr/2024, sobre busca pessoal; Tema 506, jun/2024, sobre 40 g de maconha; Tema 1139, sobre ações em curso). É a lei mudando por interpretação.
4. **Crime com critério mais objetivo** (ex.: furto e insignificância), para contrastar.
5. **Base 2, direcionada:** só acórdãos que analisaram o mérito do §4º ou da busca pessoal. É ela que alimenta a árvore A.

**Análises com o que já temos**
6. **Ementas em escala:** 844 de tráfico na 5ª Turma e cerca de 630 na 6ª. Regex para assunto, barreira processual, resultado e marcadores, usando os 40 extraídos como gabarito. Primeira comparação entre as turmas.
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
- `_/` ainda tem uma cópia dos 3 JSONs da 6ª Turma, que já estão em `fontes/json/sexta_turma/`. Pode apagar.
- `scripts/protocolo_extracao.md` e `extracao/protocolo_extracao.md` são iguais; o oficial é o de `extracao/`.
- `STATUS.md` foi incorporado a este README e pode ser apagado.

## 8. Próximos passos

1. Baixar os CSVs e PDFs dos 40 da 6ª Turma (seção 5) → metadados e extração com o mesmo protocolo.
2. Comparar a 5ª e a 6ª Turma (amostras e ementas em escala).
3. Tentar obter as monocráticas.
4. Conferir à mão 5 casos da extração por IA.
5. Fechar o dicionário de colunas (base: `extracao/protocolo_extracao.md`).
6. Montar a árvore A em Prolog a partir de `leis/`, já pensando no teste de sensibilidade.
