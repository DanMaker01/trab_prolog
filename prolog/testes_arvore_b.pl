:- encoding(utf8).
/*  testes_arvore_b.pl -- a árvore B em Prolog decide exatamente como o modelo do scikit-learn
    swipl -g run_tests -t halt prolog/testes_arvore_b.pl
*/
:- use_module(library(plunit)).
:- ensure_loaded(arvore_b).
:- ensure_loaded(fatos_ementas).
:- ensure_loaded(pred_sklearn).

:- begin_tests(arvore_b).
test(equivalencia_com_relator) :-
    forall(pred_sklearn(com_relator, C, Esperado), arvore_b(com_relator, C, Esperado)).
test(equivalencia_sem_relator) :-
    forall(pred_sklearn(sem_relator, C, Esperado), arvore_b(sem_relator, C, Esperado)).
test(uma_resposta_por_caso) :-
    forall(pred_sklearn(M, C, _), findall(X, arvore_b(M, C, X), [_])).
:- end_tests(arvore_b).
