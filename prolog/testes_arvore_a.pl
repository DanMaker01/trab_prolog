:- encoding(utf8).
/*  testes_arvore_a.pl -- testes unitários da árvore A (casos sintéticos)
    Rodar:  swipl -g run_tests -t halt prolog/testes_arvore_a.pl
*/
:- use_module(library(plunit)).
:- ensure_loaded(arvore_a).

% ---------- casos sintéticos (prefixo t_) ----------
% primário, bons antecedentes, 20 g de cocaína, nada mais
caso(t_simples, teste, '').
data_fato(t_simples, date(2024, 1, 10)).
droga(t_simples, cocaina). qtd_g(t_simples, 20).
primario(t_simples, sim). maus_antecedentes(t_simples, nao).

% reincidente
caso(t_reinc, teste, '').
droga(t_reinc, maconha). qtd_g(t_reinc, 50).
primario(t_reinc, nao). reincidente(t_reinc, sim).

% fato anterior à Lei 11.343/2006
caso(t_lei_antiga, teste, '').
data_fato(t_lei_antiga, date(2005, 3, 1)).
primario(t_lei_antiga, sim). maus_antecedentes(t_lei_antiga, nao).

% só ações penais em curso (Tema 1.139)
caso(t_acoes, teste, '').
droga(t_acoes, crack). qtd_g(t_acoes, 15).
primario(t_acoes, sim). maus_antecedentes(t_acoes, nao). acoes_em_curso(t_acoes, sim).

% 432 kg de maconha, primário, sem outro indício (como o AREsp 2.946.226)
caso(t_432kg, teste, '').
droga(t_432kg, maconha). qtd_g(t_432kg, 432000).
primario(t_432kg, sim). maus_antecedentes(t_432kg, nao).

% primariedade não informada
caso(t_faltante, teste, '').
droga(t_faltante, cocaina). qtd_g(t_faltante, 30).

% ato infracional 2 anos antes do fato + celular
caso(t_ato, teste, '').
data_fato(t_ato, date(2024, 5, 1)).
droga(t_ato, maconha). qtd_g(t_ato, 80).
primario(t_ato, sim). maus_antecedentes(t_ato, nao).
ato_infracional(t_ato, sim). ultimo_ato_infracional(t_ato, 2022). indicio(t_ato, celular).

% maus antecedentes antigos (condenação de 2010, fato em 2023)
caso(t_antigo, teste, '').
data_fato(t_antigo, date(2023, 11, 18)).
droga(t_antigo, cocaina). qtd_g(t_antigo, 40).
primario(t_antigo, sim). maus_antecedentes(t_antigo, sim). antecedente_ano(t_antigo, 2010).

% condenado também por associação (art. 35)
caso(t_assoc, teste, '').
droga(t_assoc, cocaina). qtd_g(t_assoc, 10).
primario(t_assoc, sim). maus_antecedentes(t_assoc, nao). associacao(t_assoc, condenado).

:- begin_tests(lei).
test(lei_antiga) :- decide(garantista, t_lei_antiga, nao_aplicavel, _).
test(lei_nova)   :- lei_aplicavel(t_simples, lei_11343).
:- end_tests(lei).

:- begin_tests(requisitos).
test(simples_todos_concedem, [forall(perfil(P))]) :- decide(P, t_simples, concede(_), []).
test(reincidente_todos_negam, [forall(perfil(P))]) :- decide(P, t_reinc, nega, M), memberchk(primario, M).
test(associacao_todos_negam, [forall(perfil(P))]) :- decide(P, t_assoc, nega, M), memberchk(nao_integra_orcrim, M).
:- end_tests(requisitos).

:- begin_tests(criterios_vagos).
% Tema 1.139: ações em curso não afastam o § 4º, salvo no perfil restritivo
test(tema1139_garantista)    :- decide(garantista, t_acoes, concede(_), _).
test(tema1139_intermediario) :- decide(intermediario, t_acoes, concede(_), _).
test(tema1139_restritivo)    :- decide(restritivo, t_acoes, nega, M), memberchk(nao_dedica, M).
% mesma quantidade (432 kg), leituras opostas
test(qtd_garantista)  :- decide(garantista, t_432kg, concede(1/6), _).
test(qtd_restritivo)  :- decide(restritivo, t_432kg, nega, [nao_dedica]).
% quantidade grande sozinha não basta no intermediário
test(qtd_intermediario) :- decide(intermediario, t_432kg, concede(1/6), _).
% dado faltante: in dubio pro reo x ônus da defesa
test(faltante_pro_reo)  :- decide(intermediario, t_faltante, concede(_), _).
test(faltante_onus, [setup(assertz(user:politica_global(onus_defesa))), cleanup(retractall(user:politica_global(_)))]) :-
    decide(intermediario, t_faltante, nega, M), memberchk(nao_comprovado(primario), M).
% ato infracional recente
test(ato_garantista)    :- decide(garantista, t_ato, concede(_), _).
test(ato_intermediario) :- decide(intermediario, t_ato, nega, [nao_dedica]).
% direito ao esquecimento
test(esquecimento_garantista)    :- decide(garantista, t_antigo, concede(_), _).
test(esquecimento_intermediario) :- decide(intermediario, t_antigo, nega, [bons_antecedentes]).
:- end_tests(criterios_vagos).

:- begin_tests(pena).
test(pena_2_3) :- pena(garantista, t_simples, M, aberto, sim), M =:= 20.
test(pena_sem_p4) :- pena(restritivo, t_432kg, 60, semiaberto, nao).
test(pena_reincidente) :- pena(garantista, t_reinc, _, fechado, nao).
:- end_tests(pena).
