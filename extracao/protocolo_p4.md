# Extração da base do §4º (tráfico privilegiado, art. 33, §4º, Lei 11.343/2006)

Você recebe o texto de decisões do STJ (acórdãos e decisões monocráticas) de UM processo em que a defesa pediu o §4º. O objetivo é registrar os FATOS que a lei manda considerar (para comparar casos parecidos julgados por relatores diferentes) e o que cada instância decidiu sobre o §4º.

Regras: use SÓ o que está no texto (o relatório costuma transcrever a sentença e o acórdão do TJ). Campo sem informação = "" (vazio). Não deduza números. Se o texto disser algo só como alegação da defesa, registre em `obs`, não como fato.

## Um objeto por RÉU que pediu o §4º

Identificação
- processo: ex. "REsp 2117393" (classe original, sem AgRg/EDcl)
- relator, uf, reu, sexo (M | F)
- data_fato: "AAAA-MM-DD" ou ""

Fatos
- drogas: ex. "cocaina+maconha" (minúsculas, sem acento)
- qtd_g_total: total em gramas (número); "" se não houver peso
- qtd_por_droga: ex. "maconha 1200; cocaina 35"
- porcoes: texto curto
- petrechos: balança, embalagens, caderno de anotações etc. ("" se nada)
- dinheiro: valor em R$ ou ""
- arma: sim | nao | ""
- primario: sim | nao | ""
- reincidente: sim | nao | ""
- maus_antecedentes: sim | nao | "" (+ descrição curta em `antecedentes_desc`)
- atos_infracionais: sim | nao | ""; ultimo_ato_infracional_ano: AAAA ou ""
- acoes_penais_em_curso: sim | nao | ""
- associacao_art35: condenado | absolvido | nao_imputado | ""
- outros_indicios_dedicacao: o que mais a origem usou (ex. "investigacao previa", "denuncias anonimas", "conversas no celular", "local conhecido"); separe por ";"
- majorante_art40: "nao" ou o inciso

Decisões sobre o §4º
- sent_p4: nao | fração ("1/6", "2/3") | ""
- tj_p4: nao | fração | ""
- tj_fundamentos_negar: categorias separadas por ";" entre: quantidade | natureza | variedade | petrechos | dinheiro | atos_infracionais | acoes_em_curso | maus_antecedentes | reincidencia | associacao | investigacao_previa | denuncias | celular | outro:<texto>
- stj_mono_p4: o que a decisão monocrática do STJ fez (nao_conheceu | negou | concedeu <fração> | concedeu_oficio <fração> | "")
- stj_final_p4: resultado após o último acórdão (negado | concedido <fração> | concedido_oficio <fração> | redimensionado_fracao <fração>)
- stj_obice: Sum. 7 | Sum. 182 | Sum. 284/STF | Sum. 83 | HC substitutivo | nenhum | outro
- stj_analisou_merito: sim | nao
- stj_precedentes: precedentes-chave citados sobre o §4º (ex. "Tema 1139", "EREsp 1.916.596", "REsp 1.887.511", "HC 725.534"); separe por ";"
- stj_fundamento: 1 frase com a razão central do STJ
- quem_recorreu_ultimo: defesa | mp
- resultado_final_reu: favoravel | parcial | desfavoravel (para o RÉU, após o último acórdão)
- pena_final_m: pena final em MESES, se informada
- regime_final: fechado | semiaberto | aberto | ""
- votacao: unanime | maioria; vencidos
- obs: até 2 frases com o que for notável (ex. divergência entre o relator e a turma)

## Saída
Grave /tmp/claude-0/t6b/extracao/saidas_p4/saida_<registro>.json com {"casos":[...]} para cada arquivo. Depois responda com no máximo 4 linhas de dúvidas por processo.
