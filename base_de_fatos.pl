% ============================================================
% TÍTULO III - DA AÇÃO PENAL
% Transposição do CPP (Arts. 24 a 62) para Prolog
% ============================================================


% ============================================================
% FATOS
% ============================================================

% --- Art. 24: Espécies de ação penal ---
acao_penal_publica.
acao_penal_privada.

% A ação pública depende, quando a lei exigir, de:
condicao_acao_publica(requisicao_ministro_justica).
condicao_acao_publica(representacao_ofendido).
condicao_acao_publica(representacao_representante_legal).

% --- Art. 24, §1º: Ordem de legitimidade para representação em caso de morte/ausência ---
ordem_representacao_morte(1, conjuge).
ordem_representacao_morte(2, ascendente).
ordem_representacao_morte(3, descendente).
ordem_representacao_morte(4, irmao).

% --- Art. 24, §2º: Crime contra patrimônio/interesse da União, Estado, Município ---
ente_publico(uniao).
ente_publico(estado).
ente_publico(municipio).

% --- Art. 26: Contravenções ---
acao_penal_contravencao(auto_prisao_flagrante).
acao_penal_contravencao(portaria_autoridade_judiciaria).
acao_penal_contravencao(portaria_autoridade_policial).

% --- Art. 28-A, caput: Requisitos do acordo de não persecução penal (ANPP) ---
requisito_anpp(confissao_formal_e_circunstancial).
requisito_anpp(infraccao_sem_violencia_ou_grave_ameaca).
requisito_anpp(pena_minima_inferior_4_anos).
requisito_anpp(necessario_e_suficiente_para_reprovacao_e_prevencao).

% --- Art. 28-A, I a V: Condições do ANPP (cumulativa e alternativamente) ---
condicao_anpp(reparar_dano_ou_restituir_coisa).
condicao_anpp(renunciar_bens_e_direitos).
condicao_anpp(prestar_servico_comunidade_ou_entidades_publicas).
condicao_anpp(pagar_prestacao_pecuniaria).
condicao_anpp(cumprir_outra_condicao_proporcional_compativel).

% --- Art. 28-A, §2º: Hipóteses de vedação do ANPP ---
vedacao_anpp(cabivel_transacao_penal_jecrim).
vedacao_anpp(investigado_reincidente).
vedacao_anpp(elementos_conduta_criminal_habitual_reiterada_profissional).
vedacao_anpp(beneficiado_anpp_transacao_suspensao_nos_5_anos_anteriores).
vedacao_anpp(crime_violencia_domestica_familiar_ou_contra_mulher_por_condicao_de_sexo).

% --- Art. 36: Ordem de preferência entre titulares do direito de queixa ---
ordem_preferencia_queixa(1, conjuge).
ordem_preferencia_queixa(2, ascendente).
ordem_preferencia_queixa(3, descendente).
ordem_preferencia_queixa(4, irmao).

% --- Art. 38: Prazos de decadência ---
prazo_decadencia_geral(6, meses).
prazo_decadencia_violencia_domestica_mulher(12, meses).

% --- Art. 46: Prazos para oferecimento da denúncia ---
prazo_denuncia_reu_preso(5, dias).
prazo_denuncia_reu_solto_ou_afiancado(15, dias).
prazo_aditamento_queixa(3, dias).

% --- Art. 58: Prazo para aceitação do perdão ---
prazo_aceitacao_perdao(3, dias).

% --- Art. 60: Prazos de perempção ---
prazo_perempcao_inacao_querelante(30, dias_seguidos).
prazo_perempcao_falecimento_ou_incapacidade(60, dias).


% ============================================================
% REGRAS LÓGICAS
% ============================================================

% --- Art. 24, caput: Ação pública promovida por denúncia do MP ---
acao_publica_promovida_por(denuncia_ministerio_publico).

% Ação pública dependente de condição quando a lei exigir
acao_publica_dependente(Condicao) :-
    acao_penal_publica,
    condicao_acao_publica(Condicao).

% --- Art. 24, §1º: Transferência do direito de representação ---
legitimado_representacao_morte(Sujeito) :-
    ordem_representacao_morte(_, Sujeito).

% --- Art. 24, §2º: Ação pública incondicionada em crimes contra entes públicos ---
acao_penal_publica_incondicionada(Crime) :-
    praticado_em_detrimento(Crime, Ente),
    ente_publico(Ente).

% --- Art. 25: Representação irretratável após denúncia ---
representacao_irretratavel :- 
    denuncia_oferecida.

% --- Art. 27: Qualquer pessoa do povo pode provocar o MP ---
legitimado_provocar_mp(pessoa_do_povo) :-
    acao_penal_publica.

% --- Art. 28: Arquivamento comunicado à vítima, investigado e autoridade policial ---
arquivamento_comunicado :- 
    vitima(V), investigado(I), autoridade_policial(A),
    comunicar(V), comunicar(I), comunicar(A).

% --- Art. 28-A, caput: Cabimento do ANPP ---
cabivel_anpp :-
    nao_caso_de_arquivamento,
    requisito_anpp(confissao_formal_e_circunstancial),
    requisito_anpp(infraccao_sem_violencia_ou_grave_ameaca),
    requisito_anpp(pena_minima_inferior_4_anos),
    requisito_anpp(necessario_e_suficiente_para_reprovacao_e_prevencao),
    \+ vedacao_anpp_aplicavel.

% --- Art. 28-A, §1º: Pena mínima considera aumento e diminuição ---
pena_minima_para_anpp(Pena) :-
    pena_minima_cominada(PenaBase),
    causas_aumento(A), causas_diminuicao(D),
    Pena is PenaBase + A - D.

% --- Art. 28-A, §2º: Vedações ao ANPP ---
vedacao_anpp_aplicavel :-
    vedacao_anpp(Hipotese),
    hipotese_presente(Hipotese).

% --- Art. 28-A, §3º: Formalização do ANPP ---
anpp_formalizado :- 
    escrito,
    assinado_por(membro_ministerio_publico),
    assinado_por(investigado),
    assinado_por(defensor).

% --- Art. 28-A, §4º: Homologação mediante audiência ---
homologacao_anpp :- 
    audiencia_realizada,
    verificada_voluntariedade,
    verificada_legalidade.

% --- Art. 28-A, §5º: Devolução ao MP se condições inadequadas ---
devolucao_anpp_mp :-
    condicoes_inadequadas_ou_insuficientes_ou_abusivas.

% --- Art. 28-A, §6º: Após homologação, execução perante juízo de execução penal ---
execucao_anpp :- 
    homologado_judicialmente,
    remessa_ao_mp_para_execucao.

% --- Art. 28-A, §7º: Juiz pode recusar homologação ---
recusa_homologacao :- 
    requisitos_legais_nao_atendidos.
recusa_homologacao :- 
    inadequacao_nao_realizada.

% --- Art. 28-A, §8º: Recusada homologação, devolução ao MP ---
devolucao_pos_recusa :- 
    recusa_homologacao,
    remessa_ao_mp_para_complementacao_ou_denuncia.

% --- Art. 28-A, §9º: Vítima intimada da homologação e do descumprimento ---
intimacao_vitima :- 
    homologacao_anpp, intimar(vitima).
intimacao_vitima :- 
    descumprimento_anpp, intimar(vitima).

% --- Art. 28-A, §10: Descumprimento gera rescisão e denúncia ---
rescisao_anpp_e_denuncia :- 
    descumprimento_condicao_anpp,
    comunicacao_ao_juizo,
    oferecimento_denuncia.

% --- Art. 28-A, §11: Descumprimento pode justificar não oferecimento de suspensão condicional ---
justifica_nao_suspensao_condicional :- 
    descumprimento_anpp.

% --- Art. 28-A, §12: ANPP não consta de certidão de antecedentes, salvo Art. 28-A, §2º, III ---
anpp_nao_consta_certidao :- 
    celebracao_e_cumprimento_anpp,
    \+ finalidade_inciso_III_paragrafo_2.

% --- Art. 28-A, §13: Cumprimento integral gera extinção de punibilidade ---
extincao_punibilidade_anpp :- 
    cumprimento_integral_anpp,
    decreto_juizo_competente.

% --- Art. 28-A, §14: Recusa do MP em propor ANPP permite remessa a órgão superior ---
remessa_orgao_superior :- 
    recusa_mp_em_propor_anpp,
    requerimento_investigado.

% --- Art. 29: Ação privada subsidiária da pública ---
cabivel_acao_privada_subsidiaria :- 
    acao_penal_publica,
    nao_intentada_no_prazo_legal.

% Atribuições do MP na ação privada subsidiária
atribuicao_mp_acao_subsidiaria(aditar_queixa).
atribuicao_mp_acao_subsidiaria(repudiar_queixa).
atribuicao_mp_acao_subsidiaria(oferecer_denuncia_substitutiva).
atribuicao_mp_acao_subsidiaria(intervir_em_todos_os_termos).
atribuicao_mp_acao_subsidiaria(fornecer_elementos_de_prova).
atribuicao_mp_acao_subsidiaria(interpor_recurso).
atribuicao_mp_acao_subsidiaria(retomar_acao_como_parte_principal).

% --- Art. 30: Titular da ação privada ---
titular_acao_privada(ofendido).
titular_acao_privada(quem_tenha_qualidade_para_representar_ofendido).

% --- Art. 31: Transferência do direito de queixa em caso de morte/ausência ---
legitimado_queixa_morte(Sujeito) :-
    ordem_representacao_morte(_, Sujeito).

% --- Art. 32: Nomeação de advogado ao pobre ---
nomeacao_advogado_pobre :- 
    acao_penal_privada,
    requerimento_parte,
    comprovacao_pobreza.

pessoa_pobre :- 
    nao_pode_prover_despesas_processo_sem_privar_se_do_sustento.

prova_pobreza(atestado_autoridade_policial).

% --- Art. 33: Curador especial ---
cabivel_curador_especial :- 
    ofendido_menor_18_ou_mentalmente_enfermo_ou_retardado_mental,
    (nao_tem_representante_legal ; colidem_interesses).

% --- Art. 34: Ofendido menor de 21 e maior de 18 ---
titular_queixa_menor_21_maior_18(ofendido).
titular_queixa_menor_21_maior_18(representante_legal).

% --- Art. 36: Preferência entre titulares do direito de queixa ---
preferencia_queixa(Sujeito) :-
    ordem_preferencia_queixa(_, Sujeito).

prosseguimento_por_outro_titular :- 
    desistencia_da_instancia.
prosseguimento_por_outro_titular :- 
    abandono_da_acao.

% --- Art. 37: Pessoas jurídicas podem exercer ação penal ---
pode_exercer_acao_penal(Fundacao) :- fundacao_legalmente_constituida(Fundacao).
pode_exercer_acao_penal(Associacao) :- associacao_legalmente_constituida(Associacao).
pode_exercer_acao_penal(Sociedade) :- sociedade_legalmente_constituida(Sociedade).

representacao_pessoa_juridica(contrato_ou_estatuto).
representacao_pessoa_juridica(diretores_ou_socios_gerentes) :- 
    silencio_contrato_estatuto.

% --- Art. 38: Decadência ---
decadencia_direito_queixa_ou_representacao :- 
    prazo_decadencia_geral(Prazo, Unidade),
    nao_exercicio_no_prazo(Prazo, Unidade).

decadencia_violencia_domestica_mulher :- 
    prazo_decadencia_violencia_domestica_mulher(Prazo, Unidade),
    nao_exercicio_no_prazo(Prazo, Unidade).

% --- Art. 39: Forma da representação ---
forma_representacao(pessoalmente).
forma_representacao(por_procurador_com_poderes_especiais).

meio_representacao(escrita).
meio_representacao(oral).

destinatario_representacao(juiz).
destinatario_representacao(orgao_ministerio_publico).
destinatario_representacao(autoridade_policial).

% --- Art. 40: Juízes/tribunais remetem cópias ao MP ---
remessa_copias_mp :- 
    juiz_ou_tribunal_verifica_crime_acao_publica.

% --- Art. 41: Conteúdo da denúncia ou queixa ---
conteudo_denuncia_ou_queixa(exposicao_fato_criminoso_com_circunstancias).
conteudo_denuncia_ou_queixa(qualificacao_acusado_ou_esclarecimentos_identificacao).
conteudo_denuncia_ou_queixa(classificacao_crime).
conteudo_denuncia_ou_queixa(rol_testemunhas) :- necessario.

% --- Art. 42: MP não pode desistir da ação penal ---
vedado_mp(desistir_acao_penal).

% --- Art. 44: Queixa por procurador com poderes especiais ---
queixa_por_procurador :- 
    poderes_especiais,
    nome_querelante_no_mandato,
    mencao_fato_criminoso_no_mandato.

% --- Art. 45: Aditamento da queixa pelo MP ---
mp_pode_aditar_queixa :- 
    queixa_oferecida.

% --- Art. 46: Prazos para denúncia ---
prazo_denuncia(5) :- reu_preso.
prazo_denuncia(15) :- reu_solto_ou_afiancado.

% --- Art. 47: Requisição de esclarecimentos e documentos pelo MP ---
mp_pode_requisitar :- 
    necessarios_maiores_esclarecimentos_ou_documentos_ou_elementos_de_conviccao.

% --- Art. 48: Indivisibilidade da queixa ---
queixa_indivisivel :- 
    queixa_contra_um_dos_autores,
    processo_de_todos_os_autores.

% --- Art. 49: Renúncia a um autor estende-se a todos ---
renuncia_estende_a_todos :- 
    renuncia_em_relacao_a_um_autor.

% --- Art. 50: Forma da renúncia expressa ---
renuncia_expressa :- 
    declaracao_assinada_pelo_ofendido_ou_representante_ou_procurador_com_poderes_especiais.

% --- Art. 51: Perdão a um querelado aproveita a todos, salvo recusa ---
perdao_aproveita_a_todos :- 
    perdao_concedido_a_um_querelado,
    \+ recusa_do_querelado.

% --- Art. 52: Perdão pelo querelante menor de 21 e maior de 18 ---
perdao_por_menor_21_maior_18 :- 
    querelante_menor_21_maior_18,
    (perdao_pelo_querelante ; perdao_pelo_representante_legal),
    \+ oposicao_da_outra_parte.

% --- Art. 53: Aceitação do perdão pelo curador ---
aceitacao_perdao_pelo_curador :- 
    querelado_mentalmente_enfermo_ou_retardado_mental,
    (nao_tem_representante_legal ; colidem_interesses),
    curador_nomeado_pelo_juiz.

% --- Art. 54: Aceitação do perdão por querelado menor de 21 ---
aceitacao_perdao_menor_21 :- 
    querelado_menor_21,
    aplica_art_52.

% --- Art. 55: Perdão aceito por procurador com poderes especiais ---
perdao_aceito_por_procurador :- 
    procurador_com_poderes_especiais.

% --- Art. 56: Perdão extraprocessual expresso segue Art. 50 ---
perdao_extraprocessual_expresso :- 
    aplica_art_50.

% --- Art. 57: Renúncia tácita e perdão tácito admitem todos os meios de prova ---
renuncia_tacita_admite_todos_meios_prova.
perdao_tacito_admite_todos_meios_prova.

% --- Art. 58: Aceitação do perdão em 3 dias; silêncio importa aceitação ---
aceitacao_perdao_no_prazo :- 
    intimacao_querelado,
    manifestacao_em_3_dias.
aceitacao_perdao_por_silencio :- 
    intimacao_querelado,
    silencio_por_3_dias.

extincao_punibilidade_perdao :- 
    perdao_aceito,
    juiz_julga_extinta_punibilidade.

% --- Art. 59: Aceitação do perdão fora do processo ---
aceitacao_perdao_fora_processo :- 
    declaracao_assinada_pelo_querelado_ou_representante_ou_procurador_com_poderes_especiais.

% --- Art. 60: Perempção da ação penal privada ---
perempcao_acao_penal :- 
    somente_mediante_queixa,
    hipotese_perempcao.

hipotese_perempcao :- 
    iniciada_acao,
    querelante_deixa_andamento_por_30_dias_seguidos.
hipotese_perempcao :- 
    falecimento_ou_incapacidade_querelante,
    nao_comparecimento_em_60_dias_de_quem_couber.
hipotese_perempcao :- 
    querelante_deixa_de_comparecer_sem_motivo_justificado_a_ato_do_processo.
hipotese_perempcao :- 
    querelante_deixa_de_formular_pedido_condenacao_alegacoes_finais.
hipotese_perempcao :- 
    querelante_pessoa_juridica_extinta_sem_sucessor.

% --- Art. 61: Declaração de ofício da extinção da punibilidade ---
juiz_declara_extincao_punibilidade_de_oficio :- 
    reconhece_extincao_punibilidade_em_qualquer_fase.

% --- Art. 62: Morte do acusado ---
extincao_punibilidade_por_morte :- 
    certidao_obito,
    ouvido_ministerio_publico,
    declaracao_juiz.
