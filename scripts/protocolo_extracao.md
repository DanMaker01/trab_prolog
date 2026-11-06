# Extração de casos de tráfico (STJ, 5ª Turma)

Você recebe o texto de acórdãos do STJ (ementa, relatório, voto). Para CADA RÉU, gere uma linha de "caso"; para cada TESE discutida, uma linha de "tese". Use SÓ o que está no texto. Campo sem informação = "" (vazio). Não invente nem deduza números.

## Campos de caso (um objeto por réu)
- processo: ex. "HC 1037460" (classe original, sem AgRg/EDcl)
- via: HC | RHC | AREsp | REsp ; se for contra condenação definitiva, acrescente " (revisao criminal)" ou " (HC pos-transito)"
- data_fato: "AAAA-MM-DD" se o texto der a data do fato/prisão; senão ""
- uf
- relator
- reu: nome; sexo: M | F (pelo nome/texto)
- drogas: ex. "cocaina+maconha" (minúsculas, sem acento)
- qtd_g: total em gramas (número; some as drogas; kg→g); "" se só houver porções
- porcoes: texto curto, ex. "15 porcoes", "24 pinos + 42 pedras"
- petrechos_dinheiro: balança, dinheiro, celulares etc.
- majorante_art40: "nao" ou o inciso, ex. "III (escola)", "V (interestadual)"
- origem_abordagem: patrulhamento | denuncia anonima | investigacao | monitoramento | mandado | revista prisional | outro (texto curto)
- local_conhecido: sim | nao | "" (se o texto falar em "local conhecido pelo tráfico", "ponto de venda" etc.)
- comportamento_reu: o que o réu fez antes da abordagem, nas palavras do texto (ex. "mudou de direcao", "fugiu", "nervosismo", "atitude suspeita sem descricao")
- tipo_busca: pessoal | veicular | domiciliar | combinações com "+"
- consentimento: para busca domiciliar: quem autorizou, ou "nao"
- primario: sim | nao | ""
- antecedentes: "bons" | descrição curta (ex. "reincidente especifico", "roubo extinto em 2010")
- atos_infracionais: nao | sim (descrição curta); ultimo_ato_infracional_ano: AAAA ou ""
- marcadores_subjetivos: expressões sobre a pessoa/contexto social usadas na fundamentação (ex. "sem ocupacao licita", "conhecido no meio policial", "bairro X", "gangue"); separe por ";"
- parecer_mpf: favoravel | desfavoravel | "" (favorável/desfavorável AO RÉU)
- sent_pena_m, tj_pena_m, stj_pena_m: pena em MESES (número decimal; 5a10m10d = 70.3); "absolvido" se for o caso
- sent_regime, tj_regime, stj_regime: fechado | semiaberto | aberto
- sent_p4, tj_p4, stj_p4: nao | sim | fração ("1/6", "2/3")
- tj_fund_neg_p4: por que o §4º foi negado/reduzido na origem (curto)
- votacao: unanime | maioria ; vencidos: nomes
- resultado_final_reu: favoravel | parcial | desfavoravel  (do ponto de vista do RÉU, após o último acórdão)
- erro_tecnico_defesa: "" ou descrição (ex. "artigo errado", "sem cotejo analitico", "nao impugnou fundamento (Sum. 182)")
- obs: até 2 frases com o que for juridicamente notável

## Campos de tese (um objeto por tese)
- processo, reu
- tese: nulidade_busca_pessoal | nulidade_busca_domiciliar | p4 | desclassificacao_art28 | insignificancia | absolvicao_autoria | dosimetria_pena_base | regime | substituicao_prd | revisao_criminal_cabimento | outro:<nome>
- quem_alegou: defesa | mp
- obice: Sum. 7 | Sum. 182 | Sum. 284/STF | HC substitutivo | revisao criminal incabivel | nenhum | outro
- analisou_merito: sim | nao
- resultado_reu: favoravel | desfavoravel
- fundamento: 1 frase com a razão central do STJ

## Saída
Escreva um arquivo JSON em /tmp/claude-0/p4/saida_<registro>.json com {"casos":[...], "teses":[...]} para cada arquivo lido. Depois responda com uma lista curta de dúvidas/ambiguidades encontradas (máx. 5 linhas por processo).
