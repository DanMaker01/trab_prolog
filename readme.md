# trab_ia_justica: organização das pastas

```
STATUS.md              diário do projeto: decisões, achados, próximos passos
README.md              este arquivo

fontes/                tudo o que veio de fora, sem alteração
  json/                JSONs mensais da 5ª Turma do STJ (2026-06, 2026-07, 2026-08)
    sexta_turma/       JSONs mensais da 6ª Turma, mesmos meses (só acórdãos)
  stj/<registro>_<processo>/
                       um diretório por processo: PDFs (acórdãos, monocráticas, íntegras do DJe)
                       e o CSV exportado de https://consulta-processo.web.stj.jus.br/

leis/                  Código Penal e Lei de Drogas compilados (github.com/ctresb/leis, baixados em 13/10/2026)

extracao/              passo intermediário: texto e extração por IA
  protocolo_extracao.md   regras seguidas na extração (o mesmo de scripts/)
  textos/                 texto dos PDFs dos 40 sorteados, um .txt por registro
  saidas/                 JSON da extração (casos e teses) de cada um dos 40
  textos_contraste/       texto dos PDFs dos 14 casos de contraste (lidos à mão)

dados/                 tabelas finais
  casos.csv, teses.csv          14 casos de contraste, escolhidos à mão (qualitativos)
  amostra.csv                   os 40 sorteados (semente 2026)
  metadados.csv                 metadados de 52 processos (saída de ler_processos.py)
  amostra_casos.csv, amostra_teses.csv   extração dos 40 (coluna `incluir`)

scripts/
  ler_processos.py      fontes/stj/*/processo-*.csv  ->  dados/metadados.csv
  sortear_amostra.py    fontes/json/*.json           ->  dados/amostra.csv
  pdf_para_txt.py       PDFs de um processo          ->  um .txt sem duplicatas
  protocolo_extracao.md regras da extração por IA

_/                     pasta de entrada para novos downloads; depois de organizados em fontes/,
                       pode ser esvaziada.
```

Rodar os scripts sempre a partir da raiz do projeto, por exemplo `python scripts\ler_processos.py`.
