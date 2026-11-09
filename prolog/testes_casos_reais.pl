:- encoding(utf8).
/*  testes_casos_reais.pl -- testes de regressão com réus REAIS (prolog/fatos_casos.pl)
    swipl -g run_tests -t halt prolog/testes_casos_reais.pl
    Fixam os resultados que o texto do trabalho cita (experimento E2 e exemplos).
*/
:- use_module(library(plunit)).
:- ensure_loaded(arvore_a).
:- ensure_loaded(fatos_casos).

% o identificador do réu começa com p4_<registro>
reu(Registro, C) :- atom_concat(p4_, Registro, Pref), caso(C, p4, _), sub_atom(C, 0, _, _, Pref), !.

% E2: o relator concedeu sozinho e a Turma reformou. A leitura garantista reproduz o relator;
% a intermediária e a restritiva reproduzem a Turma.
relator_vencido('202501891953').   % AREsp 2.946.226, 432 kg de maconha
relator_vencido('202502468442').   % HC 1.017.077, 2 kg de cocaína
relator_vencido('202502487449').   % HC 1.017.446, 17 kg
relator_vencido('202504939960').   % HC 1.060.758, 308 kg de maconha

:- begin_tests(e2_relator_x_turma).
test(garantista_concede, [forall(relator_vencido(R))]) :-
    reu(R, C), decide(garantista, C, concede(_), _).
test(intermediario_nega, [forall(relator_vencido(R))]) :-
    reu(R, C), decide(intermediario, C, nega, _).
test(restritivo_nega, [forall(relator_vencido(R))]) :-
    reu(R, C), decide(restritivo, C, nega, _).
:- end_tests(e2_relator_x_turma).

:- begin_tests(exemplos).
% HC 1.091.524: 11 g de maconha; o TJ negou a redução só por causa do celular
test(celular_isolado_garantista)    :- reu('202601572319', C), decide(garantista, C, concede(_), _).
test(celular_isolado_restritivo)    :- reu('202601572319', C), decide(restritivo, C, nega, [nao_dedica]).
% 432 kg de maconha: a fração da leitura garantista é a mínima (1/6)
test(fracao_minima_432kg)           :- reu('202501891953', C), decide(garantista, C, concede(1/6), _).
% nenhum réu real fica sem decisão em nenhuma leitura
test(todos_decididos) :-
    forall(( caso(C, F, _), F \== teste, perfil(P) ), once(decide(P, C, _, _))).
:- end_tests(exemplos).
