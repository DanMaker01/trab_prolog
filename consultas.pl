% Art. 24 – Ação pública é promovida por denúncia do MP?
?- acao_publica_promovida_por(X).
% X = denuncia_ministerio_publico.

% Art. 24 – Quais condições a ação pública pode depender?
?- acao_publica_dependente(C).
% C = requisicao_ministro_justica ;
% C = representacao_ofendido ;
% C = representacao_representante_legal.

% Art. 24, §1º – Quem pode representar em caso de morte do ofendido?
?- legitimado_representacao_morte(S).
% S = conjuge ; S = ascendente ; S = descendente ; S = irmao.

% Art. 27 – Quem pode provocar o MP?
?- legitimado_provocar_mp(L).
% L = pessoa_do_povo.

% Art. 28-A – Cabe ANPP?
?- cabivel_anpp.
% true (se todos os requisitos forem satisfeitos e não houver vedação).

% Art. 28-A, §2º – Quais hipóteses vedam o ANPP?
?- vedacao_anpp(V).
% V = cabivel_transacao_penal_jecrim ;
% V = investigado_reincidente ;
% V = elementos_conduta_criminal_habitual_reiterada_profissional ;
% V = beneficiado_anpp_transacao_suspensao_nos_5_anos_anteriores ;
% V = crime_violencia_domestica_familiar_ou_contra_mulher_por_condicao_de_sexo.

% Art. 28-A, §13 – Quando há extinção da punibilidade pelo ANPP?
?- extincao_punibilidade_anpp.
% true (se cumprimento integral + decreto do juízo competente).

% Art. 29 – Cabe ação privada subsidiária?
?- cabivel_acao_privada_subsidiaria.
% true (se ação pública não intentada no prazo legal).

% Art. 29 – Quais atribuições do MP na ação subsidiária?
?- atribuicao_mp_acao_subsidiaria(A).
% A = aditar_queixa ; A = repudiar_queixa ; ... etc.

% Art. 31 – Quem pode oferecer queixa em caso de morte do ofendido?
?- legitimado_queixa_morte(S).
% S = conjuge ; S = ascendente ; S = descendente ; S = irmao.

% Art. 36 – Qual a ordem de preferência para a queixa?
?- ordem_preferencia_queixa(N, S).
% N = 1, S = conjuge ; N = 2, S = ascendente ; ...

% Art. 38 – Há decadência do direito de queixa/representação?
?- decadencia_direito_queixa_ou_representacao.
% true (se não exercido no prazo de 6 meses).

% Art. 38, §2º – Há decadência no caso de violência doméstica contra a mulher?
?- decadencia_violencia_domestica_mulher.
% true (se não exercido no prazo de 12 meses).

% Art. 41 – Qual o conteúdo da denúncia/queixa?
?- conteudo_denuncia_ou_queixa(C).
% C = exposicao_fato_criminoso_com_circunstancias ;
% C = qualificacao_acusado_ou_esclarecimentos_identificacao ;
% C = classificacao_crime ;
% C = rol_testemunhas (se necessário).

% Art. 42 – O MP pode desistir da ação penal?
?- vedado_mp(X).
% X = desistir_acao_penal.

% Art. 46 – Qual o prazo para denúncia?
?- prazo_denuncia(P).
% P = 5 (réu preso) ; P = 15 (réu solto ou afiançado).

% Art. 58 – Quando se dá a extinção da punibilidade pelo perdão?
?- extincao_punibilidade_perdao.
% true (se perdão aceito e juiz julga extinta).

% Art. 60 – Quando ocorre perempção?
?- perempcao_acao_penal.
% true (se somente mediante queixa + hipótese de perempção).

% Art. 62 – Quando há extinção da punibilidade por morte do acusado?
?- extincao_punibilidade_por_morte.
% true (se certidão de óbito + MP ouvido + declaração do juiz).
