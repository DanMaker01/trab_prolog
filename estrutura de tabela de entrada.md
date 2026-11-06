# Colunas para Tabela de Dados de Treinamento da IA (Juiz Criminal em Prolog)

Com base no arquivo de consultas derivado do Título III do CPP (Ação Penal), a tabela de treinamento deve capturar **todos os atributos necessários para que cada consulta possa ser respondida**. Abaixo, as colunas organizadas por bloco temático, indicando tipo de dado e a qual consulta/artigo se refere.

---

## 1. Identificação do Caso

| Coluna | Tipo | Descrição | Artigo/Consulta |
|---|---|---|---|
| `id_caso` | INTEGER (PK) | Identificador único do caso | — |
| `data_fato` | DATE | Data do fato criminoso | — |
| `tipo_crime` | TEXT | Homicídio, lesão corporal, contravenção, etc. | Art. 24, 26 |
| `crime_com_violencia_ou_grave_ameaca` | BOOLEAN | Se houve violência/grave ameaça | Art. 28-A, caput |
| `pena_minima_cominada_anos` | REAL | Pena mínima do delito (em anos) | Art. 28-A, caput e §1º |
| `causas_aumento_anos` | REAL | Soma das causas de aumento | Art. 28-A, §1º |
| `causas_diminuicao_anos` | REAL | Soma das causas de diminuição | Art. 28-A, §1º |

---

## 2. Espécie de Ação Penal (Art. 24, 26)

| Coluna | Tipo | Descrição | Consulta |
|---|---|---|---|
| `especie_acao_penal` | TEXT | `publica` / `privada` | `acao_publica_promovida_por/1` |
| `condicao_acao_publica` | TEXT | `requisicao_ministro_justica`, `representacao_ofendido`, `representacao_representante_legal`, `nenhuma` | `acao_publica_dependente/1` |
| `crime_contra_ente_publico` | BOOLEAN | Se o crime atinge patrimônio/interesse da União, Estado ou Município | Art. 24, §2º |
| `ente_publico_atingido` | TEXT | `uniao` / `estado` / `municipio` / `nenhum` | `ente_publico/1` |
| `acao_penal_contravencao` | TEXT | `auto_prisao_flagrante`, `portaria_autoridade_judiciaria`, `portaria_autoridade_policial`, `n/a` | `acao_penal_contravencao/1` |

---

## 3. Ofendido e Legitimidade (Art. 24, §1º; 30; 31; 33; 34; 36; 37)

| Coluna | Tipo | Descrição | Consulta |
|---|---|---|---|
| `ofendido_vivo` | BOOLEAN | Se o ofendido está vivo | Art. 24, §1º / 31 |
| `ofendido_declarado_ausente` | BOOLEAN | Ausência declarada judicialmente | Art. 24, §1º / 31 |
| `grau_parentesco_representante` | TEXT | `conjuge`, `ascendente`, `descendente`, `irmao`, `nenhum` | `legitimado_representacao_morte/1` |
| `ofendido_idade` | INTEGER | Idade do ofendido | Art. 33 / 34 |
| `ofendido_mentalmente_enfermo` | BOOLEAN | Condição mental | Art. 33 |
| `ofendido_retardado_mental` | BOOLEAN | Condição mental | Art. 33 |
| `tem_representante_legal` | BOOLEAN | Se possui representante legal | Art. 33 |
| `interesses_colidem` | BOOLEAN | Se interesses do representante colidem com os do ofendido | Art. 33 |
| `titular_queixa` | TEXT | `ofendido`, `representante_legal`, `curador_especial`, `ambos` | `titular_queixa_menor_21_maior_18/1` |
| `tipo_pessoa_juridica` | TEXT | `fundacao`, `associacao`, `sociedade`, `n/a` | `pode_exercer_acao_penal/1` |
| `forma_representacao_pj` | TEXT | `contrato_ou_estatuto`, `diretores_ou_socios_gerentes`, `n/a` | `representacao_pessoa_juridica/1` |
| `multiplicidade_titulares_queixa` | BOOLEAN | Se há mais de um titular do direito de queixa | Art. 36 |
| `titular_queixa_preferencial` | TEXT | `conjuge`, `ascendente`, `descendente`, `irmao` | `preferencia_queixa/1` |
| `desistencia_instancia` | BOOLEAN | Se houve desistência | `prosseguimento_por_outro_titular` |
| `abandono_acao` | BOOLEAN | Se houve abandono | `prosseguimento_por_outro_titular` |

---

## 4. Representação e Queixa (Art. 25; 32; 38; 39; 44)

| Coluna | Tipo | Descrição | Consulta |
|---|---|---|---|
| `denuncia_oferecida` | BOOLEAN | Se a denúncia já foi oferecida | `representacao_irretratavel` |
| `forma_representacao` | TEXT | `pessoalmente`, `por_procurador_com_poderes_especiais` | `forma_representacao/1` |
| `meio_representacao` | TEXT | `escrita`, `oral` | `meio_representacao/1` |
| `destinatario_representacao` | TEXT | `juiz`, `orgao_ministerio_publico`, `autoridade_policial` | `destinatario_representacao/1` |
| `data_ciencia_autoria` | DATE | Data em que soube quem é o autor | Art. 38 |
| `data_exercicio_queixa_ou_representacao` | DATE | Data em que exerceu o direito | Art. 38 |
| `crime_violencia_domestica_mulher` | BOOLEAN | Se é crime de violência doméstica/familiar contra a mulher | Art. 38, §2º |
| `comprovacao_pobreza` | BOOLEAN | Se comprovou pobreza | Art. 32 |
| `tipo_prova_pobreza` | TEXT | `atestado_autoridade_policial`, `outro`, `n/a` | `prova_pobreza/1` |
| `queixa_por_procurador` | BOOLEAN | Se a queixa foi por procurador | Art. 44 |
| `procurador_poderes_especiais` | BOOLEAN | Se tem poderes especiais | Art. 44 |
| `nome_querelante_no_mandato` | BOOLEAN | Se consta no mandato | Art. 44 |
| `mencao_fato_criminoso_mandato` | BOOLEAN | Se consta no mandato | Art. 44 |

---

## 5. ANPP – Acordo de Não Persecução Penal (Art. 28-A)

| Coluna | Tipo | Descrição | Consulta |
|---|---|---|---|
| `caso_de_arquivamento` | BOOLEAN | Se é caso de arquivamento | `cabivel_anpp` |
| `confissao_formal_e_circunstancial` | BOOLEAN | Confissão do investigado | `cabivel_anpp` |
| `necessario_e_suficiente` | BOOLEAN | Reprovação e prevenção | `cabivel_anpp` |
| `transacao_penal_jecrim_cabivel` | BOOLEAN | Vedação I | `vedacao_anpp_aplicavel` |
| `investigado_reincidente` | BOOLEAN | Vedação II | `vedacao_anpp_aplicavel` |
| `conduta_criminal_habitual` | BOOLEAN | Vedação II (habitual/reiterada/profissional) | `vedacao_anpp_aplicavel` |
| `infracoes_pretéritas_insignificantes` | BOOLEAN | Exceção à vedação II | `vedacao_anpp_aplicavel` |
| `beneficiado_5_anos_anteriores` | BOOLEAN | Vedação III | `vedacao_anpp_aplicavel` |
| `tipo_beneficio_anterior` | TEXT | `anpp`, `transacao_penal`, `suspensao_condicional`, `nenhum` | Art. 28-A, §2º, III |
| `anpp_formalizado_escrito` | BOOLEAN | Requisito §3º | `anpp_formalizado` |
| `assinado_mp` | BOOLEAN | Requisito §3º | `anpp_formalizado` |
| `assinado_investigado` | BOOLEAN | Requisito §3º | `anpp_formalizado` |
| `assinado_defensor` | BOOLEAN | Requisito §3º | `anpp_formalizado` |
| `audiencia_realizada` | BOOLEAN | Requisito §4º | `homologacao_anpp` |
| `voluntariedade_verificada` | BOOLEAN | Requisito §4º | `homologacao_anpp` |
| `legalidade_verificada` | BOOLEAN | Requisito §4º | `homologacao_anpp` |
| `condicoes_inadequadas` | BOOLEAN | §5º | `devolucao_anpp_mp` |
| `condicoes_insuficientes` | BOOLEAN | §5º | `devolucao_anpp_mp` |
| `condicoes_abusivas` | BOOLEAN | §5º | `devolucao_anpp_mp` |
| `anpp_homologado` | BOOLEAN | §6º | `execucao_anpp` |
| `remessa_mp_para_execucao` | BOOLEAN | §6º | `execucao_anpp` |
| `requisitos_legais_atendidos` | BOOLEAN | §7º | `recusa_homologacao` |
| `descumprimento_condicao_anpp` | BOOLEAN | §10 | `rescisao_anpp_e_denuncia` |
| `comunicacao_juizo` | BOOLEAN | §10 | `rescisao_anpp_e_denuncia` |
| `cumprimento_integral_anpp` | BOOLEAN | §13 | `extincao_punibilidade_anpp` |
| `decreto_juizo_competente` | BOOLEAN | §13 | `extincao_punibilidade_anpp` |
| `recusa_mp_em_propor_anpp` | BOOLEAN | §14 | `remessa_orgao_superior` |
| `requerimento_investigado` | BOOLEAN | §14 | `remessa_orgao_superior` |
| `finalidade_inciso_III_paragrafo_2` | BOOLEAN | §12 (exceção à não constância em certidão) | `anpp_nao_consta_certidao` |

---

## 6. Ação Privada Subsidiária (Art. 29)

| Coluna | Tipo | Descrição | Consulta |
|---|---|---|---|
| `acao_publica_nao_intentada_no_prazo` | BOOLEAN | Requisito | `cabivel_acao_privada_subsidiaria` |
| `mp_aditou_queixa` | BOOLEAN | Atribuição | `atribuicao_mp_acao_subsidiaria` |
| `mp_repudiou_queixa` | BOOLEAN | Atribuição | `atribuicao_mp_acao_subsidiaria` |
| `mp_ofereceu_denuncia_substitutiva` | BOOLEAN | Atribuição | `atribuicao_mp_acao_subsidiaria` |
| `mp_interveio_todos_termos` | BOOLEAN | Atribuição | `atribuicao_mp_acao_subsidiaria` |
| `mp_forneceu_elementos_prova` | BOOLEAN | Atribuição | `atribuicao_mp_acao_subsidiaria` |
| `mp_interpos_recurso` | BOOLEAN | Atribuição | `atribuicao_mp_acao_subsidiaria` |
| `mp_retomou_acao_parte_principal` | BOOLEAN | Atribuição | `atribuicao_mp_acao_subsidiaria` |

---

## 7. Denúncia e Queixa – Conteúdo e Prazos (Art. 41; 42; 46; 47)

| Coluna | Tipo | Descrição | Consulta |
|---|---|---|---|
| `exposicao_fato_criminoso` | BOOLEAN | Requisito Art. 41 | `conteudo_denuncia_ou_queixa` |
| `qualificacao_acusado` | BOOLEAN | Requisito Art. 41 | `conteudo_denuncia_ou_queixa` |
| `classificacao_crime` | BOOLEAN | Requisito Art. 41 | `conteudo_denuncia_ou_queixa` |
| `rol_testemunhas_necessario` | BOOLEAN | Requisito Art. 41 | `conteudo_denuncia_ou_queixa` |
| `reu_preso` | BOOLEAN | Status do réu | `prazo_denuncia/1` |
| `reu_solto_ou_afiancado` | BOOLEAN | Status do réu | `prazo_denuncia/1` |
| `data_recebimento_autos_mp` | DATE | Início do prazo | Art. 46 |
| `data_oferecimento_denuncia` | DATE | Para cálculo do prazo | Art. 46 |
| `mp_requisitou_esclarecimentos` | BOOLEAN | Art. 47 | `mp_pode_requisitar` |

---

## 8. Queixa – Indivisibilidade, Renúncia e Perdão (Art. 48–59)

| Coluna | Tipo | Descrição | Consulta |
|---|---|---|---|
| `queixa_contra_um_autor` | BOOLEAN | Art. 48 | `queixa_indivisivel` |
| `processo_de_todos_autores` | BOOLEAN | Art. 48 | `queixa_indivisivel` |
| `renuncia_em_relacao_a_um_autor` | BOOLEAN | Art. 49 | `renuncia_estende_a_todos` |
| `renuncia_expressa_assinada` | BOOLEAN | Art. 50 | `renuncia_expressa` |
| `perdao_concedido_a_um_querelado` | BOOLEAN | Art. 51 | `perdao_aproveita_a_todos` |
| `recusa_perdao_por_querelado` | BOOLEAN | Art. 51 | `perdao_aproveita_a_todos` |
| `querelante_menor_21_maior_18` | BOOLEAN | Art. 52 | `perdao_por_menor_21_maior_18` |
| `perdao_pelo_querelante` | BOOLEAN | Art. 52 | `perdao_por_menor_21_maior_18` |
| `perdao_pelo_representante` | BOOLEAN | Art. 52 | `perdao_por_menor_21_maior_18` |
| `oposicao_da_outra_parte` | BOOLEAN | Art. 52 | `perdao_por_menor_21_maior_18` |
| `querelado_mentalmente_enfermo_ou_retardado` | BOOLEAN | Art. 53 | `aceitacao_perdao_pelo_curador` |
| `curador_nomeado_juiz` | BOOLEAN | Art. 53 | `aceitacao_perdao_pelo_curador` |
| `querelado_menor_21` | BOOLEAN | Art. 54 | `aceitacao_perdao_menor_21` |
| `perdao_por_procurador_poderes_especiais` | BOOLEAN | Art. 55 | `perdao_aceito_por_procurador` |
| `perdao_extraprocessual_expresso` | BOOLEAN | Art. 56 | `perdao_extraprocessual_expresso` |
| `renuncia_tacita` | BOOLEAN | Art. 57 | `renuncia_tacita_admite_todos_meios_prova` |
| `perdao_tacito` | BOOLEAN | Art. 57 | `perdao_tacito_admite_todos_meios_prova` |
| `intimacao_querelado_perdao` | BOOLEAN | Art. 58 | `aceitacao_perdao_no_prazo` |
| `manifestacao_em_3_dias` | BOOLEAN | Art. 58 | `aceitacao_perdao_no_prazo` |
| `silencio_por_3_dias` | BOOLEAN | Art. 58 | `aceitacao_perdao_por_silencio` |
| `perdao_aceito` | BOOLEAN | Art. 58, § único | `extincao_punibilidade_perdao` |
| `aceitacao_fora_processo_assinada` | BOOLEAN | Art. 59 | `aceitacao_perdao_fora_processo` |

---

## 9. Perempção da Ação Penal Privada (Art. 60)

| Coluna | Tipo | Descrição | Consulta |
|---|---|---|---|
| `somente_mediante_queixa` | BOOLEAN | Requisito | `perempcao_acao_penal` |
| `iniciada_acao` | BOOLEAN | Hipótese I | `hipotese_perempcao` |
| `querelante_inacao_30_dias_seguidos` | BOOLEAN | Hipótese I | `hipotese_perempcao` |
| `falecimento_ou_incapacidade_querelante` | BOOLEAN | Hipótese II | `hipotese_perempcao` |
| `nao_comparecimento_60_dias` | BOOLEAN | Hipótese II | `hipotese_perempcao` |
| `querelante_ausente_ato_sem_motivo` | BOOLEAN | Hipótese III | `hipotese_perempcao` |
| `querelante_sem_pedido_condenacao_alegacoes_finais` | BOOLEAN | Hipótese III | `hipotese_perempcao` |
| `querelante_pj_extinta_sem_sucessor` | BOOLEAN | Hipótese IV | `hipotese_perempcao` |

---

## 10. Extinção da Punibilidade (Art. 61; 62)

| Coluna | Tipo | Descrição | Consulta |
|---|---|---|---|
| `juiz_reconhece_extincao_qualquer_fase` | BOOLEAN | Art. 61 | `juiz_declara_extincao_punibilidade_de_oficio` |
| `certidao_obito_acusado` | BOOLEAN | Art. 62 | `extincao_punibilidade_por_morte` |
| `mp_ouvido_morte_acusado` | BOOLEAN | Art. 62 | `extincao_punibilidade_por_morte` |
| `juiz_declarou_extincao_morte` | BOOLEAN | Art. 62 | `extincao_punibilidade_por_morte` |

---

## 11. Rótulos de Saída (Targets para o Treinamento)

Essas colunas representam a **decisão final esperada da IA** — o que o modelo deve aprender a prever. São derivadas das consultas acima.

| Coluna (target) | Tipo | Descrição | Origem |
|---|---|---|---|
| `y_cabivel_anpp` | BOOLEAN | Se o ANPP é cabível | `cabivel_anpp` |
| `y_vedacao_anpp` | BOOLEAN | Se há vedação ao ANPP | `vedacao_anpp_aplicavel` |
| `y_homologacao_anpp` | BOOLEAN | Se o ANPP foi homologado | `homologacao_anpp` |
| `y_extincao_punibilidade_anpp` | BOOLEAN | Se houve extinção por ANPP | `extincao_punibilidade_anpp` |
| `y_cabivel_acao_privada_subsidiaria` | BOOLEAN | Se cabe ação privada subsidiária | `cabivel_acao_privada_subsidiaria` |
| `y_decadencia_queixa_representacao` | BOOLEAN | Se houve decadência (6 meses) | `decadencia_direito_queixa_ou_representacao` |
| `y_decadencia_violencia_domestica` | BOOLEAN | Se houve decadência (12 meses) | `decadencia_violencia_domestica_mulher` |
| `y_representacao_irretratavel` | BOOLEAN | Se a representação é irretratável | `representacao_irretratavel` |
| `y_queixa_indivisivel` | BOOLEAN | Se a queixa é indivisível | `queixa_indivisivel` |
| `y_renuncia_estende_todos` | BOOLEAN | Se a renúncia se estende a todos | `renuncia_estende_a_todos` |
| `y_perdao_aproveita_todos` | BOOLEAN | Se o perdão aproveita a todos | `perdao_aproveita_a_todos` |
| `y_extincao_punibilidade_perdao` | BOOLEAN | Se houve extinção por perdão | `extincao_punibilidade_perdao` |
| `y_perempcao_acao_penal` | BOOLEAN | Se houve perempção | `perempcao_acao_penal` |
| `y_extincao_punibilidade_morte` | BOOLEAN | Se houve extinção por morte do acusado | `extincao_punibilidade_por_morte` |
| `y_acao_publica_incondicionada` | BOOLEAN | Se a ação é pública incondicionada | `acao_penal_publica_incondicionada` |
| `y_prazo_denuncia_dias` | INTEGER | Prazo para denúncia (5 ou 15) | `prazo_denuncia/1` |

---

## Observações para a Modelagem de Dados

1. **Granularidade**: Cada linha da tabela representa **um caso concreto** (um inquérito ou processo). As colunas booleanas indicam a presença/ausência de fatos jurídicos que ativam as regras Prolog.

2. **Valores nulos (`n/a`)**: Use `NULL` ou `n/a` para colunas que não se aplicam (ex.: `forma_representacao_pj` quando a vítima é pessoa física). O Prolog trata `n/a` como fato ausente.

3. **Datas**: `data_ciencia_autoria`, `data_exercicio_queixa`, `data_recebimento_autos_mp` são essenciais para calcular decadência (Art. 38) e prazos (Art. 46) — o modelo pode derivar `y_decadencia_*` por diferença de datas.

4. **Pena mínima**: `pena_minima_cominada_anos + causas_aumento_anos - causas_diminuicao_anos` alimenta diretamente `pena_minima_para_anpp/1` (Art. 28-A, §1º).

5. **Colunas derivadas vs. brutas**: As colunas de 1 a 10 são **features** (entradas); as da seção 11 são **targets** (saídas). Para treinar a IA, você pode usar as features para prever os targets — ou usar os targets como rótulos de consistência jurídica.

6. **Volume mínimo sugerido**: Para cobrir todas as combinações de regras (especialmente ANPP, que tem 4 requisitos + 5 vedações + 5 condições), recomenda-se pelo menos **500–1.000 casos sintéticos** gerados a partir das regras Prolog, com variação controlada de cada booleano.
