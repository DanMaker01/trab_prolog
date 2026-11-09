:- encoding(utf8).
/*  experimento_a.pl -- roda a árvore A, com os três perfis, sobre os réus reais
    swipl -g main -t halt prolog/experimento_a.pl
    ->  resultados/arvore_a.csv (dado faltante a favor do réu) e resultados/arvore_a_onus.csv (contra)
*/
:- ensure_loaded(arvore_a).
:- dynamic dir_exp/1.
:- prolog_load_context(directory, D), retractall(dir_exp(_)), assertz(dir_exp(D)).
saida(Nome, Arq) :- dir_exp(D), atomic_list_concat([D, '/../resultados/', Nome], Arq).
:- ensure_loaded(fatos_casos).

rotulo(concede(F), R) :- format(atom(R), "concede ~w", [F]).
rotulo(nega, nega).
rotulo(nao_aplicavel, nao_aplicavel).

ref(C, Inst, R) :- ( referencia(C, Inst, V) -> term_to_atom(V, R) ; R = '' ).

main :-
    retractall(politica_global(_)), saida('arvore_a.csv', A1), roda(A1),
    assertz(politica_global(onus_defesa)), saida('arvore_a_onus.csv', A2), roda(A2),
    retractall(politica_global(_)).

roda(Arq) :-
    open(Arq, write, S),
    format(S, "caso,fonte,relator,garantista,intermediario,restritivo,motivos_restritivo,tj_p4,stj_p4,resultado~n", []),
    forall(caso(C, Fonte, Rel),
      ( \+ sub_atom(C, 0, _, _, t_),
        decide(garantista, C, D1, _), decide(intermediario, C, D2, _), decide(restritivo, C, D3, M3),
        maplist(rotulo, [D1, D2, D3], [R1, R2, R3]),
        term_to_atom(M3, MA), ref(C, tj_p4, TJ), ref(C, stj_p4, STJ), ref(C, resultado, RES),
        format(S, "~w,~w,\"~w\",~w,~w,~w,\"~w\",~w,~w,~w~n", [C, Fonte, Rel, R1, R2, R3, MA, TJ, STJ, RES]) )),
    close(S).
